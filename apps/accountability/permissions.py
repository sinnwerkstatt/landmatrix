from rest_framework.permissions import BasePermission

from apps.accounts.models import User, UserRole

SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']


class IsReporterOrHigher(BasePermission):
    def has_permission(self, request, view):
        user: User = request.user  # type: ignore
        return bool(user and not user.is_anonymous and user.role >= UserRole.REPORTER)


class IsReporterOrHigherOrReadonly(BasePermission):
    def has_permission(self, request, view):
        user: User = request.user  # type: ignore
        reporter_or_higher = user and not user.is_anonymous and user.role >= UserRole.REPORTER
        if (request.method in SAFE_METHODS or reporter_or_higher):
            return True
        return False 


class IsOwnerOrEditorOrReadonly(BasePermission):
    def has_object_permission(self, request, view, obj):
        user: User = request.user

        if request.method in SAFE_METHODS:
            return True
               
        if obj.owner == user or user in obj.editors.all():
            return True

        return False


class IsUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        user: User = request.user
        if obj.user == user:
            return True
        return False


class IsAdministrator(BasePermission):
    def has_permission(self, request, view):
        user: User = request.user  # type: ignore
        return bool(
            user and not user.is_anonymous and user.role >= UserRole.ADMINISTRATOR
        )