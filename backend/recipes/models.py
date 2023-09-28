"""
Module for creating, configuring and managing `recipe' app models.
"""
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from colorfield.fields import ColorField

from users.models import CustomUser


class Ingredient(models.Model):
    """ Ingredient model. """

    name = models.CharField(
        max_length=200,
        verbose_name='Ingredient name',
        db_index=True,
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Measurement unit',
    )

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Tag(models.Model):
    """ Tag model. """

    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Tag name',
    )
    color = ColorField(
        default='#FF0000',
        max_length=200,
        verbose_name='Tag color',
        unique=True,
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Tag slug',
    )

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """ Recipe model. """

    name = models.CharField(
        max_length=200,
        verbose_name='Recipe name',
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Recipe author',
    )
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Recipe image',
    )
    text = models.TextField(
        verbose_name='Recipe description',
    )
    tags = models.ManyToManyField(
        Tag,
        db_index=True,
        related_name='recipes',
        verbose_name='Recipe tags',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='ingredients',
        through='IngredientInRecipe',
        through_fields=('recipe', 'ingredient'),
        verbose_name='Ingredients in the recipe.',
    )
    cooking_time = models.IntegerField(
        blank=False,
        verbose_name='Recipe preparation time in minutes.',
        default=1,
        validators=[
            MinValueValidator(
                1, 'Cooking time must be >=1 minute.'),
            MaxValueValidator(
                6000, 'Cooking time exceeds all norms!')
        ],
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Recipe publication date.',
    )

    class Meta:
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    """ Relationship model between recipe and ingredient models. """

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
        validators=[MinValueValidator(
            1, 'The number of ingredients must be >=1'
        )],
        default=1,
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


class Favorite(models.Model):
    """ Favorites model. """

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='User',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='users_favorites',
        verbose_name="Recipe from the user's favorites.",
    )

    class Meta:
        verbose_name = 'Favorites'
        verbose_name_plural = 'Favorites'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorite',
            ),
        )

    def __str__(self):
        return f'{self.recipe} from {self.user} favorites'


class ShoppingCart(models.Model):
    """ ShoppingCart model. """

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='User',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name="Recipe from a user's shopping cart.",
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_shopping_cart'
            ),
        )
        verbose_name = 'Shopping cart'
        verbose_name_plural = 'Shopping carts.'

    def __str__(self):
        return f'{self.recipe} from {self.user} shopping cart'
