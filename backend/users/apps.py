"""
Module for configuring the 'users' application.
"""
from django.apps import AppConfig


class UsersConfig(AppConfig):
    """ Users app config class """

    default_auto_field = "django.db.models.BigAutoField"
    name = 'users'
