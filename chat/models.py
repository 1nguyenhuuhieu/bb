from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.db.models.fields.related import OneToOneField

class Chat(models.Model):
    sender = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    mess = models.TextField( default='Seen', blank=True, null=True)
    created = models.DateTimeField( auto_now=True)
    file = models.ImageField(upload_to='x_files/',blank=True)