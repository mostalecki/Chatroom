from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.db import IntegrityError
from .models import Room
from .forms import RoomForm

# Create your views here.


def homepage(request):
    """ Main page """

    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            try:
                room = form.save()
                name = form.cleaned_data["name"]
                return redirect(reverse("room", kwargs={"room_name": name}))

            # Occurs when room with that name already exists in database
            except IntegrityError:
                messages.error(
                    request,
                    f"Room named {form.cleaned_data.get('name')} already exists",
                )
        else:
            print(form.errors)

    rooms = Room.objects.filter(is_private=False)
    return render(request, "chat/home.html", {"rooms": rooms, "form": form})


def room(request, room_name):
    """ Page of a chatroom"""

    if Room.objects.filter(name=room_name).exists():
        return render(request, "chat/room.html", {"room_name": room_name})

    messages.error(request, f"Room {room_name} not found")
    return redirect("home")
