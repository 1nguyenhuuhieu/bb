from django.contrib.auth.models import User
from .models import *
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username']

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['sender', 'created', 'mess', 'file', 'video', 'id']

class LastSenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['sender']
