"""
Constants.
"""
from django.utils.translation import gettext_lazy as _


class HelpTextRecipes():
    """Help text for recipes app models in admin zone."""

    # Ingredient model.
    INGREDIENT_NAME = _('Enter a unique ingredient name.')
    MEASUREMENT_UNIT = _('Enter the unit of measurement for the ingredient.')
    # Tag model.
    TAG_NAME = _('Enter a unique tag name.')
    TAG_COLOR = _('Select a tag color.')
    TAG_SLUG = _('Enter a unique tag slug.')
    # Recipe model.
    RECIPE_NAME = _('Enter a unique recipe name.')
    RECIPE_AUTHOR = _('Enter the unique name of the recipe author.')
    RECIPE_TEXT = _('Add a recipe description.')
    RECIPE_TAG = _('Add recipe tags.')
    RECIPE_INGREDIENT = _('Add ingredients to recipe.')
    RECIPE_COOKING_TIME = _(
        'Enter the cooking time for the recipe in minutes.'
    )
    # IngredientInRecipe model.
    AMOUNT = _('Please indicate the quantity of ingredients.')


class HelpTextUsers():
    """Help text for users app models in admin zone."""

    # CustomUser model.
    HELP_EMAIL = _("Enter the user's unique email address.")
    HELP_PASSWORD = _('Enter your unique user password.')
    HELP_USERNAME = _('Enter a unique username.')
    HELP_FIRST_NAME = _('Enter your name.')
    HELP_LAST_NAME = _('Enter your last name.')


class ConstantUsers():
    """Constants for users app models."""

    # CustomUser model.
    MAX_EMAIL_LENGTH = 254
    MAX_USER_LENGTH = 150
    MAX_PASSWORD_LENGTH = 100


class ConstantRecipes():
    """Constants for recipes app models."""

    MAX_NAME_LENGTH = 200
    # Ingredient model.
    MAX_MEASUREMENT_UNIT = 256
    # Tag model.
    MAX_SLUG_LENGTH = 64
    # Recipe model.
    MIN_COOKING_TIME = 1
    MAX_COOKING_TIME = 9000
    # IngredientInRecipe model.
    MIN_AMOUNT = 1
    MAX_AMOUNT = 9000


class ErrorText():
    """Error text."""

    MIN_AMOUNT_ERROR = {'ingredient': 'The number of ingredients must be >=1.'}
    MAX_AMOUNT_ERROR = {
        'ingredient': 'The quantity of ingredients has reached the limit!'
    }
    MIN_COOKING_ERROR = {'Cooking time': 'Cooking time must be >=1 minute.'}
    MAX_COOKING_ERROR = {'Cooking time': 'Cooking time exceeds all norms!'}
    DELETE_NON_EXIST_RECIPE_ERROR = {
        'recipe': 'You are trying to delete a recipe that does not exist.'
    }
    ADD_NON_EXIST_RECIPE_ERROR = {
        'add_recipe': 'You are trying to add a non-existent recipe!'
    }
    ADD_RECIPE_TO_THE_LIST_ERROR = {
        'add_recipe': 'The recipe has already been added to list.'
    }
