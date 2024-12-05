import pytest
from django.db.models import ProtectedError


@pytest.mark.django_db
def test_investor_updated(
    investors,
    public_deal,
):
    public_deal_version = public_deal.active_version
    public_investor_version = public_deal_version.operating_company.active_version

    assert public_deal_version.has_known_investor
    assert public_deal_version.is_public

    public_deal_version.operating_company.active_version = None
    public_deal_version.operating_company.save()

    public_deal_version.refresh_from_db()
    assert not public_deal_version.has_known_investor
    assert not public_deal_version.is_public

    public_deal_version.operating_company.active_version = public_investor_version
    public_deal_version.operating_company.save()

    public_deal_version.refresh_from_db()
    assert public_deal_version.has_known_investor
    assert public_deal_version.is_public

    with pytest.raises(ProtectedError):
        public_deal_version.operating_company.delete()

    public_deal_version.operating_company.deleted = True
    public_deal_version.operating_company.save()

    public_deal_version.refresh_from_db()
    assert not public_deal_version.has_known_investor
    assert not public_deal_version.is_public
