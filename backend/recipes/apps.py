"""
Module for configuring the 'recipes' application.
"""
from django.apps import AppConfig


class RecipesConfig(AppConfig):
    """ Class for configuring the 'recipes' application. """

    default_auto_field = "django.db.models.BigAutoField"
    name = "recipes"
