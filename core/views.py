from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.utils.timesince import timesince
from django.utils.text import slugify
from django.db.models import OuterRef, Subquery
from django.db.models import Q, Count, Sum, F, FloatField
from django.core.paginator import Paginator
from django.urls import reverse

from core.models import Post, Friend, FriendRequest, Notification, Comment, ReplyComment, ChatMessage, GroupChatMessage, GroupChat, Group
from userauths.models import User, Profile, user_directory_path

import random
import time
from agora_token_builder import RtcTokenBuilder
from .models import RoomVideoCall
import json
from django.core.exceptions import ObjectDoesNotExist

import shortuuid

# Notifications Keys
noti_new_like = "New Like"
noti_new_follower = "New Follower"
noti_friend_request = "Friend Request"
noti_new_comment = "New Comment"
noti_comment_liked = "Comment Liked"
noti_comment_replied = "Comment Replied"
noti_friend_request_accepted = "Friend Request Accepted"

@login_required
def index(request):
    posts = Post.objects.filter(active=True, visibility="Everyone")

    paginator = Paginator(posts, 3)  
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    context = {
        "posts":posts
    }
    return render(request, "core/index.html", context)

@login_required
def post_detail(request, slug):
    post = Post.objects.get(active=True, visibility="Everyone", slug=slug)
    context = {
        "p":post
    }
    return render(request, "core/post-detail.html", context)

def send_notification(user, sender, post, comment, notification_type):
    notification = Notification.objects.create(
        user=user, 
        sender=sender, 
        post=post, 
        comment=comment, 
        notification_type=notification_type
    )
    return notification

@csrf_exempt
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('post-caption')
        visibility = request.POST.get('visibility')
        image = request.FILES.get('post-thumbnail')

        print("Title ============", title)
        print("thumbnail ============", image)
        print("visibility ============", visibility)

        uuid_key = shortuuid.uuid()
        uniqueid = uuid_key[:4]

        if title and image:
            post = Post(title=title, image=image, visibility=visibility, user=request.user, slug=slugify(title) + "-" + str(uniqueid.lower()))
            post.save()

            
            return JsonResponse({'post': {
                'title': post.title,
                'image_url': post.image.url,
                "full_name":post.user.profile.full_name,
                "profile_image":post.user.profile.image.url,
                "date":timesince(post.date),
                "id":post.id,
            }})
        else:
            return JsonResponse({'error': 'Invalid post data'})

    return JsonResponse({"data":"Sent"})


@csrf_exempt
def delete_post(request):
    id = request.GET['id']
    post = Post.objects.get(id=id)
    post.delete()

    data = {
        "bool":True,
    }
    return JsonResponse({"data":data})
        
def get_post(request):
    try:
        post_id = request.GET['id']
        post = Post.objects.get(id=post_id)

        posts = {
            "title": post.title,
            "image": post.image.url,
            "visibility": post.visibility
        }
        return JsonResponse(posts)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)


@csrf_exempt
def edit_post(request):
    try:
        if request.method == 'POST':
            post_id = request.POST.get('post-id')
            title = request.POST.get('post-caption')
            visibility = request.POST.get('visibility')
            post = Post.objects.get(id=post_id)

            image = request.FILES.get('post-thumbnail') if 'post-thumbnail' in request.FILES else request.POST.get('url-image')
            print("image = ", image)
            if image:
                if 'post-thumbnail' in request.POST and '/media/' in image:
                    image = image.replace('/media/', '') 
                post.image = image
                print(post.image)


            post.title = title
            post.visibility = visibility
            post.save()

            updated_post = {
                "title": post.title,
                "image": post.image.url,
                "visibility": post.visibility
            }
            return JsonResponse(updated_post)
        else:
            return HttpResponse("Invalid request method")
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)


