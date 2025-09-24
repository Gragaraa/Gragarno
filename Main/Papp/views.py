from django.shortcuts import render,redirect
from . import forms
from . import models
from django.contrib.auth import login
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
            user=form.save
            login(request,user)
            return redirect("index")
    data={
        "form":form
    }
    return render(request, 'Papp/reg.html', data)