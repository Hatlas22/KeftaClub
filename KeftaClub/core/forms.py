from .models import *
from django import forms

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'w-full px-0 text-sm text-gray-900 bg-white border-0 dark:bg-gray-800 focus:ring-0 dark:text-white dark:placeholder-gray-400',
                'placeholder': 'Enter your comment...'
            }),
        }


class ThreadForm(forms.Form):
    username = forms.CharField(label='', max_length=100)

class MessageForm(forms.ModelForm):
    body = forms.CharField(label='', max_length=1000)

    image = forms.ImageField(required=False)

    class Meta:
        model = MessageModel
        fields = ['body', 'image']

    