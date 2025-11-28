from django import forms

from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import User
class register(UserCreationForm):
    class Meta:
        model= User
        fields=['username','password1','password2']
class loginf(AuthenticationForm):
    class Meta:
        model=User
        fields=['username','password']