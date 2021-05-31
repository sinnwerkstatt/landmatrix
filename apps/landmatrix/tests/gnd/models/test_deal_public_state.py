import pytest

from apps.landmatrix.models import (
    Deal,
    Investor,
    Country,
    InvestorVentureInvolvement,
)


@pytest.fixture
def public_deal(db) -> Deal:
    c1 = Country.objects.filter(high_income=False).first()
    i1 = Investor.objects.create(id=1, name="Test Investor", status=2)
    i2 = Investor.objects.create(id=2, name="Test Parent Investor", status=2)
    InvestorVentureInvolvement.objects.create(investor=i2, venture=i1, role="PARENT")

    deal = Deal.objects.create(
        id=3,
        confidential=False,
        country=c1,
        operating_company=i1,
        status=2,
        datasources=[{"name": "Test data source"}],
    )

    assert Deal.objects.filter(id=3).count() == 1
    assert Deal.objects.get(id=3).operating_company
    assert Deal.objects.get(id=3).operating_company.investors.exists()
    assert len(Deal.objects.get(id=3).datasources) > 0

    assert deal.is_public
    assert Deal.objects.public().count() == 1

    assert deal in i1.get_affected_deals()
    assert deal in i2.get_affected_deals()

    i3 = Investor.objects.create(id=3, name="Test Parent Parent Investor", status=2)
    InvestorVentureInvolvement.objects.create(investor=i3, venture=i2, role="PARENT")
    assert deal in i3.get_affected_deals()

    return deal


def test_public_deal_confidential_flag(public_deal: Deal):
    public_deal.confidential = True
    public_deal.save()
    assert not public_deal.is_public
    assert public_deal.not_public_reason == "CONFIDENTIAL"
    assert Deal.objects.public().count() == 0


def test_public_deal_country_problems(public_deal: Deal):
    public_deal.country = None
    public_deal.save()
    assert not public_deal.is_public
    assert public_deal.not_public_reason == "NO_COUNTRY"
    public_deal.country = Country.objects.filter(high_income=True).first()
    public_deal.save()
    assert not public_deal.is_public
    assert public_deal.not_public_reason == "HIGH_INCOME_COUNTRY"
    assert Deal.objects.public().count() == 0


def test_public_deal_no_datasources(public_deal: Deal):
    public_deal.datasources = []
    public_deal.save()
    assert not public_deal.is_public
    assert public_deal.not_public_reason == "NO_DATASOURCES"
    assert Deal.objects.public().count() == 0


def test_public_deal_no_operating_company(public_deal: Deal):
    public_deal.operating_company = None
    public_deal.save()
    assert not public_deal.is_public
    assert public_deal.not_public_reason == "NO_OPERATING_COMPANY"
    assert Deal.objects.public().count() == 0


# Case 0: Known investor and known parent company: fine.
# Case 1: Unknown investor, known Parent company: fine.
def test_public_deal_unknown_investors_1(public_deal: Deal):
    i1 = Investor.objects.get(id=1)
    i1.name = "Unnamed Investor"
    i1.save()
    public_deal.refresh_from_db()
    assert Deal.objects.public().count() == 1
    assert public_deal.is_public


# Case 2: Known investor, unknown Parent company: fine.
def test_public_deal_unknown_investors_2(public_deal: Deal):
    i2 = Investor.objects.get(id=2)
    i2.name = "Unknown Parent Investor"
    i2.save()
    assert i2.is_actually_unknown

    public_deal.refresh_from_db()
    assert Deal.objects.public().count() == 1
    assert public_deal.is_public


# Case 3: Unknown investor, unknown Parent company: error
def test_public_deal_unknown_investors_3(public_deal: Deal):
    oc = Investor.objects.get(id=1)
    oc.name = "Unnamed Investor"
    oc.save()
    assert oc.is_actually_unknown
    pi = Investor.objects.get(name="Test Parent Investor")
    pi.name = "Unknown Parent Investor"
    pi.save()
    assert pi.is_actually_unknown

    public_deal.refresh_from_db()
    assert not public_deal.is_public
    assert public_deal.not_public_reason == "NO_KNOWN_INVESTOR"
    assert Deal.objects.public().count() == 0


# Case 4: one unknown Parent company, one known Parent company: fine
def test_public_deal_unknown_investors_multiple(public_deal: Deal):
    oc = Investor.objects.get(name="Test Investor")
    oc.name = "Unnamed Investor"
    oc.save()
    assert oc.is_actually_unknown

    pi2 = Investor.objects.create(id=4, name="Unknown second test parent investor")
    InvestorVentureInvolvement.objects.create(investor=pi2, venture=oc, role="PARENT")
    assert Deal.objects.public().count() == 1
    assert Deal.objects.get(id=3).is_public
    pi3 = Investor.objects.create(id=5, name="Unknown third test parent investor")
    InvestorVentureInvolvement.objects.create(investor=pi3, venture=oc, role="PARENT")
    assert Deal.objects.public().count() == 1
    assert Deal.objects.get(id=3).is_public

    pi = Investor.objects.get(name="Test Parent Investor")
    pi.name = "Unknown Parent Investor"
    pi.save()
    assert pi.is_actually_unknown

    public_deal.refresh_from_db()
    assert not public_deal.is_public
    assert public_deal.not_public_reason == "NO_KNOWN_INVESTOR"
    assert Deal.objects.public().count() == 0


# Case 4x: one unknown Parent company, one known Parent company: fine
def test_public_deal_unknown_investors_delete_parent(public_deal: Deal):
    assert public_deal.is_public
    i1 = Investor.objects.get(id=1)
    i2 = Investor.objects.get(id=2)
    i3 = Investor.objects.get(id=3)
    i1.name = "Unknown investor"
    i1.save()
    assert public_deal.is_public
    for inv in InvestorVentureInvolvement.objects.filter(investor=i2):
        inv.delete()
    public_deal.refresh_from_db()
    assert not public_deal.is_public

    InvestorVentureInvolvement.objects.create(investor=i3, venture=i1, role="PARENT")
    public_deal.refresh_from_db()
    assert public_deal.is_public
