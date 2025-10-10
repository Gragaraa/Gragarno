from django.shortcuts import render,redirect
from django.http import HttpResponse
from . import forms
from .models import Forum


def forum(request):
    posts = Forum.objects.all().order_by('-id')
    data={'posts':posts}
    return render(request,'SchoolF/fake.html',data)
def CreateForum(request):
    form=forms.ForumForm()
    if request.method == "POST":
        form= forms.ForumForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("forum")
    data={"form":form}
    return render(request,'SchoolF/CreateForum.html',data)


