"""
api application configuration
"""
from django.apps import AppConfig


class ApiConfig(AppConfig):
    """Класс конфигурации приложения api. """

    default_auto_field = "django.db.models.BigAutoField"
    name = "api"
