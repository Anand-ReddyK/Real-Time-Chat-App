from django.urls import path

from . import views

urlpatterns = [
    path('', views.log_in, name="log_in"),
    path('sign-up/', views.sign_up, name="sign_up"),
    path('log_out/', views.log_out, name="log_out"),
    path('user_chats/', views.user_page_view, name="user_chats"),
    path('chat/<int:pk>/', views.messages, name="chat"),
    path('new-friend-request/', views.new_friend_request, name="new-friend-request"),

    path('friend-request/<int:fr_req_id>/<str:fr_req_response>/', views.friend_requests_view, name="friend_request"),

]