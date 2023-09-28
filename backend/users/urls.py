"""
Module for 'users' app routes
"""
from django.urls import include, path

from rest_framework.routers import SimpleRouter

from .views import SubscribeViewSet

app_name = 'users'

router_v1 = SimpleRouter()

# foodgram router_v1 users v.1

router_v1.register(
    'users/<int:pk>/subscribe/', SubscribeViewSet, basename='subscribe'
    )

urlpatterns = [
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
