"""
'api' application views
"""
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.validators import ValidationError

from .utils import convert_txt
from .mixins import RetrieveListViewSet
from .filters import IngredientFilter, TagFilter
from .paginators import PageLimitPagination
from .permissions import IsAuthorOrReadOnly, IsAdminUserOrReadOnly
from .serializers import (AddRecipeSerializer,
                          IngredientSerializer,
                          RecipeSerializer,
                          TagSerializer,
                          ShortRecipeSerializer,
                          )

from recipes.models import (Favorite,
                            Ingredient,
                            Tag,
                            IngredientsInRecipe,
                            Recipe,
                            ShoppingCart,
                            )


class IngredientViewSet(RetrieveListViewSet):
    """Вьюсет для модели 'Ingredient'."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    filterset_class = IngredientFilter


class TagViewSet(RetrieveListViewSet):
    """Вьюсет для модели 'Tag'."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminUserOrReadOnly,)


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели 'Recipe'."""

    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = PageLimitPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TagFilter

    def get_serializer_class(self):
        """выбора класса сериализатора в зависимости от запроса."""

        if self.action in ('list', 'retrieve'):
            return RecipeSerializer
        return AddRecipeSerializer

    def perform_create(self, serializer):
        """
        Автоматическое сохранения автора рецепта
        при создании нового рецепта.
        """
        user = self.request.user
        serializer.save(author=user)

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk=None):
        """
        В завасимости от метода
        или удаляет рецепт из списка избранного.
        """

        if request.method == 'POST':
            return self.add_recipe(Favorite, request, pk)
        else:
            return self.delete_recipe(Favorite, request, pk)

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        """ Скачивает список покупок. """

        ingredients = IngredientsInRecipe.objects.filter(
            recipe__shopping_cart__user=request.user
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).order_by(
            'ingredient__name'
        ).annotate(ingredient_total=Sum('amount'))
        return convert_txt(ingredients)

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        """
        В завасимости от метода добавляет
        или удаляет рецепт из списка покупок.
        """

        if request.method == 'POST':
            return self.add_recipe(ShoppingCart, request, pk)
        else:
            return self.delete_recipe(ShoppingCart, request, pk)

    def add_recipe(self, model, request, pk):
        """ Добавление рецепта. """

        recipe = get_object_or_404(Recipe, pk=pk)
        user = self.request.user
        if model.objects.filter(recipe=recipe, user=user).exists():
            raise ValidationError('Рецепт уже добавлен')
        model.objects.create(recipe=recipe, user=user)
        serializer = ShortRecipeSerializer(recipe)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def delete_recipe(self, model, request, pk):
        """ Удаление рецепта. """
        recipe = get_object_or_404(Recipe, pk=pk)
        user = self.request.user
        obj = get_object_or_404(model, recipe=recipe, user=user)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
