import pytest

from apps.greennewdeal.models import Deal


@pytest.mark.django_db
def test_get_deal_size():
    Deal.objects.create(
        id=3,
        intended_size=100.234,
        contract_size=[{"date": "2008", "value": "1000"}],
        production_size=[{"value": "10"}],
        negotiation_status=[{"date": "2008", "value": "Expression of interest"}],
    )
    d3 = Deal.objects.get(id=3)
    assert d3.get_deal_size() == 100
    d3.negotiation_status = [
        {"date": "2008", "value": "Expression of interest"},
        {"date": "2010", "value": "Oral agreement"},
    ]
    d3.save()
    assert d3.get_deal_size() == 1000
    d3.contract_size = None
    d3.save()
    assert d3.get_deal_size() == 10
    d3.negotiation_status = None
    d3.save()
    assert d3.get_deal_size() == 0
