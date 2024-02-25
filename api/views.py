from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

from chat.models import Room
from .serializers import SingleChatSerializer

# Create your views here.

@api_view(['GET'])
def chatList(request, pk):
    chats = Room.objects.get(id=pk)

    chat_json = []

    for message in chats.conversation.all():
        item = {}
        item['message'] = message.content
        item['created_by'] = message.created_by.name
        item['created_at'] = message.created_at.strftime("%b. %d, %Y, %I:%M %p")

        chat_json.append(item)

    return Response(chat_json)


@api_view(['GET'])
def chatLenght(request, pk):
    chats = Room.objects.get(id=pk)

    length = len(chats.conversation.all())

    response = [length]

    return Response(response)

