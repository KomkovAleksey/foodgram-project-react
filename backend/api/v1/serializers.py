"""
Module for creating, configuring and managing 'recipes' app serializers
"""
import webcolors
from djoser.serializers import UserCreateSerializer, UserSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.db.transaction import atomic
from drf_extra_fields.fields import Base64ImageField

from core.constants import ConstantRecipes
from users.models import Follow
from recipes.models import (
    Ingredient,
    Tag,
    Recipe,
    IngredientInRecipe,
    Favorite,
    ShoppingCart
)

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

    is_subscribed = serializers.SerializerMethodField(
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
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        """Checking a user's subscription to other users."""
        request = self.context.get('request')

        return (
            request and request.user.is_authenticated
            and request.user.follower.filter(author_id=obj.id).exists()
        )


class ShortRecipeSerializer(serializers.ModelSerializer):
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

    recipes_count = serializers.ReadOnlyField(
        source='recipes.count'
    )
    recipes = serializers.SerializerMethodField(
        method_name='get_recipes'
    )

    class Meta(CustomUserSerializer.Meta):
        model = User
        fields = CustomUserSerializer.Meta.fields + (
            'recipes_count',
            'recipes',
        )
        read_only_fields = (
            'email',
            'username',
            'first_name',
            'last_name',
        )

    def get_recipes(self, obj):
        """Get the number of recipes for a specific author."""
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = obj.recipes.all()
        if limit:
            try:
                recipes = recipes[:int(limit)]
            except ValueError:
                pass

        return ShortRecipeSerializer(recipes, many=True, read_only=True).data


class FollowSerializer(serializers.ModelSerializer):
    """Serializer for model Follow."""

    class Meta:
        model = Follow
        fields = ('user', 'author')
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'author'),
                message='You are already subscribed.'
            )
        ]

    def validate(self, data):
        """Self-subscription check."""
        if data['user'] == data['author']:
            raise serializers.ValidationError('No self-subscription!')

        return super().validate(data)

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return SubscriptionSerializer(instance.author, context=context).data


class Hex2NameColor(serializers.Field):
    """Converts a color code to a color name."""

    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError(
                'There is no name for this color'
            )


