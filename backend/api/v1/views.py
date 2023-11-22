"""
Module for creating, configuring and managing `api' app viewsets
"""
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from rest_framework.permissions import SAFE_METHODS
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from users.serializers import ShortRecipeSerializer
from recipes.models import (
    Ingredient,
    Tag,
    Recipe,
    Favorite,
    ShoppingCart,
    IngredientInRecipe
)
from .pagination import CustomPagination
from .permissions import IsAuthorOrReadOnly
from .utils import convert_txt
from .filters import IngredientFilter, RecipeFilter
from .serializers import (
    IngredientSerializer,
    TagSerializer,
    RecipeReadSerializer,
    RecipeCreateUpdateSerializer,
)


class IngredientViewSet(ReadOnlyModelViewSet):
    """Viewset for 'ingredients' model."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class TagViewSet(ReadOnlyModelViewSet):
    """Viewset for 'tags' model."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(ModelViewSet):
    """Viewset for 'Recipes' model."""

    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        """Selecting a serializer class depending on the request."""
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer

        return RecipeCreateUpdateSerializer

    def perform_create(self, serializer):
        """
        Automatically saves the recipe author
        when creating a new recipe.
        """
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """
        Automatically saves the recipe author
        when updating a recipe.
        """
        serializer.save(author=self.request.user)

    def add_recipe(self, model, request, pk):
        """Adds recipes to the list."""
        user = self.request.user
        if not Recipe.objects.filter(id=pk).exists():
            return Response(
                'There is no such recipe.',
                status=status.HTTP_400_BAD_REQUEST
            )
        recipe = Recipe.objects.get(id=pk)
        recipe_in_list = model.objects.filter(recipe=recipe, user=user)
        if recipe_in_list.exists():
            return Response(
                {'error': 'The recipe has already been added to list.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        model.objects.create(recipe=recipe, user=user)
        serializer = ShortRecipeSerializer(recipe)
        return Response(
            data=serializer.data, status=status.HTTP_201_CREATED
        )

    def delete_recipe(self, model, request, pk):
        """Removes recipes from the list."""
        recipe = get_object_or_404(Recipe, pk=pk)
        user = self.request.user
        recipe_in_list = model.objects.filter(recipe=recipe, user=user)
        if recipe_in_list.exists():
            recipe_in_list.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'error': 'You are trying to delete a recipe that does not exist.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk=None):
        """
        Depending on the method,
        adds or removes a recipe from favorites.
        """
        if request.method == 'POST':
            return self.add_recipe(Favorite, request, pk)
        if request.method == 'DELETE':
            return self.delete_recipe(Favorite, request, pk)

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        """
        Depending on the method,
        adds or removes a recipe from the shopping list.
        """
        if request.method == 'POST':
            return self.add_recipe(ShoppingCart, request, pk)
        if request.method == 'DELETE':
            return self.delete_recipe(ShoppingCart, request, pk)

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        """Downloads a shopping list."""
        ingredients = IngredientInRecipe.objects.filter(
            recipe__shopping_cart__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).order_by(
            'ingredient__name'
        ).annotate(ingredient_total=Sum('amount'))

        return convert_txt(ingredients)
