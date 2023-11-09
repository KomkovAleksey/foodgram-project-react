"""
A module for registering and configuring "users"
application models in the administrator interface.
"""
from django.contrib import admin
from django.contrib.auth.models import Group
from rest_framework.authtoken import TokenProxy

from .models import CustomUser, Follow


admin.site.site_header = (
    'Administration of the "users" app for "foodgram" project.'
)

admin.site.empty_value_display = '-empty-'

admin.site.unregister(Group)
admin.site.unregister(TokenProxy)


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """Represents the "CustomUser" model in the admin interface."""

    list_display = (
        'email',
        'username',
        'first_name',
        'last_name',
        'recipe_count',
        'follower_count',
    )
    search_fields = (
        'username',
        'email',
        'first_name',
        'last_name',
    )
    list_filter = (
        'username',
        'email',
        'first_name',
        'last_name',
    )

    @admin.display(description='Number of recipes in the favorites list')
    def recipe_count(self, obj):
        return obj.recipes.count()

    @admin.display(description='Number of followers')
    def follower_count(self, obj):
        return obj.author_followers.count()


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Represents the "Subscribe" model in the admin interface."""

    list_display = (
        'user',
        'author',
    )
    list_filter = (
        'user',
        'author',
    )
    ordering = (
        'id',
    )
