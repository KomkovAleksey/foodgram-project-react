"""
Constants.
"""


class Help_text_recipes():
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

    RECIPE_COOKING_TIME = 'Enter the cooking time for the recipe in minutes.'


class Help_text_users():
    """Help text for users app models in admin zone."""

    # CustomUser model.
    HELP_EMAIL = "Enter the user's unique email address."

    HELP_PASSWORD = 'Enter your unique user password.'

    HELP_USERNAME = 'Enter a unique username.'

    HELP_FIRST_NAME = 'Enter your name.'

    HELP_LAST_NAME = 'Enter your last name.'
