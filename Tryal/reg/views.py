from django.shortcuts import render
def home(request):
    if request.user.is_authenticated:
        pass
    else:
        return render(request,"reg/home.html")
def login(request):
    return render(request,"reg/login.html")
def reg(request):

    return render(request,"reg/registrate.html")
# Create your views here.
