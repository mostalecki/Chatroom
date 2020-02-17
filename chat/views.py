from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Room, Connection

# Create your views here.

def homepage(request):
    ''' Main page '''
    rooms = Room.objects.filter(is_private=False)
    return render(request, 'chat/home.html', {'rooms':rooms})

def room(request, room_name):
    ''' Page of a chatroom'''

    return render(request, 'chat/room.html', {'room_name': room_name})