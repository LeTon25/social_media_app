from django.urls import path 
from core import views 

app_name = "core"

urlpatterns = [
    path("", views.index, name="feed"),
    path("post/<slug:slug>/", views.post_detail, name="post-detail"),

    # Chat Feature
    path("core/inbox/", views.inbox, name="inbox"),
    path("core/inbox/<username>/", views.inbox_detail, name="inbox_detail"),

    # Group Chát
    path("core/group-inbox/", views.group_inbox, name="group_inbox"),
    path("core/group-inbox/<slug:slug>/", views.group_inbox_detail, name="group_inbox_detail"),

    # Join & leave Group
    path("core/join-group-page/<slug:slug>/", views.join_group_chat_page, name="join_group_chat_page"),
    path("core/join-group/<slug:slug>/", views.join_group_chat, name="join_group"),
    path("core/leave-group/<slug:slug>/", views.leave_group_chat, name="leave_group_chat"),

    # Games
    path("core/all-games/", views.games, name="games"),
    path("core/stack_brick/", views.stack_brick, name="stack_brick"),
    path("core/game_2048/", views.game_2048, name="game_2048"),
    path("core/game_caro/", views.game_caro, name="game_caro"),

    # Search
    path('search/', views.search_users, name='search_users'),

    # Load more post
    path('load_more_posts/', views.load_more_posts, name='load_more_posts'),

    # Birthday
    path('birthdays/',views.load_birthday,name="birthdays"),

    #Group
    path('groups/',views.load_groups,name="groups"),
    path('groups/create-group',views.load_create_group,name="create-group-page"),
    path('groups/<slug:slug>/', views.group_detail, name='group_detail'),   
    # path('group/<slug:slug>/view', views.increase_group_views, name='increase_group_views'),

    #Pages
    path('pages/',views.load_pages,name='pages'),
    path('pages/create-page',views.load_create_page,name="create-page-page"),

    # Video call
    path('core/inbox/<username>/video/', views.videoCall),
    path('get_token/', views.getToken),

    path('core/inbox/<username>/video/create_member/', views.createMember),
    path('get_member/', views.getMember),
    path('delete_member/', views.deleteMember),

    #Group
    path('group_chat/',views.load_group_chat,name="group_chat"),
    # path('group_chat/create-group',views.load_create_group,name="group_chat-page"),

    # Ajax URLs
    path("create-post/", views.create_post, name="create-post"),
    path("delete-post/", views.delete_post, name="delete-post"),
    path("edit-post/", views.edit_post, name="edit-post"),
    path("get-post/", views.get_post, name="get-post"),
    path("like-post/", views.like_post, name="like-post"),
    path("comment-post/", views.comment_on_post, name="comment-post"),
    path("like-comment/", views.like_comment, name="like-comment"),
    path("reply-comment/", views.reply_comment, name="reply-comment"),
    path("delete-comment/", views.delete_comment, name="delete-comment"),
    path("add-friend/", views.add_friend, name="add-friend"),
    path("accept-friend-request/", views.accept_friend_request, name="accept-friend-request"),
    path("reject-friend-request/", views.reject_friend_request, name="reject-friend-request"),
    path("unfriend/", views.unfriend, name="unfriend"),
    path("block-user/", views.block_user, name="block_user"),
    path('add-group/',views.add_group,name="add-group"),
    path('groups/my-group/<username>',views.my_group,name="my-group"),
    path("join-group/", views.join_group, name="join-group"),

]