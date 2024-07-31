from django.contrib.auth.models import AnonymousUser

from apps.accounts.models import User, UserRole
from .permissions import (
    is_anybody_or_higher,
    is_reporter_or_higher,
    is_editor_or_higher,
    is_admin,
)

ANONYMOUS = AnonymousUser()

ANYBODY = User(role=UserRole.ANYBODY)
REPORTER = User(role=UserRole.REPORTER)
EDITOR = User(role=UserRole.EDITOR)
ADMINISTRATOR = User(role=UserRole.ADMINISTRATOR)

STAFF = User(is_staff=True)
SUPERUSER = User(is_superuser=True)


def test_is_anybody_or_higher():
    assert not is_anybody_or_higher(ANONYMOUS)

    assert is_anybody_or_higher(ANYBODY)
    assert is_anybody_or_higher(REPORTER)
    assert is_anybody_or_higher(EDITOR)
    assert is_anybody_or_higher(ADMINISTRATOR)

    assert is_anybody_or_higher(STAFF)
    assert is_anybody_or_higher(SUPERUSER)


def test_is_reporter_or_higher():
    assert not is_reporter_or_higher(ANONYMOUS)

    assert not is_reporter_or_higher(ANYBODY)
    assert is_reporter_or_higher(REPORTER)
    assert is_reporter_or_higher(EDITOR)
    assert is_reporter_or_higher(ADMINISTRATOR)

    assert not is_reporter_or_higher(STAFF)
    assert is_reporter_or_higher(SUPERUSER)


def test_is_editor_or_higher():
    assert not is_editor_or_higher(ANONYMOUS)

    assert not is_editor_or_higher(ANYBODY)
    assert not is_editor_or_higher(REPORTER)
    assert is_editor_or_higher(EDITOR)
    assert is_editor_or_higher(ADMINISTRATOR)

    assert not is_editor_or_higher(STAFF)
    assert is_editor_or_higher(SUPERUSER)


def test_is_admin():
    assert not is_admin(ANONYMOUS)

    assert not is_admin(ANYBODY)
    assert not is_admin(REPORTER)
    assert not is_admin(EDITOR)
    assert is_admin(ADMINISTRATOR)

    assert not is_admin(STAFF)
    assert is_admin(SUPERUSER)
