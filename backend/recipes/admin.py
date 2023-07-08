"""
Registering models in the 'recipes' admin interface.
"""
from django.contrib import admin

from recipes.models import (Favorite,
                            Ingredient,
                            Tag,
                            IngredientsInRecipe,
                            Recipe,
                            ShoppingCart,
                            )


class IngredientsInRecipeInline(admin.TabularInline):
    """
    класс для отображения и управления
    отношением "многие-ко-многим"
    между моделью Recipe и моделью Ingredients
    """
    model = Recipe.ingredients.through
    extra = 1

@admin.register(IngredientsInRecipe)
class IngredientsInRecipeAdmin(admin.ModelAdmin):
    """
    Представляет модель 'IngredientsInRecipe'
    в интерфейсе администратора.
    """

    list_display = (
        'pk',
        'ingredient',
        'recipe',
        'amount'
    )
    search_fields = ('recipe__name', 'ingredient__name')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """ Представляет модель 'Tag' в интерфейсе администратора. """

    list_display = (
        'pk',
        'name',
        'color',
        'slug'
    )
    list_editable = ('color',)
    search_fields = ('name', 'color', 'slug')

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Представляет модель 'Ingredient' в интерфейсе администратора."""

    list_display = (
        'pk',
        'name',
        'measurement_unit',
    )
    search_fields = ('measurement_unit',)
    list_filter = ('measurement_unit',)

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Представляет модель 'Recipe' в интерфейсе администратора."""

    inlines = (IngredientsInRecipeInline,)
    list_display = (
        'pk',
        'name',
        'author'
    )
    search_fields = (
        'name',
        'author__username',
        'author__email'
    )
    readonly_fields = ('is_favorited',)

    def is_favorited(self, instance):
        return instance.favorite_recipes.count()

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Представляет модель 'Favorite' в интерфейсе администратора."""

    list_display = (
        'pk',
        'user',
        'recipe'
    )
    search_fields = (
        'user__username',
        'user__email',
        'recipe__name'
    )

@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """Представляет модель 'ShoppingCart' в интерфейсе администратора."""

    list_display = (
        'pk',
        'user',
        'recipe'
    )
    search_fields = (
        'user__username',
        'user__email',
        'recipe__name'
    )
