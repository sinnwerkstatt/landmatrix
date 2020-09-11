import pytest

from apps.landmatrix.models import (
    Deal,
    Investor,
    Country,
    DataSource,
    InvestorVentureInvolvement,
)


@pytest.fixture
def public_deal(db) -> Deal:
    c1 = Country.objects.filter(high_income=False).first()
    i1 = Investor.objects.create(id=1, name="Test Investor")
    i2 = Investor.objects.create(id=2, name="Test Parent Investor")
    InvestorVentureInvolvement.objects.create(
        investor=i2, venture=i1, role="STAKEHOLDER"
    )

    deal = Deal.objects.create(
        id=3, confidential=False, country=c1, operating_company=i1, status=2,
    )
    DataSource.objects.create(deal=deal, name="Test data source")

    assert Deal.objects.filter(id=3).count() == 1
    assert Deal.objects.get(id=3).operating_company
    assert Deal.objects.get(id=3).operating_company.investors.exists()
    assert Deal.objects.get(id=3).datasources.exists()

    assert deal.is_public_deal()
    assert Deal.objects.public().count() == 1

    return deal


def test_public_deal_confidential_flag(public_deal: Deal):
    public_deal.confidential = True
    public_deal.save()
    with pytest.raises(public_deal.IsNotPublic, match="Confidential Flag"):
        public_deal.is_public_deal()
    assert Deal.objects.public().count() == 0


def test_public_deal_country_problems(public_deal: Deal):
    public_deal.country = None
    public_deal.save()
    with pytest.raises(
        public_deal.IsNotPublic, match="No Country or High-Income Country"
    ):
        public_deal.is_public_deal()
    public_deal.country = Country.objects.filter(high_income=True).first()
    public_deal.save()
    with pytest.raises(
        public_deal.IsNotPublic, match="No Country or High-Income Country"
    ):
        public_deal.is_public_deal()
    assert Deal.objects.public().count() == 0


def test_public_deal_no_datasources(public_deal: Deal):
    public_deal.datasources.all().delete()
    with pytest.raises(public_deal.IsNotPublic, match="No Datasources"):
        public_deal.is_public_deal()
    assert Deal.objects.public().count() == 0


def test_public_deal_no_operating_company(public_deal: Deal):
    public_deal.operating_company = None
    public_deal.save()
    with pytest.raises(public_deal.IsNotPublic, match="No Operating Company"):
        public_deal.is_public_deal()
    assert Deal.objects.public().count() == 0


# Case 0: Known investor and known parent company: fine.
# Case 1: Unknown investor, known Parent company: fine.
def test_public_deal_unknown_investors_1(public_deal: Deal):
    oc = Investor.objects.get(name="Test Investor")
    oc.name = "Unnamed Investor"
    oc.save()
    assert Deal.objects.public().count() == 1
    assert Deal.objects.get(id=3).is_public_deal()


# Case 2: Known investor, unknown Parent company: fine.
def test_public_deal_unknown_investors_2(public_deal: Deal):
    pi = Investor.objects.get(name="Test Parent Investor")
    pi.name = "Unknown Parent Investor"
    pi.save()
    assert pi.is_actually_unknown
    assert Deal.objects.public().count() == 1
    assert Deal.objects.get(id=3).is_public_deal()


# Case 3: Unknown investor, unknown Parent company: error
def test_public_deal_unknown_investors_3(public_deal: Deal):
    oc = Investor.objects.get(name="Test Investor")
    oc.name = "Unnamed Investor"
    oc.save()
    assert oc.is_actually_unknown
    pi = Investor.objects.get(name="Test Parent Investor")
    pi.name = "Unknown Parent Investor"
    pi.save()
    assert pi.is_actually_unknown

    with pytest.raises(Deal.IsNotPublic, match="No known investor"):
        Deal.objects.get(id=3).is_public_deal()
    assert Deal.objects.public().count() == 0


# Case 4: one unknown Parent company, one known Parent company: fine
def test_public_deal_unknown_investors_multiple(public_deal: Deal):
    oc = Investor.objects.get(name="Test Investor")
    oc.name = "Unnamed Investor"
    oc.save()
    assert oc.is_actually_unknown

    pi2 = Investor.objects.create(id=3, name="Unknown second test parent investor")
    InvestorVentureInvolvement.objects.create(
        investor=pi2, venture=oc, role="STAKEHOLDER"
    )
    assert Deal.objects.public().count() == 1
    assert Deal.objects.get(id=3).is_public_deal()
    pi3 = Investor.objects.create(id=4, name="Unknown third test parent investor")
    InvestorVentureInvolvement.objects.create(
        investor=pi3, venture=oc, role="STAKEHOLDER"
    )
    assert Deal.objects.public().count() == 1
    assert Deal.objects.get(id=3).is_public_deal()

    pi = Investor.objects.get(name="Test Parent Investor")
    pi.name = "Unknown Parent Investor"
    pi.save()
    assert pi.is_actually_unknown

    with pytest.raises(Deal.IsNotPublic, match="No known investor"):
        Deal.objects.get(id=3).is_public_deal()
    assert Deal.objects.public().count() == 0
