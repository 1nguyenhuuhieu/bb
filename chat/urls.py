from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('fcAS6keJhH/', views.doctruyen, name='doctruyen'),
    path('dangxuat/', views.logout_view, name='dangxuat'),
    path('zcO2LK8Due/<int:id>', views.xemvideo, name='xemvideo'),
]
