"""
Constants.
"""

# CustomPagination
MAX_PAGE_SIZE = 6


class HelpTextRecipes():
    """Help text for recipes app models in admin zone."""

    # Ingredient model.
    INGREDIENT_NAME = 'Enter a unique ingredient name.'
    MEASUREMENT_UNIT = 'Enter the unit of measurement for the ingredient.'
    # Tag model.
    TAG_NAME = 'Enter a unique tag name.'
    TAG_COLOR = 'Select a tag color.'
    TAG_SLUG = 'Enter a unique tag slug.'
    # Recipe model.
    RECIPE_NAME = 'Enter a unique recipe name.'
    RECIPE_AUTHOR = 'Enter the unique name of the recipe author.'
    RECIPE_TEXT = 'Add a recipe description.'
    RECIPE_TAG = 'Add recipe tags.'
    RECIPE_INGREDIENT = 'Add ingredients to recipe.'
    RECIPE_COOKING_TIME = (
        'Enter the cooking time for the recipe in minutes.'
    )
    # IngredientInRecipe model.
    AMOUNT = ('Please indicate the quantity of ingredients.')


class HelpTextUsers():
    """Help text for users app models in admin zone."""

    # CustomUser model.
    HELP_EMAIL = "Enter the user's unique email address."
    HELP_PASSWORD = 'Enter your unique user password.'
    HELP_USERNAME = 'Enter a unique username.'
    HELP_FIRST_NAME = 'Enter your name.'
    HELP_LAST_NAME = 'Enter your last name.'


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
    INCORRECT_AMOUNT = 0
