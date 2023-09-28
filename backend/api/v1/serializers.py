"""
Serializers
"""
import base64

import webcolors
from rest_framework import serializers, validators
from django.core.files.base import ContentFile

from .validators import (validate_tags, 
                         validate_cooking_time,
                         validate_ingredients,
                         )
from users.serializers import CustomUserSerializer
from recipes.models import (Ingredient,
                            Tag,
                            Recipe,
                            IngredientInRecipe,
                            Favorite,
                            ShoppingCart
                            )


class Hex2NameColor(serializers.Field):
    """ """
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError(
                'There is no name for this color'
                )


class Base64ImageField(serializers.ImageField):
    """ Base64 string decoding. """

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):
    """ Serializer for model Tag. """

    color = Hex2NameColor()

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)


class IngredientSerializer(serializers.ModelSerializer):
    """ Serializer for model Ingredient. """

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    """ Serializer for model IngredientInRecipe. """

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')

    validators = (
        validators.UniqueTogetherValidator(
            queryset=IngredientInRecipe.objects.all(),
            fields=('ingredient', 'recipe')
        ),
    )


class RecipeReadSerializer(serializers.ModelSerializer):
    """ Serializer for model 'Recipe' on GET requests. """

    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientSerializer(many=True)
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id'
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

    def get_is_favorited(self, obj):
        """ Checking to see if the recipe is in your favorites. """
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False

        return Favorite.objects.filter(user=request.user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        """ Checking to see if the recipe is on the shopping cart list. """
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False

        return ShoppingCart.objects.filter(
            user=request.user, recipe=obj).exists()


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    """ Serializer for model 'Recipe' on POST, PATCH, DELETE requests. """

    author = CustomUserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(many=True)
    ingredients = IngredientSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id'
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

        validators = [
            validate_tags,
            validate_cooking_time,
            validate_ingredients,
        ]

    def create_IngredientInRecipe_objects(self, ingredients, recipe):
        """ """
        for ingredient in ingredients:
            IngredientInRecipe.objects.get_or_create(
                recipe=recipe,
                ingredient=ingredient['id'],
                amount=ingredient['amount']
            )

    def create(self, validated_data):
        """ Creates a recipe. """
        author = self.context.get('request').user
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(author - author, **validated_data)
        recipe.tags.set(tags)
        recipe.save()
        self.get_IngredientInRecipe_objects(ingredients, recipe)

        return recipe

    def update(self, instance, validated_data):
        """ Updates recipe. """
        instance.author = validated_data.get('author', instance.author)
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        IngredientInRecipe.objects.filter(recept=instance).delete()
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        instance.tags.set(tags)
        self.get_IngredientInRecipe_objects(ingredients, instance)
        instance.save()

        return instance


class FavoriteSerializer(serializers.ModelSerializer):
    """ Serializer for model 'Favorite'. """

    class Meta:
        model = Favorite
        fields = ['user', 'recipe']
        validators = [
            validators.UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=['user', 'recipe'],
                message='You have already added the recipe to your favorites.'
            )
        ]


class ShoppingCartSerializer(serializers.ModelSerializer):
    """ Serializer for model 'ShoppingCart'. """

    class Meta:
        model = ShoppingCart
        fields = ['user', 'recipe']
        validators = [
            validators.UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=['user', 'recipe'],
                message=(
                    'You have already added the recipe to your shopping list.'
                    )
            )
        ]
