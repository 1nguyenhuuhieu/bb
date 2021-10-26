from django.db import models

# Create your models here.

class Chat(models.Model):
    mess = models.TextField( default='Seen', blank=True, null=True)
    created = models.DateTimeField( auto_now=True)