@csrf_exempt
def like_post(request):

    id = request.GET['id']
    post = Post.objects.get(id=id)
    user = request.user
    bool = False 

    if user in post.likes.all():
        post.likes.remove(user)
        bool = False
    else:
        post.likes.add(user)
        bool = True 
        # Do this during noticiation lecture
        if post.user != request.user:
            send_notification(post.user, user, post, None, noti_new_like)

    data = {
        "bool":bool,
        'likes':post.likes.all().count()
    }
    return JsonResponse({"data":data})


@csrf_exempt
def comment_on_post(request):

    id = request.GET['id']
    comment = request.GET['comment']
    post = Post.objects.get(id=id)
    comment_count = Comment.objects.filter(post=post).count()
    user = request.user

    new_comment = Comment.objects.create(
        post=post,
        comment=comment,
        user=user
    )

    # Notifications system
    if new_comment.user != post.user:
        send_notification(post.user, user, post, new_comment, noti_new_comment)


    data = {
        "bool":True,
        'comment':new_comment.comment,
        "profile_image":new_comment.user.profile.image.url,
        "date":timesince(new_comment.date),
        "comment_id":new_comment.id,
        "post_id":new_comment.post.id,
        "comment_count":comment_count + int(1)
    }
    return JsonResponse({"data":data})



@csrf_exempt
def like_comment(request):

    id = request.GET['id']
    comment = Comment.objects.get(id=id)
    user = request.user
    bool = False 

    if user in comment.likes.all():
        comment.likes.remove(user)
        bool = False
    else:
        comment.likes.add(user)
        bool = True 

        # Notifications system
        if comment.user != user:
            send_notification(comment.user, user, comment.post, comment, noti_comment_liked)


    data = {
        "bool":bool,
        'likes':comment.likes.all().count()
    }
    return JsonResponse({"data":data})



@csrf_exempt
def reply_comment(request):

    id = request.GET['id']
    reply = request.GET['reply']

    comment = Comment.objects.get(id=id)
    user = request.user

    new_reply = ReplyComment.objects.create(
        comment=comment,
        reply=reply,
        user=user
    )

    # Notifications system
    if comment.user != user:
        send_notification(comment.user, user, comment.post, comment, noti_comment_replied)

    data = {
        "bool":True,
        'reply':new_reply.reply,
        "profile_image":new_reply.user.profile.image.url,
        "date":timesince(new_reply.date),
        "reply_id":new_reply.id,
        "post_id":new_reply.comment.post.id,
    }
    return JsonResponse({"data":data})


@csrf_exempt
def delete_comment(request):
    id = request.GET['id']
    
    comment = Comment.objects.get(id=id, user=request.user)
    comment.delete()

    data = {
        "bool":True,
    }
    return JsonResponse({"data":data})




@csrf_exempt
def add_friend(request):
    sender = request.user
    receiver_id = request.GET['id'] 
    bool = False

    if sender.id == int(receiver_id):
        return JsonResponse({'error': 'Bạn không thể gửi kết bạn cho chính mình'})
    
    receiver = User.objects.get(id=receiver_id)
    
    try:
        friend_request = FriendRequest.objects.get(sender=sender, receiver=receiver)
        if friend_request:
            friend_request.delete()
        bool = False
        return JsonResponse({'error': 'Cancelled', 'bool':bool})
    except FriendRequest.DoesNotExist:
        friend_request = FriendRequest(sender=sender, receiver=receiver)
        friend_request.save()
        bool = True
        
        
        send_notification(receiver, sender, None, None, noti_friend_request)

        return JsonResponse({'success': 'Sent',  'bool':bool})
    


@csrf_exempt
def accept_friend_request(request):
    id = request.GET['id'] 

    receiver = request.user
    sender = User.objects.get(id=id)
    
    friend_request = FriendRequest.objects.filter(receiver=receiver, sender=sender).first()

    receiver.profile.friends.add(sender)
    sender.profile.friends.add(receiver)

    friend_request.delete()

    send_notification(sender, receiver, None, None, noti_friend_request_accepted)

    data = {
        "message":"Accepted",
        "bool":True,
    }
    
    return JsonResponse({'data': data})



