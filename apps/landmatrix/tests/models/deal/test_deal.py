from apps.landmatrix.models.country import Country
from apps.landmatrix.models.deal import DealHull, DealVersion

# TODO: Make country mandatory
# def test_country_is_mandatory():
#     with pytest.raises(IntegrityError, match="country"):
#         DealHull.objects.create()


def test_get_deal_size():
    spain = Country.objects.get(id=724, name="Spain")
    deal = DealHull.objects.create(country=spain)
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


def test_calculate_initiation_year():
    spain = Country.objects.get(id=724, name="Spain")
    deal = DealHull.objects.create(country=spain)
    version = DealVersion.objects.create(
        deal_id=deal.id,
    )

    assert version.initiation_year is None, (
        "No negotiation or implementation status items."
    )

    version = DealVersion.objects.create(
        deal_id=deal.id,
        negotiation_status=[
            {"choice": "EXPRESSION_OF_INTEREST", "date": "2014", "current": True},
        ],
    )

    assert version.initiation_year is None, "Invalid choice EXPRESSION_OF_INTEREST."

    version = DealVersion.objects.create(
        deal_id=deal.id,
        negotiation_status=[
            {"choice": "EXPRESSION_OF_INTEREST", "date": "2014", "current": True},
            {"choice": "UNDER_NEGOTIATION"},
            {"choice": "ORAL_AGREEMENT", "date": None},
        ],
    )

    assert version.initiation_year is None, (
        "Valid choices UNDER_NEGOTIATION / ORAL_AGREEMENT, but no dates."
    )

    version = DealVersion.objects.create(
        deal_id=deal.id,
        negotiation_status=[
            {"choice": "EXPRESSION_OF_INTEREST", "date": "2014", "current": True},
            {"choice": "UNDER_NEGOTIATION"},
            {"choice": "ORAL_AGREEMENT", "date": None},
            {"choice": "CONTRACT_SIGNED", "date": "2018-12-01"},
        ],
    )

    assert version.initiation_year == 2018, (
        "Initiation year is 2018 - date of CONTRACT_SIGNED choice."
    )

    version = DealVersion.objects.create(
        deal_id=deal.id,
        negotiation_status=[
            {"choice": "EXPRESSION_OF_INTEREST", "date": "2014", "current": True},
            {"choice": "UNDER_NEGOTIATION"},
            {"choice": "ORAL_AGREEMENT", "date": None},
            {"choice": "CONTRACT_SIGNED", "date": "2018-12-01"},
            {"choice": "NEGOTIATIONS_FAILED", "date": "2020"},
            {"choice": "CONTRACT_FAILED", "date": "2024"},
        ],
    )

    assert version.initiation_year == 2018, (
        "Initiation year is 2018 - earliest date of all dated items with valid choice."
    )

    version = DealVersion.objects.create(
        deal_id=deal.id,
        negotiation_status=[
            {"choice": "EXPRESSION_OF_INTEREST", "date": "2014", "current": True},
            {"choice": "UNDER_NEGOTIATION"},
            {"choice": "ORAL_AGREEMENT", "date": None},
            {"choice": "CONTRACT_SIGNED", "date": "2018-12-01"},
            {"choice": "NEGOTIATIONS_FAILED", "date": "2020"},
            {"choice": "CONTRACT_FAILED", "date": "2024"},
        ],
        implementation_status=[
            {"choice": "PROJECT_NOT_STARTED", "date": "2014"},
            {"choice": "STARTUP_PHASE", "date": "2016", "current": True},
        ],
    )

    assert version.initiation_year == 2016, (
        "Initiation year is 2016 - earliest date of all dated items "
        "with valid negotiation or implementation choice."
    )
