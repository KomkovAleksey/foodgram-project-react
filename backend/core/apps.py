"""
core application configuration
"""
from django.apps import AppConfig


class CoreConfig(AppConfig):
    """core application configuration class."""
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
