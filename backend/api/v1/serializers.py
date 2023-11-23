"""
Module for creating, configuring and managing 'recipes' app serializers
"""
import webcolors
from rest_framework import serializers, validators
from django.db.transaction import atomic
from drf_extra_fields.fields import Base64ImageField

from core.constants import ConstantRecipes
from core.service import create_IngredientInRecipe_objects, in_list
from users.serializers import CustomUserSerializer
from recipes.models import (
    Ingredient,
    Tag,
    Recipe,
    IngredientInRecipe,
    Favorite,
    ShoppingCart
)


class Hex2NameColor(serializers.Field):
    """Converts a color code to a color name."""

    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError(
                {'Color name': 'There is no name for this color'}
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
    """ Serializer for model IngredientInRecipe. """

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
        validators = (
            validators.UniqueTogetherValidator(
                queryset=IngredientInRecipe.objects.all(),
                fields=('ingredient', 'recipe')
            ),
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
    ingredients = serializers.SerializerMethodField(
        method_name='get_ingredients',
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

    def get_ingredients(self, obj):
        """Gets a list of ingredients for a recipe."""
        ingredients = IngredientInRecipe.objects.filter(recipe=obj)

        return IngredientInRecipeSerializer(ingredients, many=True).data

    def get_is_favorited(self, obj):
        """Checking whether the recipe is in your favorites."""
        return in_list(obj, Favorite)

    def get_is_in_shopping_cart(self, obj):
        """Checking whether the recipe is in the shopping cart."""
        return in_list(obj, ShoppingCart)


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
        max_value=ConstantRecipes.MAX_COOKING_TIME
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
                {'tags': 'You must select at least one tag.'}
            )
        if len(tags) != len(set(tags)):
            raise serializers.ValidationError(
                {'tags': 'Tags should not be repeated!'}
            )

        # Checking ingredients.
        ingredients = data.get('ingredients')
        if not ingredients:
            raise serializers.ValidationError(
                {'ingredients': 'The ingredients field cannot be empty.'}
            )
        for ingredient in ingredients:
            ingredient_name = ingredient['id']
        if int(ingredient['amount']) <= 0:
            raise serializers.ValidationError(
                {'ingredients': f'Incorrect quantity for {ingredient_name}'}
            )
        if not isinstance(ingredient['amount'], int):
            raise serializers.ValidationError(
                {'ingredients': 'must be a whole number!'}
            )
        if (len(set(item["id"] for item in ingredients)) != len(ingredients)):
            raise serializers.ValidationError(
                {'ingredients': 'There can be no duplicate ingredients!'}
            )

        # Checking the cooking time.
        cooking_time = data.get('cooking_time')
        if not cooking_time:
            raise serializers.ValidationError(
                {'cooking_time': 'Add cooking time to recipe.'}
            )
        if cooking_time < ConstantRecipes.MIN_COOKING_TIME:
            raise serializers.ValidationError(
                {'Cooking time': 'Cooking time must be >=1 minute.'}
            )
        if cooking_time > ConstantRecipes.MAX_COOKING_TIME:
            raise serializers.ValidationError(
                {'Cooking time': 'Cooking time exceeds all norms!'}
            )

        # Checking recipe image.
        image = data.get('image')
        if not image:
            raise serializers.ValidationError(
                {'image': 'Add recipe images.'}
            )

        return super().validate(data)

    @atomic
    def create(self, validated_data):
        """Creates a recipe."""
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        recipe.save()
        create_IngredientInRecipe_objects(ingredients, recipe)

        return recipe

    @atomic
    def update(self, instance, validated_data):
        """Updates recipe."""
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance.tags.clear()
        instance.tags.set(tags)
        IngredientInRecipe.objects.filter(recipe=instance).delete()
        create_IngredientInRecipe_objects(ingredients, instance)

        return super().update(instance, validated_data)

    def to_representation(self, instance):
        serializer = RecipeReadSerializer(
            instance, context={'request': self.context.get('request')}
        )

        return serializer.data
