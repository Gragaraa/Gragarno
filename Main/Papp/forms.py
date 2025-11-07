from django import forms

from django.contrib.auth.forms import UserCreationForm
from .models import User, Product


class EventForm(forms.Form):
    data = forms.CharField(max_length=10)
    description=forms.CharField(max_length=10)

class MainInfoForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email","password1","password2"]
