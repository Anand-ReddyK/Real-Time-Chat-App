from django.urls import path

from . import views

urlpatterns = [
    path('', views.log_in, name="log_in"),
    path('sign-up/', views.sign_up, name="sign_up"),
    path('user_chats/', views.user_page_view, name="user_chats"),
    path('chat/<int:pk>/', views.messages, name="chat"),
    path('new-chat/', views.new_chat, name="new-chat"),
]