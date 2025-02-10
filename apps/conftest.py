from typing import Type

import pytest

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APIClient

from apps.accounts.models import User, UserRole
from apps.landmatrix.models.country import Country
from apps.landmatrix.models.deal import DealDataSource, DealHull, DealVersion
from apps.landmatrix.models.investor import InvestorHull, InvestorVersion

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


@pytest.fixture
def investors(db) -> list[InvestorHull]:
    N_INVESTORS = 2
    return InvestorHull.objects.bulk_create(
        [InvestorHull(first_created_at=timezone.now()) for _ in range(N_INVESTORS)]
    )


@pytest.fixture
def deal_with_active_version(db) -> DealHull:
    spain = Country.objects.get(id=724, name="Spain")
    deal = DealHull.objects.create(country=spain)
    deal.active_version = DealVersion.objects.create(deal_id=deal.id)
    deal.save()
    return deal


@pytest.fixture
def investor_with_active_version(db) -> InvestorHull:
    investor = InvestorHull.objects.create()
    investor.active_version = InvestorVersion.objects.create(
        name="MiracleCompany",
        investor_id=investor.id,
    )
    investor.save()
    return investor


@pytest.fixture
def public_deal(
    db,
    deal_with_active_version,
    investor_with_active_version,
) -> DealHull:
    deal_with_active_version.active_version.operating_company = (
        investor_with_active_version
    )
    DealDataSource.objects.create(
        nid="1234abcd",
        dealversion=deal_with_active_version.active_version,
    )
    # Trigger calculation of independent fields
    deal_with_active_version.active_version.save()
    return deal_with_active_version
