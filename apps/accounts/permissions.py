from rest_framework.permissions import BasePermission

from apps.accounts.models import UserRole


class IsReporterOrHigher(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.role >= UserRole.REPORTER)
