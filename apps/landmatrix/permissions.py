from rest_framework.permissions import BasePermission

from apps.accounts.models import UserRole, User


class IsReporterOrHigher(BasePermission):
    def has_permission(self, request, view):
        user: User = request.user
        return bool(user and not user.is_anonymous and user.role >= UserRole.REPORTER)
