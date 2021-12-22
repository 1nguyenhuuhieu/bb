from django.urls import path, include
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)



urlpatterns = [
    path('', views.index, name='index'),
    path('api/', include(router.urls)),
    path('fcAS6keJhH/', views.doctruyen, name='doctruyen'),
    path('dangxuat/', views.logout_view, name='dangxuat'),
    path('zcO2LK8Due/<int:id>', views.xemvideo, name='xemvideo'),
    path('FBn0XShVss/', views.photos, name='photos'),
]
