from django.shortcuts import render, redirect
from django.http import JsonResponse
import json

from . import models
# Create your views here.

def log_in(request):
    user_exist = 0
    if request.method == "POST":
        username = request.POST["name"]
        if models.User.objects.filter(name=username).exists():
            request.session['user'] = username

            return redirect('user_chats')
        else:
            user_exist = 1
    
    context = {
        'user_ex_log': user_exist
    }
    return render(request, 'chat/index.html', context)



def sign_up(request):
    user_exist = 0

    if request.method == "POST":
        username = request.POST["name"]
        try:
            models.User.objects.create(name=username)
            request.session['user'] = username

            return redirect('user_chats')
        except Exception as e:
            user_exist = 1
            
        # print(request.POST)
    
    context = {
        "user_ex": user_exist
    }

    return render(request, "chat/index.html", context)



def user_page_view(request):
    username = request.session.get('user')
    user = models.User.objects.get(name=username)
    chats = models.SingleChat.objects.filter(members__in=[user.id])

    context = {
        "chats": chats,
        "username": username
    }

    return render(request, 'chat/user_page2.html', context)


def createNewMessage(message, conversation_id, user):
    conversation = models.SingleChat.objects.get(id=conversation_id)
    new_message = models.Messages.objects.create(
        conversation=conversation, 
        content=message,
        created_by = models.User.objects.get(name=user)
    )

    item = {}
    item['message'] = new_message.content
    item['created_by'] = new_message.created_by.name
    item['created_at'] = new_message.created_at.strftime("%b. %d, %Y, %I:%M %p")

    return item



def messages(request, pk):
    conversation = models.SingleChat.objects.get(id=pk)
    user = request.session['user']

    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        mess = data.get('message', '')

        if mess:
            message_json = createNewMessage(mess, pk, user)

            return JsonResponse(message_json)
    
    context = {
        "conversation": conversation,
        "user": models.User.objects.get(name=request.session['user']),
        "chat_id": pk
    }

    return render(request, "chat/messages.html", context)



def new_chat(request):
    users = models.User.objects.all().exclude(name=request.session['user'])

    if request.method == 'POST' and request.POST.getlist('selected_users'):

        chat_object = models.SingleChat()
        chat_object.save()

        for user_id in request.POST.getlist('selected_users'):
            chat_object.members.add(int(user_id))
        
        created_user = models.User.objects.get(name=request.session['user'])
        chat_object.members.add(created_user)
        
        return redirect('user_chats')

    context = {
        "users": users
    }

    return render(request, "chat/create_chat.html", context)
