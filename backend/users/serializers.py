"""
Module for creating, configuring and managing 'users' app serializers
"""
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from .models import CustomUser, Subscribe
from ..recipes.models import Recipe


class CustomUserCreateSerializer(UserCreateSerializer):
    """ Serializer for model 'CustomUser' on POST requests. """

    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
            )


class CustomUserSerializer(UserSerializer):
    """ Serializer for model 'CustomUser'. """

    is_subscribed = serializers.SerializerMethodField(
        method_name='get_is_subscribed',
        read_only=True,
        )

    class Meta:
        model = CustomUser
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
            'is_subscribed',
            )

    def get_is_subscribed(self, obj):
        """ Checking a user's subscription to other users. """
        user = self.context.get('request').user
        if user.is_anonymous:
            return False

        return Subscribe.objects.filter(user=user, author=obj).exists()

    def validate(self, data):
        """ Checking if there is a user with the same username. """
        if CustomUser.object.filters(username=data.get('username')
                                     ).exists():
            raise serializers.ValidationError(
                'A user with the same username already exists!'
            )

        return super().validate(data)


class SubscribeSerializer(serializers.ModelSerializer):
    """ Serializer for model 'Subscribe'. """

    user = SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        many=False,
        read_only=True,
    )

    following = SlugRelatedField(
        slug_field='username',
        many=False,
        queryset=CustomUser.objects.all(),
    )

    class meta:
        model = Subscribe
        fields = ('user', 'following',)
        read_only_fields = ('user',)
        validators = [
            UniqueTogetherValidator(
                queryset=Subscribe.objects.all(),
                fields=('user', 'following'),
                message='You are already subscribed.'
            )
        ]

    def validate(self, data):
        """ Checking your subscription to yourself. """
        if self.context['request'].user == data['following']:
            raise serializers.ValidationError(
                "You can't subscribe to yourself."
            )

        return super().validate(data)


class ShortRecipeSerializer(serializers.ModelSerializer):
    """ Shortened recipe serializer. """

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscriptionSerializer(serializers.ModelSerializer):
    """ Serializer about user-created subscriptions and recipes. """

    recipes = ShortRecipeSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField(
        method_name='get_is_subscribed'
        )
    recipes_count = serializers.SerializerMethodField(
        method_name='get_recipes_count'
    )

    class Meta:
        model = CustomUser
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

    def get_is_subscribed(self, obj):
        """ Checking a user's subscription to other users. """
        user = self.context.get('request').user
        if user.is_anonymous:
            return False

        return Subscribe.objects.filter(user=user, author=obj).exists()

    def get_recipes_count(self, obj):
        """Getting the total number of recipes, written by the user. """
        return obj.author.recipes.count()
