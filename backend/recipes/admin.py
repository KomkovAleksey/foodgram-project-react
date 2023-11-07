"""
Module for registering "recipe" app models in the admin interface.
"""
from django.contrib import admin

from .models import (
    Tag,
    Ingredient,
    Recipe,
    IngredientInRecipe,
    ShoppingCart,
    Favorite,
)

admin.site.site_header = (
    'Administration of the "recipes" app for "foodgram" project.'
)

admin.site.empty_value_display = '-empty-'


class IngredientsInRecipeInline(admin.StackedInline):
    """
    Class for display and control
    many-to-many relationship
    between the Recipe model
    and the Ingredient model.
    """

    model = IngredientInRecipe
    extra = 1


@admin.register(IngredientInRecipe)
class IngredientInRecipeAdmin(admin.ModelAdmin):
    """Represents the "IngredientsRecipe" model in the admin interface."""

    list_display = (
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
        'name',
        'color',
        'slug',
    )
    list_filter = (
        'name',
    )
    search_fields = (
        'name',
        'slug',
    )
    ordering = (
        'name',
    )


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Represents the "Ingredient" model in the admin interface."""

    list_display = (
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

    def get_favorites(self, instance):
        """
        Shows the total number of times
        this recipe has been added to favorites.
        """
        return instance.favorite_recipes.count()


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Represents the "Favorite" model in the admin interface."""

    list_display = (
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
