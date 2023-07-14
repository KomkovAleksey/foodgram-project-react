"""
Access rights for users.
"""
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrReadOnly(BasePermission):
    """Права автора или только чтение."""

    message = 'Нужны права автора.'

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user == obj.author
        )


class IsAdminUserOrReadOnly(BasePermission):
    """Права администратора или только чтение."""

    message = 'Нужны права администратора.'

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin_or_super_user
            or request.method in SAFE_METHODS
        )
