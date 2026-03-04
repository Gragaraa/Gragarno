from django import forms
from .models import ForumPost

class PostForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Заголовок темы'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Текст сообщения...', 'rows': 5}),
        }
from .models import Comment

