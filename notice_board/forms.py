from .models import Message
from django import forms


class AddMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['title', 'body']
