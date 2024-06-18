from rest_framework.permissions import BasePermission

from apps.accounts.models import User, UserRole


class IsReporterOrHigher(BasePermission):
    def has_permission(self, request, view):
        user: User = request.user  # type: ignore
        return bool(user and not user.is_anonymous and user.role >= UserRole.REPORTER)


class IsAdministrator(BasePermission):
    def has_permission(self, request, view):
        user: User = request.user  # type: ignore
        return bool(
            user and not user.is_anonymous and user.role >= UserRole.ADMINISTRATOR
        )
