from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


class RegexUsername(RegexValidator):
    """Checking the username for invalid characters."""

    regex = '^[\w.@+-]+$'
    message = 'The username contains invalid characters.',


def validate_username(value):
    """It is forbidden to use 'me' as a nickname."""

    if value == "me":
        raise ValidationError(
            {'username': "You cannot use 'me' as the username."}
        )
    return value
