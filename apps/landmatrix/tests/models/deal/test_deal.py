import pytest
from django.db import IntegrityError

from apps.landmatrix.models.country import Country
from apps.landmatrix.models.deal import DealHull, DealVersion


# TODO: Make country mandatory
# def test_country_is_mandatory():
#     with pytest.raises(IntegrityError, match="country"):
#         DealHull.objects.create()


def test_get_deal_size():
    heaven = Country.objects.create(name="Heaven")
    deal = DealHull.objects.create(country=heaven)
    version = DealVersion.objects.create(
        deal_id=deal.id,
        intended_size=100.23,
        contract_size=[{"date": "2008", "area": 1000, "current": True}],
        production_size=[{"area": 10, "current": True}],
        negotiation_status=[
            {"date": "2008", "choice": "EXPRESSION_OF_INTEREST", "current": True}
        ],
    )

    assert float(version.deal_size) == 100.23

    version.negotiation_status = [
        {"date": "2008", "choice": "EXPRESSION_OF_INTEREST"},
        {"date": "2010", "choice": "ORAL_AGREEMENT", "current": True},
    ]
    version.save()
    assert version.deal_size == 1000

    version.contract_size = []
    version.save()
    assert version.deal_size == 10

    version.negotiation_status = []
    version.save()
    assert version.deal_size == 0
