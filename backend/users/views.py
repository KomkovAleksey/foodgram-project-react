"""
Module for creating, configuring and managing `users' app viewsets
"""
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from .models import Follow
from .serializers import (
    CustomUserSerializer,
    SubscriptionSerializer
)

User = get_user_model()


def get_author(id):
    return get_object_or_404(User, id=id)


class CustomUserViewSet(UserViewSet):
    """Vievset for working with users."""

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = PageNumberPagination

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated],
    )
    def subscriptions(self, request):
        subscribed_to = self.paginate_queryset(
            User.objects.filter(author__follower=request.user)
        )
        serializer = SubscriptionSerializer(subscribed_to, many=True)
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated],
    )
    def subscribe(self, request, id):
        """ Subscribe to the user. """
        author = get_author(id)
        follower = request.user

        serializer = SubscriptionSerializer(
            author,
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save

        subscription, created = Follow.objects.get_or_create(
            follower=follower,
            author=author,
        )

        if created:
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        else:
            message = {'You are already following this author'}

            return Response(
                message, status=status.HTTP_400_BAD_REQUEST
            )

    @subscribe.mapping.delete
    def delete_subscribe(self, request, id):
        """Unsubscribe from a user."""
        author = get_author(id)
        subscription = get_object_or_404(
            Follow,
            follower=request.user,
            author=get_author(id),
        )
        subscription.delete()
        message = {f'You have unsubscribed from this {author}'}

        return Response(message, status=status.HTTP_204_NO_CONTENT)