@csrf_exempt
def reject_friend_request(request):
    id = request.GET['id'] 

    receiver = request.user
    sender = User.objects.get(id=id)
    
    friend_request = FriendRequest.objects.filter(receiver=receiver, sender=sender).first()
    friend_request.delete()

    data = {
        "message":"Rejected",
        "bool":True,
    }
    return JsonResponse({'data': data})


@csrf_exempt
def unfriend(request):
    sender = request.user
    friend_id = request.GET['id'] 
    bool = False

    if sender.id == int(friend_id):
        return JsonResponse({'error': 'You cannot unfriend yourself, wait a minute how did you even send yourself a friend request?.'})
    
    my_friend = User.objects.get(id=friend_id)
    
    if my_friend in sender.profile.friends.all():
        sender.profile.friends.remove(my_friend)
        my_friend.profile.friends.remove(sender)
        bool = True
        return JsonResponse({'success': 'Unfriend Successfull',  'bool':bool})
    
    


@login_required
def inbox(request):
    user_id = request.user

    chat_message = ChatMessage.objects.filter(
        id__in =  Subquery(
            User.objects.filter(
                Q(sender__reciever=user_id) |
                Q(reciever__sender=user_id)
            ).distinct().annotate(
                last_msg=Subquery(
                    ChatMessage.objects.filter(
                        Q(sender=OuterRef('id'),reciever=user_id) |
                        Q(reciever=OuterRef('id'),sender=user_id)
                    ).order_by('-id')[:1].values_list('id',flat=True) 
                )
            ).values_list('last_msg', flat=True).order_by("-id")
        )
    ).order_by("-id")
    
    context = {
        'chat_message': chat_message,
    }
    return render(request, 'chat/inbox.html', context)


@login_required
def inbox_detail(request, username):
    user_id = request.user
    
    message_list = ChatMessage.objects.filter(
        id__in =  Subquery(
            User.objects.filter(
                Q(sender__reciever=user_id) |
                Q(reciever__sender=user_id)
            ).distinct().annotate(
                last_msg=Subquery(
                    ChatMessage.objects.filter(
                        Q(sender=OuterRef('id'),reciever=user_id) |
                        Q(reciever=OuterRef('id'),sender=user_id)
                    ).order_by('-id')[:1].values_list('id',flat=True) 
                )
            ).values_list('last_msg', flat=True).order_by("-id")
        )
    ).order_by("-id")

    sender = request.user
    receiver = User.objects.get(username=username)
    receiver_details = User.objects.get(username=username)
    
    messages_detail = ChatMessage.objects.filter(
        Q(sender=sender, reciever=receiver) | Q(sender=receiver, reciever=sender)
    ).order_by("date")

    messages_detail.update(is_read=True)
    if messages_detail:
        r = messages_detail.first()
        reciever = User.objects.get(username=r.reciever)
    else:
        reciever = User.objects.get(username=username)

    context = {
        'message_detail': messages_detail,
        "reciever":reciever,
        "sender":sender,
        "receiver_details":receiver_details,
        "message_list":message_list,
    }
    return render(request, 'chat/inbox_detail.html', context)


def block_user(request):
    id = request.GET['id']
    user = request.user
    friend = User.objects.get(id=id)

    if user.id == friend.id:
        return JsonResponse({'error': 'You cannot block yourself'})


    if friend in user.profile.friends.all():
        user.profile.blocked.add(friend)
        user.profile.friends.remove(friend)
        friend.profile.friends.remove(user)
    else:
        return JsonResponse({'error': 'You cannot block someone that is not your friend'})

    return JsonResponse({'success': 'User Blocked'})


@login_required
def group_inbox(request):
    groupchat = GroupChat.objects.filter(members__in=User.objects.filter(pk=request.user.pk), active=True)
    print("groupchat =============", groupchat)
    context = {
        'groupchat': groupchat,
    }
    return render(request, 'chat/group_inbox.html', context)


