"""
Module for creating, configuring and managing `users' app models.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """ CustomUser model class """

    email = models.EmailField(
        verbose_name='Email',
        max_length=20,
        unique=True
    )
    password = models.CharField(
        verbose_name='Password',
        max_length=20,
        blank=False,
        null=False,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'password']

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

    def __str__(self):
        return f'{self.get_full_name()}: {self.email}'


class Subscribe(models.Model):
    """ Model of Subscribe of one user to another. """

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Subscriber',
    )
    following = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Tracked user',
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=['following', 'user'],
                name='unique_follow'
            ),
        )
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'

    def __str__(self):
        return f'{self.user.username} follows the {self.author.username}'
