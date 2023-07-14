"""
Serializers for 'api' application.
"""
from django.db import transaction
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers, validators

import users.serializers as users
from recipes.models import (Favorite,
                            Ingredient,
                            Tag,
                            IngredientsInRecipe,
                            Recipe,
                            ShoppingCart,
                            )


class ShortRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели `Recipe`"""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('__all__',)


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для модели 'Ingredient'."""

    class Meta:
        model = Ingredient
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для модели 'Tag'."""

    class Meta:
        model = Tag
        fields = '__all__'


class TagField(serializers.SlugRelatedField):
    """Сериализатор для слага модели 'Tag'."""

    def to_representation(self, value):
        request = self.context.get('request')
        context = {'request': request}
        serializer = TagSerializer(value, context=context)
        return serializer.data


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для 'IngredientInRecipe'."""

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientsInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')

    validators = (
        validators.UniqueTogetherValidator(
            queryset=IngredientsInRecipe.objects.all(),
            fields=('ingredient', 'recipe')
        ),
    )

    def __str__(self):
        return f'{self.ingredient} in {self.recipe}'


class AddIngredientSerializer(serializers.ModelSerializer):
    """Класс определяет сериализатор для `IngredientsInRecipe`."""

    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientsInRecipe
        fields = ('id', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для 'Recipe'."""

    author = users.CurrentUserSerializer()
    tags = TagField(
        slug_field='id', queryset=Tag.objects.all(), many=True
    )
    ingredients = IngredientInRecipeSerializer(
        source='ingredient_in_recipe',
        read_only=True, many=True
    )
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField(
        method_name='get_is_favorited'
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        method_name='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'name',
            'author',
            'ingredients',
            'image',
            'text',
            'cooking_time',
            'is_favorited',
            'is_in_shopping_cart'
        )

    def in_list(self, obj, model):
        """Проверка - находится ли обьект в модели"""

        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return model.objects.filter(user=request.user, recipe=obj).exists()

    def get_is_favorited(self, obj):
        """Проверка - находится ли рецепт в избранном."""

        return self.in_list(obj, Favorite)

    def get_is_in_shopping_cart(self, obj):
        """Проверка - находится ли рецепт в списке  покупок."""

        return self.in_list(obj, ShoppingCart)


class AddRecipeSerializer(serializers.ModelSerializer):
    """ Сериализатор для  добавления и изменения рецептов."""

    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    ingredients = AddIngredientSerializer(many=True)
    image = Base64ImageField(max_length=None)

    class Meta:
        model = Recipe
        fields = (
            'tags',
            'name',
            'ingredients',
            'image',
            'text',
            'cooking_time'
        )

    def to_representation(self, instance):
        serializer = RecipeSerializer(instance)
        return serializer.data

    def create_ingredients(self, ingredients, recipe):
        """ Создает объекты `IngredientsInRecipe` для списка ингредиентов"""

        for ingredient in ingredients:
            amount = ingredient['amount']
            ingredient = ingredient['id']
            ingredients, created = IngredientsInRecipe.objects.get_or_create(
                recipe=recipe,
                ingredient=ingredient,
                amount=amount
            )

    @transaction.atomic
    def create(self, validated_data):
        """Создаёт рецепт."""

        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        recipe.save()
        self.create_ingredients(ingredients, recipe)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        """Обновляет рецепт."""

        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance.ingredients.clear()
        self.create_ingredients(ingredients, instance)
        instance.tags.clear()
        instance.tags.set(tags)
        return super().update(instance, validated_data)

    def validate(self, data):
        """Проверка вводных данных при создании/редактировании рецепта."""

        ings = data['ingredients']
        if not ings:
            raise serializers.ValidationError(
                'Поле с ингредиентами не может быть пустым'
            )
        unique_ings = []
        for ingredient in ings:
            name = ingredient['id']
            if int(ingredient['amount']) <= 0:
                raise serializers.ValidationError(
                    f'Не корректное количество для {name}'
                )
            if not isinstance(ingredient['amount'], int):
                raise serializers.ValidationError(
                    'Количество ингредиентов должно быть целым числом'
                )
            if name not in unique_ings:
                unique_ings.append(name)
            else:
                raise serializers.ValidationError(
                    'В рецепте не может быть повторяющихся ингредиентов'
                )
        return data

    def validate_cooking_time(self, data):
        """Проверка время приготовления."""

        if data <= 0:
            raise serializers.ValidationError(
                'Время приготовления не может быть меньше 1 минуты'
            )
        return data