@login_required
def group_inbox_detail(request, slug):
    groupchat_list = GroupChat.objects.filter(members__in=User.objects.filter(pk=request.user.pk), active=True)
    groupchat = GroupChat.objects.get(slug=slug, active=True)
    group_messages = GroupChatMessage.objects.filter(groupchat=groupchat).order_by("id")

    if request.user not in groupchat.members.all():
        return redirect("core:join_group_chat_page", groupchat.slug)


    context = {
        'groupchat': groupchat,
        'group_name': groupchat.slug,
        'group_messages': group_messages,
        'groupchat_list': groupchat_list,
    }
    return render(request, 'chat/group_inbox_detail.html', context)

def join_group_chat_page(request, slug):
    groupchat = GroupChat.objects.get(slug=slug, active=True)

    context = {
        'groupchat': groupchat,
    }
    return render(request, 'chat/join_group_chat_page.html', context)


def join_group_chat(request, slug):
    groupchat = GroupChat.objects.get(slug=slug, active=True)

    if request.user in groupchat.members.all():
        return redirect("core:group_inbox_detail", groupchat.slug)
    
    groupchat.members.add(request.user)
    return redirect("core:group_inbox_detail", groupchat.slug)


def leave_group_chat(request, slug):
    groupchat = GroupChat.objects.get(slug=slug, active=True)

    if request.user in groupchat.members.all():
        groupchat.members.remove(request.user)
        return redirect("core:join_group_chat_page", groupchat.slug)

    return redirect("core:join_group_chat_page", groupchat.slug)


def games(request):
    return render(request, 'games/all_games.html')

def stack_brick(request):
    return render(request, 'games/stack_brick.html')

def game_2048(request):
    return render(request, 'games/2048.html')

def game_caro(request):
    return render(request, 'games/caro.html')


def search_users(request):
    query = request.GET.get('q')
    if query:
        users = User.objects.filter(username__icontains=query) | User.objects.filter(email__icontains=query) | User.objects.filter(full_name__icontains=query)

        users_data = []
        for user in users:
            try:
                profile = Profile.objects.get(user=user)
                profile_image = profile.image.url
                full_name = profile.full_name
            except Profile.DoesNotExist:
                profile_image = None
                full_name = None

            user_data = {
                'username': user.username,
                'full_name': full_name,
                'email': user.email,
                'profile_image': profile_image,
            }
            users_data.append(user_data)
    else:
        users_data = []
    return JsonResponse({'users': users_data})




def load_more_posts(request):
    all_posts = Post.objects.filter(active=True, visibility="Everyone").order_by('-date')

    # Paginate the posts
    paginator = Paginator(all_posts, 3)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    posts_data = []
    for post in page_obj:
        post_data = {
            'title': post.title,
            'profile_image': post.user.profile.image.url,
            'full_name': post.user.profile.full_name,
            'image_url': post.image.url if post.image else None,
            'video': post.video.url if post.video else None,
            'id': post.id,
            'id': post.id,
            'likes': post.likes.count(),
            'slug': post.slug,
            'views': post.views,
            'date': timesince(post.date),
        }
        posts_data.append(post_data)

    return JsonResponse({'posts': posts_data})

# trả về trang birthday 
def load_birthday(request):
    return render(request,'core/birthday.html')

def load_create_group(request):
    return render(request,'groups/create-group.html')

#trả về trang pages
def load_pages(request):
    return render(request,'pages/pages.html')
def load_create_page(request):
    return render(request,'pages/create-page.html')

#trả về trang groups
def load_groups(request):
    groups = Group.objects.filter(active=True)
    
    context = {
        "groups":groups
    }
    return render(request,'groups/index.html', context)

def group_detail(request, slug):
    group = get_object_or_404(Group, slug=slug)
    return render(request, 'groups/group-detail.html', {'group': group})

def load_create_group(request):
    return render(request,'groups/create-group.html')

def load_group_profile(request):
    return render(request,'groups/group-detail.html')

