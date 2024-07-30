from typing import Type

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APIClient

from apps.accounts.models import User, UserRole
from apps.landmatrix.models.new import DealHull

UserModel: Type[User] = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def anybody2(db):
    return UserModel.objects.create_user(
        username="anybody2",
        password="love2be",
        role=UserRole.ANYBODY,
    )


@pytest.fixture
def reporter2(db):
    return UserModel.objects.create_user(
        username="reporter2",
        password="love2report",
        role=UserRole.REPORTER,
    )


@pytest.fixture
def editor2(db):
    return UserModel.objects.create_user(
        username="editor2",
        password="love2edit",
        role=UserRole.EDITOR,
    )


@pytest.fixture
def admin2(db):
    return UserModel.objects.create_user(
        username="admin2",
        password="love2administrate",
        role=UserRole.ADMINISTRATOR,
    )


@pytest.fixture
def superuser2(db):
    return UserModel.objects.create_superuser(
        username="superuser2",
        password="superduper",
    )


@pytest.fixture
def deals(db) -> list[DealHull]:
    N_DEALS = 2
    return DealHull.objects.bulk_create(
        [DealHull(first_created_at=timezone.now()) for _ in range(N_DEALS)]
    )
