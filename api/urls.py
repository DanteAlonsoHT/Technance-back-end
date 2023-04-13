from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from .views import UserViewSet
from api import views

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]
