from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class UserRegisterForm(UserCreationForm):

    email = forms.EmailField(required=True, label="Email")

    class Meta(UserCreationForm.Meta):
        model = User

        fields = ("username", "email", "first_name", "last_name")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'avatar', 'bio']