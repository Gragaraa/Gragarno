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
from django import forms
from .models import Comment, ForumPost

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Напишите что-нибудь...',
                'rows': 3,
                'style': 'width: 100%; border-radius: 10px; padding: 10px; border: 1px solid #ddd;'
            }),
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = ['title', 'content', 'image']