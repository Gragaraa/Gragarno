from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth import login, authenticate, logout
def home(request):
    return render(request,'reg/home.html')
def reg(request):
    form=forms.register()
    if request.method=="POST":
        form=forms.register(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('home')
    data={ 'form':form}
    return render(request, 'reg/reg.html',data)
def flogin(request):
    form=forms.loginf()
    if request.method=="POST":
        form=forms.loginf(request,data=request.POST)
        if form.is_valid():
            username=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password")
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
    data={"form":form}
    return render(request,'reg/login.html',data)
def flogout(request):
    logout(request)
    return redirect("home")
# Create your views here.
