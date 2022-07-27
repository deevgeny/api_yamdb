from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class AllowPostMethod(permissions.BasePermission):
    """Post method permission."""

    def has_permission(self, request, view):
        return request.method == "POST"


class AdminRegisterUser(permissions.BasePermission):
    """Allow administrator to register users."""

    def has_permission(self, request, view):
        return request.user.role == User.ADMIN and request.method == "POST"
