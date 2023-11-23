from recipes.models import IngredientInRecipe


@staticmethod
def create_IngredientInRecipe_objects(ingredients, recipe):
    """Creates ingredients for a recipe."""
    ingredient_list = [
        IngredientInRecipe(
            recipe=recipe,
            ingredient=ingredient['id'],
            amount=ingredient['amount']
        ) for ingredient in ingredients
    ]
    ingredient_list.sort(key=lambda item: item.ingredient.name)
    IngredientInRecipe.objects.bulk_create(ingredient_list)
