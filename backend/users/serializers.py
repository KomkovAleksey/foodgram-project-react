"""
Module for creating, configuring and managing 'users' app serializers
"""
from djoser.serializers import UserCreateSerializer, UserSerializer
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework.exceptions import ValidationError
from drf_extra_fields.fields import Base64ImageField

from recipes.models import Recipe
from users.models import Follow

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    """Serializer for model "CustomUser" to create a user"""

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )


class CustomUserSerializer(UserSerializer):
    """Serializer for model 'CustomUser'."""

    is_subscribed = SerializerMethodField(
        method_name='get_is_subscribed',
    )

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
            'is_subscribed',
        )
        extra_kwargs = {"password": {"write_only": True}}

    def get_is_subscribed(self, obj):
        """Checking a user's subscription to other users."""
        user = self.context.get('request').user
        if user.is_anonymous:
            return False

        return Follow.objects.filter(user=user, author=obj).exists()


class ShortRecipeSerializer(ModelSerializer):
    """Shortened recipe serializer."""

    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class SubscriptionSerializer(CustomUserSerializer):
    """Serializer about user-created subscriptions and recipes."""

    recipes_count = SerializerMethodField(
        method_name='get_recipes_count'
    )
    recipes = SerializerMethodField(
        method_name='get_recipes'
    )

    class Meta(CustomUserSerializer.Meta):
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
        )

    def validate_subscription(self, data):
        """Subscription Validation."""
        author = data['author']
        user = data['user']
        if user.follower.filter(author=author).exists():
            raise ValidationError(
                'You are already subscribed.',
                code=status.HTTP_400_BAD_REQUEST,
            )
        if user == author:
            raise ValidationError(
                "You can't subscribe to yourself.",
                code=status.HTTP_400_BAD_REQUEST,
            )

        return super().validate(data)

    def get_recipes_count(self, obj):
        """Getting the total number of recipes for current author."""
        return obj.recipes.count()

    def get_recipes(self, obj):
        """Get the number of recipes for a specific author."""
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        if limit:
            recipes = obj.recipes.all()[: int(limit)]
        else:
            recipes = obj.recipes.all()

        return ShortRecipeSerializer(recipes, many=True, read_only=True).data
