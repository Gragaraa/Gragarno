from django import forms

from django.contrib.auth.forms import UserCreationForm
from .models import User
class EventForm(forms.Form):
    data = forms.CharField()
    description=forms.CharField()
class MainInfoForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email","password1","password2"]