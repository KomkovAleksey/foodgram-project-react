"""
Module for "users" app routes
"""
from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet

# foodgram router_v1 users v.1
router_v1 = DefaultRouter()


router_v1.register('users', CustomUserViewSet, basename='users')

urlpatterns = [
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
