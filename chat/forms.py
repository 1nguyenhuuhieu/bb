from django.forms import ModelForm, Textarea
from django import forms
from .models import *

class ChatForm(ModelForm):
    class Meta:
        model = Chat
        fields = '__all__'
        labels = {
            'mess': ""
        }