from django.contrib import admin
from .models import *
# Register your model here.


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    pass

@admin.register(NewArtile)
class NewArtileAdmin(admin.ModelAdmin):
    pass
