"""
'recipes' app configuration
"""
from django.apps import AppConfig


class RecipesConfig(AppConfig):
    """Класс конфигурации приложения recipes. """

    default_auto_field = "django.db.models.BigAutoField"
    name = "recipes"
