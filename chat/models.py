from django.db import models

# Create your models here.

class Chat(models.Model):
    mess = models.CharField(max_length=1000)
    created = models.DateTimeField( auto_now_add=True)