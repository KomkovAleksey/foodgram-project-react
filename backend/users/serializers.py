"""
Module for creating, configuring and managing 'users' app serializers
"""
from djoser.serializers import UserCreateSerializer, UserSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from recipes.models import Recipe
from .models import Follow

User = get_user_model


class CustomUserCreateSerializer(UserCreateSerializer):
    """Serializer for model "CustomUser" on POST requests."""

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        )


class CustomUserSerializer(UserSerializer):
    """Serializer for model 'CustomUser'."""

    is_subscribed = serializers.SerializerMethodField(
        method_name='get_is_subscribed',
    )

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
            'is_subscribed',
        )

    def validate(self, data):
        """Checking if there is a user with the same username."""
        if User.object.filters(username=data.get('username')).exists():
            raise serializers.ValidationError(
                'A user with the same username already exists!'
            )

        return super().validate(data)

    def get_is_subscribed(self, obj):
        """Checking a user's subscription to other users."""
        user = self.context.get('request').user
        if user.is_anonymous:
            return False

        return Follow.objects.filter(user=user, author=obj).exists()


class ShortRecipeSerializer(serializers.ModelSerializer):
    """Shortened recipe serializer."""

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )
        read_only_fields = [
            'id',
            'name',
            'image',
            'cooking_time',
        ]


class SubscriptionSerializer(serializers.ModelSerializer):
    """Serializer about user-created subscriptions and recipes."""

    is_subscribed = serializers.SerializerMethodField(
        method_name='get_is_subscribed'
    )
    recipes_count = serializers.SerializerMethodField(
        method_name='get_recipes_count'
    )
    recipes = serializers.SerializerMethodField(
        method_name='get_recipes'
    )

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )
        read_only_fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'recipes',
        )

    def validate(self, data):
        author = data['author']
        user = data['user']
        if user.follower.filter(author=author).exists():
            raise ValidationError(
                'You are already subscribed.',
            )
        if user == author:
            raise ValidationError(
                "You can't subscribe to yourself.",
            )

        return super().validate(data)

    def get_is_subscribed(self, obj):
        """Checking user subscription."""
        user = self.context.get('request').user.pk
        if user.is_anonymous:
            return False

        return Follow.objects.filter(user=user, author=obj).exists()

    def get_recipes_count(self, obj):
        """Getting the total number of recipes."""
        return obj.recipes.count()

    def get_recipes(self, obj):
        request = self.context('request')
        limit = request.GET.get('recipes_limit')
        recipes = obj.recipes.all()
        if limit:
            recipes = recipes[: int(limit)]

        return ShortRecipeSerializer(recipes, many=True, read_only=True).data
