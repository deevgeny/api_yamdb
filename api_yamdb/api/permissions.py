from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class RegisterUser(permissions.BasePermission):
    """Allow initial user registration."""

    def has_permission(self, request, view):
        return True


class AdminRegisterUser(permissions.BasePermission):
    """Allow administrator to register users."""

    def has_permission(self, request, view):
        return request.user.role == User.ADMIN
