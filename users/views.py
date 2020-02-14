from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

# Create your views here.

def register(request):
    ''' Used to register users'''

    if request.user.is_authenticated:
        return redirect('chat:home')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'New user created: {username}')
            return redirect('chat:home')
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
    


