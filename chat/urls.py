from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('fcAS6keJhH/', views.doctruyen, name='doctruyen'),
    path('dangxuat/', views.logout_view, name='dangxuat'),
    path('zcO2LK8Due/<int:id>', views.xemvideo, name='xemvideo'),
    path('FBn0XShVss/', views.photos, name='photos'),
    path('getM/', views.getM, name='getM'),
]
