from django.core.exceptions import ValidationError


def validate_username(value):
    """It is forbidden to use 'me' as a nickname."""

    if value == "me":
        raise ValidationError(
            {'username': "You cannot use 'me' as the username."}
        )
    return value
