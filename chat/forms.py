from django.forms import ModelForm
from django import forms
from .models import *

class ChatForm(ModelForm):
    class Meta:
        model = Chat
        fields = '__all__'
        widgets = {
            'file': forms.FileInput(
                attrs={
                    'class': 'form-control form-control-sm'
                }
            ),
            'video': forms.FileInput(
                attrs={
                    'class': 'form-control form-control-sm'
                }
            )

        }