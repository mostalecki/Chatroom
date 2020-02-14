from django.shortcuts import render
#from django.contrib.auth.decorators import login_required

# Create your views here.

def homepage(request):
    ''' Main page '''

    return render(request, 'chat/home.html')

def room(request, room_name):
    ''' Page of a chatroom'''

    return render(request, 'chat/room.html', {'room_name': room_name})