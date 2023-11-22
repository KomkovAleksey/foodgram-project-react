"""
Module for creating, configuring and managing `users' app models.
"""
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.db import models

from core.constants import HelpTextUsers, ConstantUsers
from core.validators import validate_username


class CustomUser(AbstractUser):
    """CustomUser model class."""

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    CUSTOM_USER_ROLE_CHOICES = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    ]

    role = models.CharField(
        verbose_name='User Role',
        choices=CUSTOM_USER_ROLE_CHOICES,
        default=USER,
        max_length=16,
    )

    email = models.EmailField(
        verbose_name='Email address',
        max_length=ConstantUsers.MAX_EMAIL_LENGTH,
        unique=True,
        help_text=HelpTextUsers.HELP_EMAIL,
    )
    username = models.CharField(
        verbose_name='Username',
        max_length=ConstantUsers.MAX_USER_LENGTH,
        unique=True,
        help_text=HelpTextUsers.HELP_USERNAME,
        validators=(
            validate_username,
            UnicodeUsernameValidator(),
        )
    )
    first_name = models.CharField(
        verbose_name='Name',
        max_length=ConstantUsers.MAX_USER_LENGTH,
        help_text=HelpTextUsers.HELP_FIRST_NAME,
    )
    last_name = models.CharField(
        verbose_name='Surname',
        max_length=ConstantUsers.MAX_USER_LENGTH,
        help_text=HelpTextUsers.HELP_LAST_NAME,
    )
    password = models.CharField(
        verbose_name='Password',
        max_length=ConstantUsers.MAX_PASSWORD_LENGTH,
        blank=False,
        null=False,
        help_text=HelpTextUsers.HELP_PASSWORD,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
    ]

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ('username',)
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email'
            )
        ]

    @property
    def is_admin_or_super_user(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    def __str__(self):
        return f'{self.get_full_name()}: {self.email}'


class Follow(models.Model):
    """Subscribe to another user model."""

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Subscriber',
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Author',
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=['author', 'user'],
                name='unique_follow'
            ),
        )
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'

    def clean(self):
        """Subscription validation."""
        if self.user == self.following:
            raise ValidationError("You can't subscribe to yourself.")
        if Follow.objects.filter(
                user=self.user, following=self.following).exists():
            raise ValidationError(
                'You cannot subscribe to the same author twice.'
            )

        return super().save(self)

    def __str__(self):
        return f'{self.user.username} follows the {self.author.username}'