class TagSerializer(serializers.ModelSerializer):
    """Serializer for model Tag."""

    color = Hex2NameColor()

    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )
        read_only_fields = ('__all__',)


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for model Ingredient."""

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )
        read_only_fields = ('__all__',)


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    """Serializer for model IngredientInRecipe."""

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientInRecipe
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class AddIngredientSerializer(serializers.ModelSerializer):
    """Serializer for the amount of ingredient in a recipe."""

    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        error_messages={'does_not_exist': 'Ingredient not found!'},
    )
    amount = serializers.IntegerField(
        min_value=ConstantRecipes.MIN_AMOUNT,
        max_value=ConstantRecipes.MAX_AMOUNT,
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'amount')


class RecipeReadSerializer(serializers.ModelSerializer):
    """Serializer for model 'Recipe' on GET requests."""

    author = CustomUserSerializer(
        read_only=True,
        many=False,
    )
    tags = TagSerializer(
        read_only=True,
        many=True,
    )
    ingredients = IngredientInRecipeSerializer(
        source='amount',
        many=True,
    )
    image = Base64ImageField(required=True)
    is_favorited = serializers.SerializerMethodField(
        read_only=True,
        method_name='get_is_favorited',
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        read_only=True,
        method_name='get_is_in_shopping_cart',
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'tags',
            'author',
            'image',
            'text',
            'ingredients',
            'cooking_time',
            'is_favorited',
            'is_in_shopping_cart',
        )

    def in_list(self, obj, model):
        """Checking whether the recipe is on the list."""
        request = self.context.get('request')

        return (
            request and request.user.is_authenticated
            and model.objects.filter(
                user=request.user.id, recipe_id=obj.id
            ).exists()
        )

    def get_is_favorited(self, obj):
        """Checking whether the recipe is in your favorites."""
        return self.in_list(obj, Favorite)

    def get_is_in_shopping_cart(self, obj):
        """Checking whether the recipe is in the shopping cart."""
        return self.in_list(obj, ShoppingCart)


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for model 'Recipe' on POST, PATCH, requests."""

    author = CustomUserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )
    ingredients = AddIngredientSerializer(many=True)
    image = Base64ImageField(required=True)
    cooking_time = serializers.IntegerField(
        min_value=ConstantRecipes.MIN_COOKING_TIME,
        max_value=ConstantRecipes.MAX_COOKING_TIME,
    )

    class Meta:
        model = Recipe
        fields = (
            'tags',
            'name',
            'author',
            'ingredients',
            'image',
            'text',
            'cooking_time',
        )

    def validate(self, data):
        """Validate tags, ingredients, cooking time, recipe image"""
        # Checking tags.
        tags = data.get('tags')
        if not tags:
            raise serializers.ValidationError(
                'You must select at least one tag.'
            )
        if len(tags) != len(set(tags)):
            raise serializers.ValidationError(
                'Tags should not be repeated!'
            )

        # Checking ingredients.
        ingredients = data.get('ingredients')
        if not ingredients:
            raise serializers.ValidationError(
                'The ingredients field cannot be empty.'
            )
        for ingredient in ingredients:
            ingredient_name = ingredient['id']
        if int(ingredient['amount']) <= ConstantRecipes.INCORRECT_AMOUNT:
            raise serializers.ValidationError(
                f'Incorrect quantity for {ingredient_name}'
            )
        if not isinstance(ingredient['amount'], int):
            raise serializers.ValidationError(
                'must be a whole number!'
            )
        if (len(set(item['id'] for item in ingredients)) != len(ingredients)):
            raise serializers.ValidationError(
                'There can be no duplicate ingredients!'
            )

        return super().validate(data)

    def validate_image(self, image):
        """Checking image."""
        if not image:
            raise serializers.ValidationError('Add recipe image!')

        return image

    @staticmethod
    def create_ingredient_in_recipe_objects(ingredients, recipe):
        """Creates ingredients for a recipe."""
        ingredient_list = [
            IngredientInRecipe(
                recipe=recipe,
                ingredient=ingredient['id'],
                amount=ingredient['amount']
            ) for ingredient in ingredients
        ]
        IngredientInRecipe.objects.bulk_create(ingredient_list)

    @atomic
    def create(self, validated_data):
        """Creates a recipe."""
        current_user = self.context['request'].user
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data, author=current_user)
        recipe.tags.set(tags)
        recipe.save()
        self.create_ingredient_in_recipe_objects(ingredients, recipe)

        return recipe

    @atomic
    def update(self, instance, validated_data):
        """Updates recipe."""
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance.tags.clear()
        instance.tags.set(tags)
        IngredientInRecipe.objects.filter(recipe=instance).delete()
        self.create_ingredient_in_recipe_objects(ingredients, instance)

        return super().update(instance, validated_data)

    def to_representation(self, instance):
        serializer = RecipeReadSerializer(
            instance, context={'request': self.context.get('request')}
        )

        return serializer.data


class FavoriteSerializer(serializers.ModelSerializer):
    """Serializer for model 'Favorite'."""

    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all()
    )
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )

    class Meta:
        model = Favorite
        fields = ('recipe', 'user')
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=('recipe', 'user'),
                message='The recipe has already been added to your list.'
            )
        ]

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return ShortRecipeSerializer(instance.recipe, context=context).data


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Serializer for model 'ShoppingCar'."""

    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all()
    )
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )

    class Meta:
        model = ShoppingCart
        fields = ('recipe', 'user')
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=('recipe', 'user'),
                message='The recipe has already been added to your list.'
            )
        ]

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return ShortRecipeSerializer(instance.recipe, context=context).data
