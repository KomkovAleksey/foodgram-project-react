"""
Module for creating, configuring and managing `users' app viewsets
"""
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from .models import Follow
from api.v1.pagination import CustomPagination
from api.v1.permissions import IsAdminUserOrReadOnly
from .serializers import (
    CustomUserSerializer,
    SubscriptionSerializer
)

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    """Vievset for working with users."""

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = CustomPagination
    permission_classes = (IsAdminUserOrReadOnly,)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated],
    )
    def subscriptions(self, request):
        subscribed_to = self.paginate_queryset(
            User.objects.filter(following__user=request.user)
        )
        serializer = SubscriptionSerializer(
            subscribed_to,
            many=True,
            context={"request": request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated],
    )
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(User, pk=id)
        Subscription = Follow.objects.filter(user=user, author=author)

        if request.method == 'POST':
            serializer = SubscriptionSerializer(
                author, data=request.data, context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            if Subscription.exists():
                return Response(
                    {'subscribe': 'You are already subscribed to this user.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if user == author:
                return Response(
                    {'subscribe': "You can't subscribe to yourself."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            Follow.objects.create(user=user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            if not Subscription.exists():
                return Response(
                    status=status.HTTP_400_BAD_REQUEST
                )
            Subscription.delete()
            return Response(
                status=status.HTTP_204_NO_CONTENT
            )

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        """View subscriptions to authors. My subscriptions."""
        user = request.user
        serializer = CustomUserSerializer(user, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
