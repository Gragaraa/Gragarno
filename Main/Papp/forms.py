from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
class EventForm(forms.Form):
    data = forms.CharField()
    description=forms.CharField()
class MainInfoForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email","password1","password2"]