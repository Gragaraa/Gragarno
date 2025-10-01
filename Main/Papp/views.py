from django.shortcuts import render,redirect
from . import forms
from . import models
from django.contrib.auth import login
from .models import User
def page(request):
    list_event = models.Event.objects.all()
    data={
    }
    for i in list_event:
        data[i.data]: i.description

    return render(request, 'Papp/htmll.html', data)
def pagereg(request):


    # form=forms.MainInfoForm()
    # if request.method == "POST":
    #     form= forms.MainInfoForm(request.POST)
    #     if form.is_valid():
    #         user=form.save()
    #         print("✅ Пользователь сохранён:", user)
    #         login(request,user)
    #         return redirect("index")

    form=forms.EventForm()
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