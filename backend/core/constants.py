"""
Constants.
"""
from django.utils.translation import gettext_lazy as _


class Help_text_recipes():
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

    RECIPE_COOKING_TIME = _('Enter the cooking time for the recipe in minutes.')


class Help_text_users():
    """Help text for users app models in admin zone."""

    # CustomUser model.
    HELP_EMAIL = _("Enter the user's unique email address.")

    HELP_PASSWORD = _('Enter your unique user password.')

    HELP_USERNAME = _('Enter a unique username.')

    HELP_FIRST_NAME = _('Enter your name.')

    HELP_LAST_NAME = _('Enter your last name.')
