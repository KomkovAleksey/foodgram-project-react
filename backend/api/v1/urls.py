"""
Module for 'api' app routes
"""
from rest_framework.routers import SimpleRouter

from django.urls import include, path

from .views import IngredientViewSet, TagViewSet, RecipeViewSet

app_name = 'api'

router_v1 = SimpleRouter()

# foodgram router_v1 API v.1

router_v1.register('tags', TagViewSet, basename='tags')
router_v1.register('ingredients', IngredientViewSet, basename='ingredients')
router_v1.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
