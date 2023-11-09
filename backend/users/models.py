"""
Module for creating, configuring and managing `users' app models.
"""
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class CustomUser(AbstractUser):
    """CustomUser model class."""

    email = models.EmailField(
        verbose_name='Email',
        max_length=254,
        unique=True,
        help_text="Enter the user's unique email address.",
    )
    username = models.CharField(
        verbose_name='Username',
        max_length=150,
        unique=True,
        help_text='Enter a unique username.',
    )
    first_name = models.CharField(
        verbose_name='Name',
        max_length=150,
        help_text='Enter your name.',
    )
    last_name = models.CharField(
        verbose_name='Surname',
        max_length=150,
        help_text='Enter your last name.',
    )
    password = models.CharField(
        verbose_name='Password',
        max_length=50,
        blank=False,
        null=False,
        help_text='Enter your unique user password.',
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
        ordering = ('-username',)
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email'
            )
        ]

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
