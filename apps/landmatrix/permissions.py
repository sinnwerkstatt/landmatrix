from typing import cast

from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import BasePermission

from apps.accounts.models import User, UserRole


class IsAnybodyOrHigher(BasePermission):
    def has_permission(self, request, view):
        return is_anybody_or_higher(request.user)


class IsReporterOrHigher(BasePermission):
    def has_permission(self, request, view):
        return is_reporter_or_higher(request.user)


class IsEditorOrHigher(BasePermission):
    def has_permission(self, request, view):
        return is_editor_or_higher(request.user)


class IsAdministrator(BasePermission):
    def has_permission(self, request, view):
        return is_admin(request.user)


def has_role_or_higher(role: UserRole, user: User) -> bool:
    return not user.is_anonymous and (
        user.is_superuser or cast(UserRole, user.role) >= role
    )


def is_anybody_or_higher(user: User | AnonymousUser) -> bool:
    return has_role_or_higher(UserRole.ANYBODY, user)


def is_reporter_or_higher(user: User | AnonymousUser) -> bool:
    return has_role_or_higher(UserRole.REPORTER, user)


def is_editor_or_higher(user: User | AnonymousUser) -> bool:
    return has_role_or_higher(UserRole.EDITOR, user)


def is_admin(user: User | AnonymousUser) -> bool:
    return has_role_or_higher(UserRole.ADMINISTRATOR, user)
