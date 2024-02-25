from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import json

from django.views.decorators.http import require_POST

from . import models
# Create your views here.


def login_required(func):
    def wrapper(request, *args, **kwargs):
        if 'user' not in request.session:
            return redirect('log_in')  

        return func(request, *args, **kwargs)

    return wrapper


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


def log_out(request):
    del request.session['user']

    return redirect('log_in')


@login_required
@require_POST
def friend_requests_view(request, fr_req_id, fr_req_response):
    user_name = request.session["user"]
    user = models.User.objects.get(name=user_name)
    friend_request = models.FriendRequest.objects.get(id=fr_req_id)

    # for not letting any random user access all friend requests
    if friend_request.to_user == user and not models.Room.objects.filter(members=friend_request.from_user.id).filter(members=friend_request.to_user.id).exists():

        if fr_req_response == "accept":
            chat_object = models.Room()
            chat_object.save()

            user.friends.add(friend_request.from_user)
            chat_object.members.add(friend_request.from_user)
            chat_object.members.add(friend_request.to_user)
            

        
        friend_request.delete()

        return JsonResponse({'message': 'Friend request handled successfully'})
    
    return HttpResponse(status=403)



@login_required
def user_page_view(request):
    username = request.session.get('user')
    user = models.User.objects.get(name=username)
    chats = models.Room.objects.filter(members__in=[user.id])
    friend_requests = models.FriendRequest.objects.filter(to_user=user)

    context = {
        "friend_requests": friend_requests,
        "chats": chats,
        "username": username,
        "user": user
    }

    return render(request, 'chat/user_page2.html', context)

# --------------------------Not a view--------------------------------------
def createNewMessage(message, conversation_id, user):
    conversation = models.Room.objects.get(id=conversation_id)
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
#---------------------------------------------------------------------------------


@login_required
def messages(request, pk):
    conversation = models.Room.objects.get(id=pk)
    user = models.User.objects.get(name=request.session['user'])
    friend_requests = models.FriendRequest.objects.filter(to_user=user)

    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        mess = data.get('message', '')

        if mess:
            message_json = createNewMessage(mess, pk, user)

            return JsonResponse(message_json)
    
    context = {
        "friend_requests": friend_requests,
        "conversation": conversation,
        "user": user,
        "chat_id": pk
    }

    return render(request, "chat/messages.html", context)


@login_required
def new_friend_request(request):
    user = models.User.objects.get(name=request.session['user'])
    incorrect_username = 0
    error = 0

    if request.method == 'POST' and request.POST.get('selected_user'):

        if(models.User.objects.filter(name=request.POST.get('selected_user')).exists()):

            to_user = models.User.objects.get(name=request.POST.get('selected_user'))

            if models.FriendRequest.objects.filter(from_user=user, to_user=to_user).exists():
                models.FriendRequest.objects.get(from_user=user, to_user=to_user).delete()
            

            try:
                friend_request_object = models.FriendRequest.objects.create(
                    from_user=user,
                    to_user=to_user
                )
            
                friend_request_object.save()

                return redirect('user_chats')

            except Exception as e:
                error = e

        else:
            incorrect_username = 1

    context = {
        "incorrect_username": incorrect_username,
        "error": error
    }

    return render(request, "chat/create_friend_request.html", context)
