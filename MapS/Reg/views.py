from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import UserRegisterForm


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация успешна!")
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'Reg/Register.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Вы вошли как {username}.")
                return redirect('home')
            else:
                messages.error(request, "Неверный логин или пароль.")
        else:
            messages.error(request, "Неверный логин или пароль.")

    form = AuthenticationForm()
    return render(request, 'Reg/Login.html', {'form': form})



def logout_view(request):
    logout(request)
    messages.info(request, "Вы вышли из аккаунта.")
    return redirect('home')