from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from .models import User
import random
from django.core.mail import send_mail
from django.template.loader import render_to_string


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Пока не подтвердит код, зайти не сможет

            # Генерируем 6-значный код
            code = str(random.randint(100000, 999999))
            user.verification_code = code
            user.save()

            # Отправка письма
            subject = 'Код подтверждения MapS'
            html_message = render_to_string('Reg/verification_email.html', {
                'user': user,
                'code': code
            })

            send_mail(
                subject,
                f'Твой код: {code}',  # Текст для простых клиентов
                'noreply@maps.com',
                [user.email],
                html_message=html_message  # Красивая HTML-версия
            )

            # Сохраняем ID пользователя в сессии, чтобы знать, кого проверять на следующей странице
            request.session['unverified_user_id'] = user.id
            messages.info(request, "Код подтверждения отправлен на почту!")
            return redirect('verify_code')  # Мы создадим этот путь следующим шагом
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


def verify_code_view(request):

    user_id = request.session.get('unverified_user_id')

    if not user_id:
        return redirect('register')

    if request.method == 'POST':
        code_entered = request.POST.get('code')
        try:
            user = User.objects.get(id=user_id)
            if user.verification_code == code_entered:
                user.is_active = True
                user.is_verified = True
                user.save()

                login(request, user)
                del request.session['unverified_user_id']

                messages.success(request, "Почта подтверждена! Добро пожаловать.")
                return redirect('home')
            else:
                messages.error(request, "Неверный код. Попробуй еще раз.")
        except User.DoesNotExist:
            return redirect('register')

    return render(request, 'Reg/verify_code.html')


def password_reset_request_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            # Генерируем новый код
            code = str(random.randint(100000, 999999))
            user.verification_code = code
            user.save()

            # Отправляем письмо в Mailtrap
            subject = 'Сброс пароля MapS'
            html_message = render_to_string('Reg/reset_password_email.html', {
                'user': user,
                'code': code
            })
            send_mail(subject, f'Код для сброса: {code}', 'noreply@maps.com', [user.email], html_message=html_message)

            request.session['reset_user_id'] = user.id
            messages.info(request, "Код для сброса пароля отправлен на почту.")
            return redirect('password_reset_confirm_code')
        except User.DoesNotExist:
            messages.error(request, "Пользователь с такой почтой не найден.")

    return render(request, 'Reg/password_reset_form.html')


def password_reset_confirm_view(request):
    user_id = request.session.get('reset_user_id')
    if not user_id:
        return redirect('password_reset_request')

    if request.method == 'POST':
        code_entered = request.POST.get('code')
        new_password = request.POST.get('password')

        try:
            user = User.objects.get(id=user_id)
            if user.verification_code == code_entered:
                user.set_password(new_password)  # Хэшируем пароль
                user.verification_code = None  # Сбрасываем код
                user.save()

                del request.session['reset_user_id']
                messages.success(request, "Пароль успешно изменен! Теперь войди.")
                return redirect('login')
            else:
                messages.error(request, "Неверный код.")
        except User.DoesNotExist:
            return redirect('password_reset_request')

    return render(request, 'Reg/password_reset_confirm.html')