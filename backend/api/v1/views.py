"""
Module for creating, configuring and managing `api' app viewsets
"""
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from .filters import IngredientFilter, RecipeFilter
from recipes.models import Ingredient, Tag, Recipe
from .serializers import (IngredientSerializer,
                          TagSerializer,
                          RecipeReadSerializer,
                          RecipeCreateUpdateSerializer,
                          )


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """ Viewset for 'ingredients' model. """

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientFilter


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """ Viewset for 'tags' model. """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """ Viewset for 'Recipes' model. """

    queryset = Recipe.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        """ Selecting a serializer class depending on the request. """
        if self.action in ('list', 'retrieve'):
            return RecipeReadSerializer

        return RecipeCreateUpdateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)
