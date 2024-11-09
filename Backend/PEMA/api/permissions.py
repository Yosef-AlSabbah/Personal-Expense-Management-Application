from rest_framework.permissions import BasePermission


class IsAdminOrForbidden(BasePermission):
    message = "Access to API documentation is restricted to admin users only."

    def has_permission(self, request, view):
        return request.user and request.user.is_staff
