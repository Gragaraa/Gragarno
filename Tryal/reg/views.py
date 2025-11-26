from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from . import forms


def home(request):
    if request.user.is_authenticated:

        return render(request, "reg/home.html", {"logged_in": True})
    else:

        return render(request, "reg/home.html", {"logged_in": False})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Неверное имя пользователя или пароль.")
    else:
        form = AuthenticationForm()
    return render(request, 'reg/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')


def reg(request):
    if request.method == "POST":
        form = forms.Registerform(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = forms.Registerform()
    return render(request, "reg/registrate.html", {'form': form})

