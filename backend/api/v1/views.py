"""
Module for creating, configuring and managing `api' app viewsets
"""
from datetime import datetime

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum
from djoser.views import UserViewSet
from rest_framework.permissions import SAFE_METHODS
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from recipes.models import (
    Ingredient,
    Tag,
    Recipe,
    Favorite,
    ShoppingCart,
    IngredientInRecipe
)
from users.models import Follow
from .pagination import CustomPagination
from .permissions import IsAuthorOrReadOnly, IsAdminUserOrReadOnly
from .filters import IngredientFilter, RecipeFilter
from .serializers import (
    ShortRecipeSerializer,
    IngredientSerializer,
    TagSerializer,
    RecipeReadSerializer,
    RecipeCreateUpdateSerializer,
    CustomUserSerializer,
    SubscriptionSerializer,
)

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    """Vievset for working with users."""

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = CustomPagination
    permission_classes = (IsAdminUserOrReadOnly,)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated],
    )
    def subscriptions(self, request):
        subscribed_to = self.paginate_queryset(
            User.objects.filter(following__user=request.user)
        )
        serializer = SubscriptionSerializer(
            subscribed_to,
            many=True,
            context={"request": request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated],
    )
    def subscribe(self, request, id):
        author = get_object_or_404(User, pk=id)
        Subscription = Follow.objects.filter(user=request.user, author=author)

        if request.method == 'POST':
            serializer = SubscriptionSerializer(
                author, data=request.data, context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            if Subscription.exists():
                return Response(
                    {'subscribe': 'You are already subscribed to this user.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if request.user == author:
                return Response(
                    {'subscribe': "You can't subscribe to yourself."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            Follow.objects.create(user=request.user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if not Subscription.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        Subscription.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        """View subscriptions to authors. My subscriptions."""
        user = request.user
        serializer = CustomUserSerializer(user, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


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
        if not Recipe.objects.filter(id=pk).exists():
            return Response(
                {'add recipe': 'You are trying to add a non-existent recipe!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        recipe = Recipe.objects.get(id=pk)
        recipe_in_list = model.objects.filter(
            recipe=recipe, user=self.request.user
        )
        if recipe_in_list.exists():
            return Response(
                {'add recipe': 'The recipe has already been added to list.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        model.objects.create(recipe=recipe, user=self.request.user)
        serializer = ShortRecipeSerializer(recipe)

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED
        )

    def delete_recipe(self, model, request, pk):
        """Removes recipes from the list."""
        recipe = get_object_or_404(Recipe, pk=pk)
        recipe_in_list = model.objects.filter(
            recipe=recipe, user=self.request.user
        )
        if recipe_in_list.exists():
            recipe_in_list.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({
            'recipe': 'You are trying to delete a recipe that does not exist.'
        },
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
        return self.delete_recipe(ShoppingCart, request, pk)

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        """Downloads a shopping list."""
        if not self.request.user.shopping_cart.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        ingredients = IngredientInRecipe.objects.filter(
            recipe__shopping_cart__user=self.request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).order_by(
            'ingredient__name'
        ).annotate(amount=Sum('amount'))
        today = datetime.today()
        shopping_list = (
            f"FoodGram Service\n"
            f"Today's date.: {today:%Y-%m-%d}\n"
            f"Your shopping list.:\n"
        )
        shopping_list += '\n'.join([
            f'- {ingredient["ingredient__name"]} - {ingredient["amount"]} '
            f'{ingredient["ingredient__measurement_unit"]}'
            for ingredient in ingredients
        ])
        filename = f'{self.request.user}_shopping_list.txt'
        content_type = 'text/plain,charset=utf8'
        response = HttpResponse(shopping_list, content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename={filename}'

        return response
