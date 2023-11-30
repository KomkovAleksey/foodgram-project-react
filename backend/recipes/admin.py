"""
Module for registering "recipe" app models in the admin interface.
"""
from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe
from rest_framework.authtoken.models import TokenProxy

from .models import (
    Tag,
    Ingredient,
    Recipe,
    IngredientInRecipe,
    ShoppingCart,
    Favorite,
)

admin.site.site_header = (
    'Foodgram project administration zone.'
)

admin.site.empty_value_display = '-empty-'

admin.site.unregister(Group)
admin.site.unregister(TokenProxy)


class IngredientsInRecipeInline(admin.StackedInline):
    """
    Class for display and control
    many-to-many relationship
    between the Recipe model
    and the Ingredient model.
    """

    model = IngredientInRecipe
    min_num = 1
    extra = 1


@admin.register(IngredientInRecipe)
class IngredientInRecipeAdmin(admin.ModelAdmin):
    """Represents the "IngredientsRecipe" model in the admin interface."""

    list_display = (
        'id',
        'ingredient',
        'recipe',
        'amount',
    )
    list_filter = (
        'ingredient',
        'recipe',
    )
    search_fields = (
        'recipe',
        'ingredient',
    )
    ordering = (
        'id',
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Represents the "Tag" model in the admin interface."""

    list_display = (
        'id',
        'name',
        'color',
        'slug',
    )
    list_filter = (
        'name',
        'color',
        'slug',
    )
    search_fields = (
        'name',
        'color',
        'slug',
    )
    ordering = (
        'name',
        'color',
        'slug',
    )


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Represents the "Ingredient" model in the admin interface."""

    list_display = (
        'id',
        'name',
        'measurement_unit',
    )
    search_fields = (
        'name',
    )
    list_filter = (
        'name',
    )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Represents the "Recipe" model in the admin interface."""

    inlines = (
        IngredientsInRecipeInline,
    )
    list_display = (
        'id',
        'name',
        'author',
        'get_favorites',
    )
    search_fields = (
        'name',
        'author',
        'tags',
    )
    list_filter = (
        'name',
        'author',
        'tags',
    )
    filter_horizontal = (
        'tags',
        'ingredients',
    )

    @admin.display()
    def get_favorites(self, instance):
        """
        Shows the total number of times
        this recipe has been added to favorites.
        """
        return instance.favorites.count()

    @admin.display(description='ingredients')
    def get_ingredients(self, obj):
        queryset = IngredientInRecipe.objects.filter(recipe_id=obj.id).all

        return ', '.join([
            f'{item.ingredient.name} {item.ingredient.amount} '
            f'{item.ingredient.measurement_unit}'
            for item in queryset
        ])


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Represents the "Favorite" model in the admin interface."""

    list_display = (
        'id',
        'user',
        'recipe',
    )
    list_filter = (
        'user',
        'recipe',
    )
    search_fields = (
        'user',
    )
    ordering = (
        'id',
    )


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """Represents the "ShoppingCart" model in the admin interface."""

    list_display = (
        'id',
        'user',
        'recipe',
    )
    list_filter = (
        'user',
        'recipe',
    )
    search_fields = (
        'user',
    )
    ordering = (
        'id',
    )
