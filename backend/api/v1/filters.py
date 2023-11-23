"""
Filters.
"""
from django_filters.rest_framework import FilterSet, filters
from django.contrib.auth import get_user_model

from recipes.models import Tag, Ingredient, Recipe

User = get_user_model()


class IngredientFilter(FilterSet):
    """Filter class for model 'Ingredient'."""

    name = filters.CharFilter(
        field_name='name',
        lookup_expr='istartswith',
    )

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(FilterSet):
    """Filter class for 'Recipe' model."""

    author = filters.ModelChoiceFilter(
        queryset=User.objects.all()
    )
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
        to_field_name='slug',
    )
    is_favorited = filters.BooleanFilter(
        method='get_is_favorited'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = (
            'tags',
            'author',
            'is_favorited',
            'is_in_shopping_cart',
        )

    def get_is_favorited(self, queryset, name, value):
        """Filters recipes based on user favorites."""
        if self.request.user.is_authenticated and value is True:
            return queryset.filter(favorites__user=self.request.user)

        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        """Filters recipes based on users shopping cart."""
        if self.request.user.is_authenticated and value is True:
            return queryset.filter(shopping_cart__user=self.request.user)

        return queryset
