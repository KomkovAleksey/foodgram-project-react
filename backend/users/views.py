"""
Module for creating, configuring and managing `users' app viewsets
"""
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, filters, permissions, mixins
from rest_framework.pagination import PageNumberPagination
from djoser.views import UserViewSet

from .models import CustomUser
from .serializers import (CustomUserSerializer,
                          SubscribeSerializer,
                          SubscriptionSerializer
                          )


class FollowViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    viewsets.GenericViewSet):

    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return self.request.user.follower.all()

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def subscribe(self, request, id):
        """Subscribe to user."""
        author = get_object_or_404(CustomUser, id=id)

        serializer = SubscribeSerializer(
            author,
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)

        subscription, created = Subscription.objects.get_or_create(
            follower=request.user,
            author=author,
        )

        if created:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            message = {"Вы уже подписаны на этого пользователя"}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        
    @subscribe.mapping.delete
    def delete_subscribe(self, request, id):
        """ Unsubscribe from the user. """
        author = get_object_or_404(CustomUser, id=id)

        subscription = get_object_or_404(
            Subscription,
            follower=request.user,
            author=author,
        )
        subscription.delete()
        message = {f"Вы отписались от {author}"}
        return Response(message, status=status.HTTP_204_NO_CONTENT)
