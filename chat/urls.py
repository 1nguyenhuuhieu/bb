from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('fcAS6keJhH/', views.doctruyen, name='doctruyen'),
    path('dangxuat/', views.logout_view, name='dangxuat'),
    path('chat/', views.chat_list, name='chat_realtime'),
    path('last_sender/', views.last_sender),
    path('ajaxChat/', views.ajax_chat, name='ajaxChat'),

]
