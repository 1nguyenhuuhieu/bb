from django.contrib import admin
from .models import *
# Register your model here.

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    pass

@admin.register(Typing)
class TypingAdmin(admin.ModelAdmin):
    pass