@csrf_exempt
def add_group(request):
    if request.method == 'POST':
        name = request.POST.get('group-name')
        topic = request.POST.get('group-topic')
        description = request.POST.get('group-description')
        friend = request.POST.get('group-friend')
        visibility = request.POST.get('visibility')

        print("name ============", name)
        print("topic ============", topic)
        print("description ============", description)
        print("friend ============", friend)
        print("access ============", visibility)

        uuid_key = shortuuid.uuid()
        uniqueid = uuid_key[:4]

        if name and description:
            group = Group(user=request.user, name=name, topic=topic, description=description, visibility=visibility, slug=slugify(name) + "-" + str(uniqueid.lower()))
            group.save()

            if friend:
                friend_ids = [int(num) for num in friend.split(",")] if friend else []
                for id in friend_ids:
                    friend_user = User.objects.get(id=id)
                    group.members.add(friend_user)
            

            return JsonResponse({'group': {
                "group": group,
                "name": group.name,
                "topic": group.topic,
                "description": group.description,
                "date": timesince(group.date),
                "views": group.views,
                "visibility": group.visibility,
            }})
        else:
            return JsonResponse({'error': 'Invalid post data'})

    return JsonResponse({"data":"Sent"})
            
    #         context = {
    #             "group": {
    #                 "name": group.name,
    #                 "description": group.description,
    #                 "date": timesince(group.date),
    #                 "views": group.views,
    #                 "visibility": group.visibility,
    #             }
    #         }

    #         return render(request, 'groups/group-detail.html', context)
    #     else:
    #         return JsonResponse({'error': 'Invalid post data'})
    # else:
    #     return render(request, 'groups/group-detail.html')


@csrf_exempt
def join_group(request):
    user = request.user
    group_id = request.GET.get('id')

    try:
        group = Group.objects.get(id=group_id)
        group.members.add(user)
        # Lấy URL chi tiết nhóm
        group_detail_url = reverse('core:group_detail', kwargs={'slug': group.slug})
        return JsonResponse({'success': 'Sent', 'group_id': group.id, 'group_detail_url': group_detail_url})
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Group not found'}, status=404)


# def increase_group_views(request, slug):
#     group = get_object_or_404(Group, slug=slug)
#     Group.objects.filter(slug=slug).update(views=F('views') + 1)
#     return HttpResponseRedirect(reverse('group_detail', args=[slug]))

def my_group(request, username):
    return render(request,'groups/create-group.html')

# trả về tạo group chat
def load_group_chat(request):
    return render(request, 'chat/create_group_chat.html')

# Xử lý call video
def videoCall(request, username):
    return render(request, 'chat/create_room_call.html')

def getToken(request):
    appId = "be589573195146e999b33c5c5e6dec15"
    appCertificate = "cf64d6ddaeb947b3ab60fe83dd6c3b8c"
    channelName = request.GET.get('channel')
    uid = random.randint(1, 230)
    expirationTimeInSeconds = 3600
    currentTimeStamp = int(time.time())
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)

    return JsonResponse({'token': token, 'uid': uid}, safe=False)


@csrf_exempt
def createMember(request, username):
    data = json.loads(request.body)
    member, created = RoomVideoCall.objects.get_or_create(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )

    return JsonResponse({'name':data['name']}, safe=False)


def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    try:
        member = RoomVideoCall.objects.get(
            uid=uid,
            room_name=room_name,
        )
        name = member.name
        return JsonResponse({'name': member.name}, safe=False)
    except RoomVideoCall.DoesNotExist:
        return JsonResponse({'error': 'Member not found'}, status=404)
    
@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)
    
    try:
        member = RoomVideoCall.objects.get(
            name=data['name'],
            uid=data['UID'],
            room_name=data['room_name']
        )
        member.delete()
        return JsonResponse('Member deleted', safe=False)
    except RoomVideoCall.DoesNotExist:
        return JsonResponse({'error': 'Member not found'}, status=404)