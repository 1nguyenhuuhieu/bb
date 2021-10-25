from django.forms import ModelForm

from .models import *

class ChatForm(ModelForm):
    class Meta:
        model = Chat
        fields = '__all__'
        label=False