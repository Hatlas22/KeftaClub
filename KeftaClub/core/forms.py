from .models import *
from django import forms

class CommentForm(forms.ModelForm):
    comment = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows': '3',
            'placeholder': 'Say Something...'
            }))

    class Meta:
        model = PostComment
        fields = ['comment']

class ThreadForm(forms.Form):
    username = forms.CharField(label='', max_length=100)

class MessageForm(forms.ModelForm):
    body = forms.CharField(label='', max_length=1000)

    image = forms.ImageField(required=False)

    class Meta:
        model = MessageModel
        fields = ['body', 'image']

    