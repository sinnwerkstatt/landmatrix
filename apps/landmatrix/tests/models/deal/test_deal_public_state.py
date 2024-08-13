import pytest

from apps.landmatrix.models.abstract import VersionStatus
from apps.landmatrix.models.choices import InvolvementRoleEnum
from apps.landmatrix.models.country import Country
from apps.landmatrix.models.deal import DealHull, DealVersion, DealDataSource
from apps.landmatrix.models.investor import InvestorHull, Involvement, InvestorVersion


@pytest.fixture
def public_deal_with_investors() -> (
    tuple[DealHull, InvestorHull, InvestorHull, InvestorHull]
):
    c1 = Country.objects.filter(high_income=False).first()

    i1 = InvestorHull.objects.create()
    i1.active_version = InvestorVersion.objects.create(
        investor=i1,
        name="Test Investor",
        status=VersionStatus.ACTIVATED,
    )
    i1.save()

    i2 = InvestorHull.objects.create()
    i2.active_version = InvestorVersion.objects.create(
        investor=i2,
        name="Test First Parent Investor",
        status=VersionStatus.ACTIVATED,
    )
    i2.save()

    Involvement.objects.create(
        parent_investor=i2,
        child_investor=i1,
        role=InvolvementRoleEnum.PARENT,
    )

    i3 = InvestorHull.objects.create()
    i3.active_version = InvestorVersion.objects.create(
        investor=i3,
        name="Test Second Parent Investor",
        status=VersionStatus.ACTIVATED,
    )
    i3.save()

    Involvement.objects.create(
        parent_investor=i3,
        child_investor=i1,
        role=InvolvementRoleEnum.PARENT,
    )

    i4 = InvestorHull.objects.create()
    i4.active_version = InvestorVersion.objects.create(
        investor=i4,
        name="Test Parent Parent Investor",
        status=VersionStatus.ACTIVATED,
    )
    i4.save()

    Involvement.objects.create(
        parent_investor=i4,
        child_investor=i3,
        role=InvolvementRoleEnum.PARENT,
    )

    d1 = DealHull.objects.create(
        confidential=False,
        country=c1,
    )

    d1.active_version = DealVersion.objects.create(
        deal=d1,
        # Cannot be in here because of save(dependent=True) sets parent_companies
        # operating_company=i1,
        status=VersionStatus.ACTIVATED,
    )
    d1.active_version.operating_company = i1
    d1.active_version.datasources.add(
        DealDataSource(name="Test datasource"),
        bulk=False,
    )
    d1.active_version.save()
    d1.save()

    return d1, i1, i2, i3


def test_public_deal(public_deal_with_investors):
    d1, i1, i2, i3 = public_deal_with_investors

    assert d1.active_version.operating_company
    assert d1.active_version.parent_companies.exists()
    assert d1.active_version.datasources.exists()

    assert d1.active_version.is_public
    assert DealHull.objects.public().count() == 1

    assert d1.active_version in i1.get_affected_dealversions()
    assert d1.active_version in i2.get_affected_dealversions()
    assert d1.active_version in i3.get_affected_dealversions()


# def test_public_deal_confidential_flag(public_deal_with_investors):
#     d1, i1, i2, i3 = public_deal_with_investors
#
#     d1.confidential = True
#     d1.save()
#
#     assert not d1.active_version.is_public
#     assert d1.not_public_reason == "NO_DATASOURCES"


# def test_public_deal_country_problems(public_deal_with_investors):
#     d1, i1, i2, i3 = public_deal_with_investors
#
#     d1.country = None
#     d1.save()
#
#     assert not d1.active_version.is_public
#     assert d1.not_public_reason == "NO_COUNTRY"
#
#     d1.country = Country.objects.filter(high_income=True).first()
#     d1.save()
#
#     assert not d1.active_version.is_public
#     assert d1.not_public_reason == "HIGH_INCOME_COUNTRY"


def test_public_deal_no_datasources(public_deal_with_investors):
    d1, i1, i2, i3 = public_deal_with_investors

    for ds in d1.active_version.datasources.all():
        ds.delete()

    d1.active_version.save()

    assert not d1.active_version.is_public
    # assert d1.not_public_reason == "NO_DATASOURCES"


def test_public_deal_no_operating_company(public_deal_with_investors):
    d1, i1, i2, i3 = public_deal_with_investors

    d1.active_version.operating_company = None
    d1.active_version.save()

    assert not d1.active_version.is_public
    # assert d1.active_version.not_public_reason == "NO_OPERATING_COMPANY"


def test_public_deal_unknown_investors_3(public_deal_with_investors):
    d1, i1, i2, i3 = public_deal_with_investors

    i1.active_version.name = "Unnamed Investor"
    i1.active_version.save()

    assert i1.active_version.name_unknown

    d1.active_version.save()
    assert d1.active_version.is_public, "Unknown investor, known parents: fine"

    i2.active_version.name = "Unknown First Parent Investor"
    i2.active_version.save()

    assert i2.active_version.name_unknown

    d1.active_version.save()
    assert d1.active_version.is_public, "Unknown investor, one known parent: fine"

    i3.active_version.name = "Unknown Second Parent Investor"
    i3.active_version.save()

    assert i3.active_version.name_unknown

    d1.active_version.save()
    assert (
        not d1.active_version.is_public
    ), "Unknown investor, no known direct parents: error"
    # assert d1.not_public_reason == "NO_KNOWN_INVESTOR"
