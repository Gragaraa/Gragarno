from django import forms
from .models import Income, Expense, Category
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
class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['amount', 'description']

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'category', 'description']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
        }