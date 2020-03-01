from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.core.files.storage import default_storage
from .forms import UserCreationForm, UserProfileForm
from .models import UserProfile

# Create your views here.

def register(request):
    ''' Used to register users'''

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'New user created: {username}')
            return redirect('home')
        else:
            for msg in form.error_messages:
                messages.error(request, f'{msg}')

    form = UserCreationForm()
    return render(request, 'users/register.html', {'form':form})


def login_user(request):
    ''' Used to log users in '''

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid username or password')

    form = AuthenticationForm
    return render(request, 'users/login.html', {'form':form})


def logout_user(request):
    ''' Used to log users out'''

    logout(request)
    return redirect('login')

def user_profile(request, username):
    ''' '''
    profile = get_object_or_404(UserProfile, user__username=username)

    context = {}

    if request.user.is_authenticated:
        user = request.user
        if user.username == username:
            if request.method == "POST":
                form = UserProfileForm(request.POST, request.FILES, instance=profile)
                # avatar images are written to drive here because 
                # for some reason django does not want to save them
                avatar = request.FILES['avatar']
                with open(f'static/{profile.avatar}', 'wb+') as destination:
                    for chunk in avatar.chunks():
                        destination.write(chunk)

            form = UserProfileForm()
            context['form'] = form

    context['username'] = profile.user.username
    context['avatar_url'] = profile.avatar.url
    
    return render(request, 'users/profile.html', context)


