"""
URL configuration for "api" app.
"""
from django.urls import include, path
from rest_framework import routers

from .views import (
    IngredientsViewSet,
    RecipeViewSet,
    TagViewSet,
)


router_v1 = routers.DefaultRouter()

router_v1.register("tags", TagViewSet, basename='tags')
router_v1.register("recipes", RecipeViewSet, basename='recipes')
router_v1.register("ingredients", IngredientsViewSet, basename='ingredients')


urlpatterns = [
    path("", include(router_v1.urls)),
    path("", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
]
