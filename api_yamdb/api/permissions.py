from rest_framework import permissions


class ForAdminOthersAuthorizedOnlyRead(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated and request.user.is_admin)











#     def has_permission(self, request, view):
#         return (request.method in permissions.SAFE_METHODS
#                 or request.user and request.user.is_authenticated)
#
#     def has_object_permission(self, request, view, obj):
#         return (request.method in permissions.SAFE_METHODS
#                 or obj.author == request.user)

#             request.method in SAFE_METHODS or
#             (request.user and request.user.is_authenticated)
#             (request.user and request.user.is_staff)
#             user.is_authenticated and user.is_admin
