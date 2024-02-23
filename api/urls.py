from django.urls import path

from . import views


urlpatterns = [
    path('<str:pk>/', views.chatList, name='chat-list'),
    path('length/<str:pk>/', views.chatLenght, name='chat-length'),
]