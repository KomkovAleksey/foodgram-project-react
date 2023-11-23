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


def in_list(self, obj, model):
    """Checking whether the recipe is on the list."""
    request = self.context.get('request')
    if request is None or request.user.is_anonymous:
        return False

    return model.objects.filter(user=request.user, recipe=obj).exists()
