from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from .models import User

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


@login_required
def profile_view(request, user_id=None):
    if user_id:
        target_user = get_object_or_404(User, id=user_id)
    else:
        target_user = request.user


    is_own_profile = (target_user == request.user)

    if request.method == "POST" and is_own_profile:
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль успешно сохранен!")
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=target_user)

    return render(request, 'Reg/Profile.html', {
        'target_user': target_user,
        'form': form,
        'is_own_profile': is_own_profile
    })
