"""
Module for registering 'recipe' app models in the admin interface.
"""
from django.contrib import admin

from .models import (Tag,
                     Ingredient,
                     Recipe,
                     IngredientInRecipe,
                     ShoppingCart,
                     Favorite,
                     )


class IngredientsInRecipeInline(admin.TabularInline):

    model = IngredientInRecipe
    extra = 1


@admin.register(IngredientInRecipe)
class IngredientsInRecipeAdmin(admin.ModelAdmin):
    """ Represents the 'IngredientsRecipe' model in the admin interface. """

    list_display = ('pk', 'ingredient', 'recipe', 'amount',)
    list_filter = ('ingredient', 'recipe',)
    search_fields = ('recipe', 'ingredient',)
    empty_value_display = '-empty-'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """ Represents the 'Tag' model in the admin interface. """

    list_display = ('pk', 'name', 'color', 'slug',)
    list_filter = ('name', 'color',)
    search_fields = ('name',)
    empty_value_display = '-empty-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """ Represents the 'Ingredient' model in the admin interface. """

    list_display = ('pk', 'name', 'measurement_unit',)
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-empty-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """ Represents the 'Recipe' model in the admin interface. """

    inlines = (IngredientsInRecipeInline,)
    list_display = ('pk', 'name', 'author', 'num_recipe_was_in_fav',)
    search_fields = ('name', 'author', 'tags',)
    list_filter = ('name', 'author', 'tags')
    empty_value_display = '-empty-'

    def num_recipe_was_in_fav(self, instance):
        """
        Shows the total number of times
        this recipe has been added to favorites.
        """
        return instance.favorite_recipes.count()


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """ Represents the 'Favorite' model in the admin interface """

    list_display = ('pk', 'user', 'recipe',)
    empty_value_display = '-empty-'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """ Represents the 'ShoppingCart' model in the admin interface. """

    list_display = ('pk', 'user', 'recipe',)
    empty_value_display = '-empty-'
