from django.shortcuts import render,redirect
from . import forms
from . import models
from django.contrib.auth import login, authenticate, logout
from .models import User
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.cache import never_cache
@never_cache
def page(request):
    list_event = models.Event.objects.all()
    data={
    }
    for i in list_event:
        data[i.data]: i.description

    return render(request, 'Papp/htmll.html', data)

def pagereg(request):


    form=forms.MainInfoForm()
    if request.method == "POST":
        form= forms.MainInfoForm(request.POST)
        if form.is_valid():

            user=form.save(commit=False)
            user.rating=0
            user.save()
            print("✅ Пользователь сохранён:", user)
            login(request,user)
            return redirect("index")


    data={
        "form":form
    }

    return render(request, 'Papp/reg.html', data)
def show_users(request):
    users = User.objects.all()
    data = {
        'users': users
    }
    return render(request, 'Papp/users.html', data)


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

                return redirect('index')
    else:
        form = AuthenticationForm()

    return render(request, 'Papp/login.html', {'form': form})
def user_logout(request):
    logout(request)
    return redirect('index')
def leader(request):
    users=User.objects.order_by('-rating')[:10]
    data={
        'users':users
    }

    return  render(request,'Papp/leaderboard.html',data)