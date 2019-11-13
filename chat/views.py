from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import json
from chat.models import ChatGroup, Message, serialize_user


def index(request):
    return render(request, 'chat/index.html', {})


def user_list(request):
    users = User.objects.all()
    return render(request, 'chat/user_list.html', {"users": users})


def room(request, room_name):
    user1 = request.user
    user2 = User.objects.get(username=room_name)
    unique_uri = ChatGroup.get_unique_uri(user1, user2)
    messages = Message.get_conversation(sender=user1, receiver=user2)
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(unique_uri)),
        "receiver": mark_safe(json.dumps(serialize_user(user2))),
        "sender": mark_safe(json.dumps(serialize_user(user1))),
        "chat_with": user2.username,
        "messages": messages
    })


def login_view(request):
    if request.method == 'POST':
        data = request.POST
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("user-list")
        else:
            error = "Invalid Credentials"
            return render(request, 'chat/login.html', {"error": error})
    else:
        return render(request, 'chat/login.html', {})


def logout_view(request):
    login(request)
    return redirect("user-list")
