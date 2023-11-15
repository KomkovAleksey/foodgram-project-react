"""
Module for creating, configuring and managing `recipe' app models.
"""
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.html import format_html
from colorfield.fields import ColorField

from core.constants import HelpTextRecipes, ConstantRecipes, ErrorText


User = get_user_model()


class Ingredient(models.Model):
    """Ingredient model."""

    name = models.CharField(
        max_length=ConstantRecipes.MAX_NAME_LENGTH,
        verbose_name='Ingredient name',
        db_index=True,
        help_text=HelpTextRecipes.INGREDIENT_NAME,
    )
    measurement_unit = models.CharField(
        max_length=ConstantRecipes.MAX_MEASUREMENT_UNIT,
        verbose_name='Measurement unit',
        help_text=HelpTextRecipes.MEASUREMENT_UNIT,
    )

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'
        ordering = ('name',)
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_ingredient_name_and_measurement_unit',
            ),
        )

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Tag model."""

    name = models.CharField(
        max_length=ConstantRecipes.MAX_NAME_LENGTH,
        unique=True,
        verbose_name='Tag name',
        help_text=HelpTextRecipes.TAG_NAME,
    )
    color = ColorField(
        default='#FF0000',
        verbose_name='Hex color',
        unique=True,
        help_text=HelpTextRecipes.TAG_COLOR,
    )
    slug = models.SlugField(
        max_length=ConstantRecipes.MAX_SLUG_LENGTH,
        unique=True,
        verbose_name='Tag slug',
        help_text=HelpTextRecipes.TAG_SLUG,
    )

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Recipe model."""

    name = models.CharField(
        max_length=ConstantRecipes.MAX_NAME_LENGTH,
        verbose_name='Recipe name',
        help_text=HelpTextRecipes.RECIPE_NAME,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Recipe author',
        help_text=HelpTextRecipes.RECIPE_AUTHOR,
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        verbose_name='Recipe image',
        blank=True,
    )
    text = models.TextField(
        verbose_name='Recipe description',
        help_text=HelpTextRecipes.RECIPE_TEXT,
    )
    tags = models.ManyToManyField(
        Tag,
        db_index=True,
        related_name='recipes',
        verbose_name='Recipe tags',
        help_text=HelpTextRecipes.RECIPE_TAG,
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='ingredients',
        through='IngredientInRecipe',
        through_fields=('recipe', 'ingredient'),
        verbose_name='Ingredients in the recipe.',
        help_text=HelpTextRecipes.RECIPE_INGREDIENT,
    )
    cooking_time = models.IntegerField(
        blank=False,
        verbose_name='Recipe preparation time in minutes.',
        default=1,
        validators=[
            MinValueValidator(
                ConstantRecipes.MIN_COOKING_TIME,
                ErrorText.MIN_COOKING_ERROR
            ),
            MaxValueValidator(
                ConstantRecipes.MAX_COOKING_TIME,
                ErrorText.MAX_COOKING_ERROR
            )
        ],
        help_text=HelpTextRecipes.RECIPE_COOKING_TIME,
    )

    class Meta:
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'
        ordering = ('name',)
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'author'),
                name='unique_author_of_the_recipe',
            ),
        )

    def formatted_text(self):
        return format_html('<br>'.join(self.text.splitlines()))

    def __str__(self):
        return f'{self.name}:{self.author.username}'


class IngredientInRecipe(models.Model):
    """Relationship model between "recipe" and "ingredient" models."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='amount',
        verbose_name='Recipe',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='amount',
        verbose_name='Ingredient',
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Amount of ingredients',
        validators=[
            MinValueValidator(
                ConstantRecipes.MIN_AMOUNT,
                ErrorText.MIN_AMOUNT_ERROR
            ),
            MaxValueValidator(
                ConstantRecipes.MAX_AMOUNT,
                ErrorText.MAX_AMOUNT_ERROR
            )
        ],
        default=1,
        help_text=HelpTextRecipes.AMOUNT,
    )

    class Meta:
        verbose_name = 'Ingredient in recipe'
        verbose_name_plural = 'Ingredients in recipes'
        constraints = (
            models.UniqueConstraint(
                fields=('ingredient', 'recipe'),
                name='unique_ingredient_in_recipe',
            ),
        )

    def __str__(self):
        return f'{self.ingredient}:{self.amount} in {self.recipe}'


class UserRecipe(models.Model):
    """Abstract class for shopping list and favorites."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='User',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Recipe',
    )

    class Meta:
        abstract = True
        ordering = ('recipe',)


class Favorite(UserRecipe):
    """Favorites model."""

    class Meta(UserRecipe.Meta):
        default_related_name = 'favorites'
        verbose_name = 'Favorites'
        verbose_name_plural = 'Favorites'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorite',
            ),
        )

    def __str__(self):
        return f'{self.recipe} from {self.user} favorites list'


class ShoppingCart(UserRecipe):
    """ShoppingCart model."""

    class Meta(UserRecipe.Meta):
        default_related_name = 'shopping_cart'
        verbose_name = 'Shopping cart'
        verbose_name_plural = 'Shopping carts.'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_shopping_cart'
            ),
        )

    def __str__(self):
        return f'{self.recipe} from {self.user} shopping cart'
