"""
"""
from rest_framework import serializers


def validate_tags(self, data):
    """ Checking recipe tags. """
    tags = data['tags']
    if not tags:
        raise serializers.ValidationError(
            'You must select at least one tag for the recipe.'
            )
    if len(data) != len(set(data)):
        raise serializers.ValidationError('Tags should not be repeated.')

    return data


def validate_ingredients(self, data):
    """ Checking recipe ingredients. """
    ingredients = data['ingredients']
    if not ingredients:
        raise serializers.ValidationError(
            'The ingredients field cannot be empty.'
        )
    unique_ingredients = []
    for ingredient in ingredients:
        name = ingredient['id']
        if int(ingredient['amount']) <= 0:
            raise serializers.ValidationError(
                f'Incorrect quantity for {name}'
                )
        if not isinstance(ingredient['amount'], int):
            raise serializers.ValidationError(
                'The number of ingredients must be a whole number.'
                )
        if name not in unique_ingredients:
            unique_ingredients.append(name)
        else:
            raise serializers.ValidationError(
                'There can be no duplicate ingredients in the recipe.'
            )

        return data


def validate_cooking_time(self, data):
    """ Checking the cooking time. """
    cooking_time = data['cooking_time']
    if cooking_time <= 0:
        raise serializers.ValidationError(
            'Cooking time must be >=1 minute.'
            )
    if cooking_time >= 1440:
        raise serializers.ValidationError(
            'Cooking time exceeds all norms!'
            )

    return data
