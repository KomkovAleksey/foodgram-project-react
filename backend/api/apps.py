"""
api application configuration
"""
from django.apps import AppConfig


class ApiConfig(AppConfig):
    """ api application configuration class. """

    default_auto_field = "django.db.models.BigAutoField"
    name = "api"
