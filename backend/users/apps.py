"""
'users' application configuration
"""
from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Класс конфигурации приложения users. """

    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
