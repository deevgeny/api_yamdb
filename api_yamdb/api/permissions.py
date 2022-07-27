from rest_framework import permissions


class RegisterUser(permissions.BasePermission):
    """"""

    def has_permission(self, request, view):
        return True
