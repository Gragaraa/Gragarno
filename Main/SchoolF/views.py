from django.shortcuts import render,redirect
from django.http import HttpResponse
from . import forms
from .models import Forum
from django.contrib.auth import get_user_model
User=get_user_model()

def forum(request):
    posts = Forum.objects.all().order_by('-id')
    data={'posts':posts}
    return render(request,'SchoolF/fake.html',data)
def CreateForum(request):

    form=forms.ForumForm()
    if request.method == "POST":
        form= forms.ForumForm(request.POST)

        if form.is_valid():
            user = User.objects.get(username=request.user)
            user.rating+=1
            checkform = form.save(commit=False)
            checkform.usera=request.user

            checkform.save()
            user.save(update_fields=['rating'])
            return redirect("forum")
    data={"form":form}
    return render(request,'SchoolF/CreateForum.html',data)


