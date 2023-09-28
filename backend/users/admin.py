"""
Module for registering 'users' app models in the admin interface.
"""
from django.contrib import admin

from .models import CustomUser, Subscribe


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """ Represents the 'CustomUser' model in the admin interface. """

    list_display = ('pk', 'username', 'first_name', 'last_name', 'email',)
    search_fields = ('username', 'email', 'first_name', 'last_name',)
    list_filter = ('username', 'email', 'first_name', 'last_name',)
    empty_value_display = '-empty-'


@admin.register(Subscribe)
class SubscriptionAdmin(admin.ModelAdmin):
    """ Represents the 'Subscribe' model in the admin interface. """

    list_display = ('pk', 'user', 'following',)
    list_filter = ('user', 'following',)
    empty_value_display = '-empty-'
