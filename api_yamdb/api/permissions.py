from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class ForAdminOthersAuthorizedOnlyRead(permissions.BasePermission):
    """
    Post and Delete method permission for authenticated admin user.
    For the other only read.
    """

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated and request.user.is_admin)


class AllowPostMethodForAnonymousUser(permissions.BasePermission):
    """Post method permission for anonymous user."""

    def has_permission(self, request, view):
        return request.method == "POST" and request.user.is_anonymous


class OnlyAuthenticatedAdminUser(permissions.BasePermission):
    """Allow any type of request for authenticated admin user."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.ADMIN
            or request.user.is_superuser
        )


class AccessPersonalProfileData(permissions.BasePermission):
    """Allow authenticated users to access personal profile."""

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user.username == obj.username
