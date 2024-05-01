from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from userauths.models import User, Profile
from userauths.forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm
from core.models import FriendRequest, Post, Group


def RegisterView(request, *args, **kwargs):
    if request.user.is_authenticated:
        messages.warning(request, f"Người dùng {request.user.username} đã đăng nhập ")
        return redirect('core:feed')   

    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        form.save()
        full_name = form.cleaned_data.get('full_name')
        phone = form.cleaned_data.get('phone')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')

        user = authenticate(email=email, password=password)
        login(request, user)

        messages.success(request, f"Xin chào {request.user.username}, tài khoản của bạn đã đươc tạo thành công.")

        profile = Profile.objects.get(user=request.user)
        profile.full_name = full_name
        profile.phone = phone
        profile.save()

        return redirect('core:feed')
    
    context = {'form':form}
    return render(request, 'userauths/sign-up.html', context)

def LoginView(request):
    # if request.user.is_authenticated:
    #     return redirect('core:feed')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Đăng nhập thành công")
                return redirect('core:feed')
            else:
                messages.error(request, 'Username hoặc mật khẩu không dúng')
        except:
            messages.error(request, 'Người dùng không tồn tại')
    return HttpResponseRedirect("/")

def LogoutView(request):
    logout(request)
    messages.success(request, 'Đăng xuất thành công')
    return redirect("userauths:sign-in")


@login_required
def my_profile(request):
    profile = request.user.profile
    posts = Post.objects.filter(active=True, user=request.user)
    groups = Group.objects.filter(active=True, user=request.user)

    context = {
        "posts":posts,
        "groups": groups,
        "profile":profile,
    }
    return render(request, "userauths/my-profile.html", context)


@login_required
def friend_profile(request, username):
    profile = Profile.objects.get(user__username=username)
    posts = Post.objects.filter(active=True, user=profile.user)

    # Send Friend Request Feature
    bool = False
    bool_friend = False

    sender = request.user
    receiver = profile.user
    bool_friend = False
    print("========================  Thêm hoặc hủy")
    try:
        friend_request = FriendRequest.objects.get(sender=sender, receiver=receiver)
        if friend_request:
            bool = True
        else:
            bool = False
    except:
        bool = False
    # if receiver not in sender.profile.friends.all():
    #     pass
    # else:
    #     print("========================  Unfriend")
    #     bool_friend = False

    # End Send Friend Request Feature
    print("Bool =======================", bool)
    

    context = {
        "posts":posts,
        "bool_friend":bool_friend,
        "bool":bool,
        "profile":profile,
    }
    return render(request, "userauths/friend-profile.html", context)


@login_required
def profile_update(request):
    if request.method == "POST":
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        u_form = UserUpdateForm(request.POST, instance=request.user)

        if p_form.is_valid() and u_form.is_valid():
            p_form.save()
            u_form.save()
            messages.success(request, "Hồ sơ đã được cập nhật thành công")
            return redirect('userauths:profile-update')
    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)
        u_form = UserUpdateForm(instance=request.user)

    context = {
        'p_form': p_form,
        'u_form': u_form,
    }
    return render(request, 'userauths/profile-update.html', context)

