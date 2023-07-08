"""
`users` application serializers.
"""
from djoser.serializers import UserSerializer
from rest_framework import serializers

import api
from recipes.models import Recipe
from .models import Subscription, User


class CurrentUserSerializer(UserSerializer):
    """сериализатор для модели `User`."""

    is_subscribed = serializers.SerializerMethodField(
        method_name='get_is_subscribed'
    )

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        """Метод проверяет, аутентифицирован ли пользователь"""

        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Subscription.objects.filter(
            user=request.user, author=obj
        ).exists()


class SubscribeSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели `Subscribe`. """

    class Meta:
        model = Subscription
        fields = ('user', 'author')

    def to_representation(self, instance):
        """Метод создает экземпляр сериализатора `SubscriptionSerializer`,
         передавая ему экземпляр подписки и контекст запроса.
          Затем он возвращает сериализованные данные."""

        request = self.context.get('request')
        context = {'request': request}
        serializer = SubscriptionSerializer(
            instance,
            context=context
        )
        return serializer.data

    def validate(self, data):
        """Проверка подписки пользоввателя."""
        user = data.get('user')
        author = data.get('author')
        if user == author:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!'
            )
        if Subscription.objects.filter(user=user, author=author).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на этого пользователя!'
            )
        return data


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор для модели `Subscription`"""

    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField(
        method_name='get_is_subscribed'
    )
    recipes = serializers.SerializerMethodField(method_name='get_recipes')
    recipes_count = serializers.SerializerMethodField(
        method_name='get_recipes_count'
    )

    class Meta:
        model = Subscription
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
        """
        Функция проверяет, существует ли
        подписка пользователя на данного автора.
        """
        request = self.context.get('request')
        return Subscription.objects.filter(
            author=obj.author, user=request.user
        ).exists()

    def get_recipes(self, obj):
        """Получение списка рецептов, написанных автором."""

        request = self.context.get('request')
        if request.GET.get('recipe_limit'):
            recipe_limit = int(request.GET.get('recipe_limit'))
            queryset = Recipe.objects.filter(
                author=obj.author)[:recipe_limit]
        else:
            queryset = Recipe.objects.filter(
                author=obj.author)
        serializer = api.serializers.ShortRecipeSerializer(
            queryset, read_only=True, many=True
        )
        return serializer.data

    def get_recipes_count(self, obj):
        """Получение общего количества рецептов,
         написанных  автором."""
        return obj.author.recipes.count()
