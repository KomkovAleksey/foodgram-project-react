"""
Access rights management module..
"""
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrReadOnly(BasePermission):
    """Author rights or read only."""

    message = 'Author rights required!'

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
    """Administrator rights or read only."""

    message = 'Administrator rights required!'

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin_or_super_user
            or request.method in SAFE_METHODS
        )
