from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class UserRecipe(models.Model):
    """Abstract class for shopping list and favorites."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='User',
    )
    recipe = models.ForeignKey(
        'recipes.Recipe',
        on_delete=models.CASCADE,
        verbose_name='Recipe',
    )

    class Meta:
        abstract = True
        ordering = ('recipe',)
