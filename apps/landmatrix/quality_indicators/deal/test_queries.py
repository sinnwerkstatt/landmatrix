from django.contrib.gis.geos import MultiPolygon, Polygon

from apps.landmatrix.models.choices import (
    AnimalsEnum,
    AreaTypeEnum,
    CarbonSequestrationEnum,
    CropsEnum,
    DatasourceTypeEnum,
    ElectricityGenerationEnum,
    ImplementationStatusEnum,
    IntentionOfInvestmentEnum,
    LocationAccuracyEnum,
    MineralsEnum,
    NatureOfDealEnum,
    NegotiationStatusEnum,
)
from apps.landmatrix.models.country import Country
from apps.landmatrix.models.deal import (
    Area,
    DealDataSource,
    DealHull,
    DealVersion,
    Location,
)
from apps.landmatrix.models.investor import InvestorHull, InvestorVersion

from .queries import (
    annotate_counts,
    produce_counts,
    q_all_basic_fields,
    q_all_datasource_valid,
    q_all_location_georeferenced,
    q_all_location_georeferenced_or_high_accuracy,
    q_all_status,
    q_all_status_dated,
    q_any_area_dated,
    q_any_location_georeferenced,
    q_any_location_georeferenced_as_contract,
    q_any_location_georeferenced_as_production,
    q_any_location_georeferenced_or_high_accuracy,
    q_any_produce_info,
    q_multiple_datasource,
    q_operating_company_in_target_country,
)


def test_q_any_location_high_accuracy_or_georeferenced(deal_with_active_version):
    version = deal_with_active_version.active_version

    qs_deal_versions = DealVersion.objects.all().annotate(counts=annotate_counts())

    assert (
        qs_deal_versions.filter(
            q_any_location_georeferenced_or_high_accuracy(),
        ).count()
        == 0
    )

    Location.objects.create(
        dealversion=version,
        level_of_accuracy=LocationAccuracyEnum.APPROXIMATE_LOCATION,
    )
    Location.objects.create(
        dealversion=version,
        level_of_accuracy=LocationAccuracyEnum.COUNTRY,
    )

    assert (
        qs_deal_versions.filter(
            q_any_location_georeferenced_or_high_accuracy(),
        ).count()
        == 0
    ), "No deal meets goal: Any location with high accuracy."

    assert (
        qs_deal_versions.filter(
            ~q_any_location_georeferenced_or_high_accuracy(),
        ).count()
        == 1
    ), "One deal meets inverse goal: Any location with high accuracy."

    Location.objects.create(
        dealversion=version,
        level_of_accuracy=LocationAccuracyEnum.EXACT_LOCATION,
    )

    assert (
        qs_deal_versions.filter(
            q_any_location_georeferenced_or_high_accuracy(),
        ).count()
        == 1
    ), "One deal meets goal: Any location with high accuracy."

    assert (
        qs_deal_versions.filter(
            ~q_any_location_georeferenced_or_high_accuracy(),
        ).count()
        == 0
    ), "No deal meets inverse goal: Any location with high accuracy."


def test_q_all_location_georeferenced_or_high_accuracy(deal_with_active_version):
    version = deal_with_active_version.active_version

    qs_deal_versions = DealVersion.objects.all().annotate(counts=annotate_counts())

    assert (
        qs_deal_versions.filter(
            q_all_location_georeferenced_or_high_accuracy(),
        ).count()
        == 0
    ), "Invalid: No locations."

    Location.objects.create(
        dealversion=version,
        level_of_accuracy=LocationAccuracyEnum.EXACT_LOCATION,
    )
    Location.objects.create(
        dealversion=version,
        level_of_accuracy=LocationAccuracyEnum.COORDINATES,
    )

    assert (
        qs_deal_versions.filter(
            q_all_location_georeferenced_or_high_accuracy(),
        ).count()
        == 1
    )
    assert (
        qs_deal_versions.filter(
            ~q_all_location_georeferenced_or_high_accuracy(),
        ).count()
        == 0
    )

    location = Location.objects.create(
        dealversion=version,
        level_of_accuracy=LocationAccuracyEnum.COUNTRY,
    )

    assert (
        qs_deal_versions.filter(
            q_all_location_georeferenced_or_high_accuracy(),
        ).count()
        == 0
    )

    assert (
        qs_deal_versions.filter(
            ~q_all_location_georeferenced_or_high_accuracy(),
        ).count()
        == 1
    )

    Area.objects.create(
        location=location,
        area=MultiPolygon(Polygon(POLYGON_1), Polygon(POLYGON_2)),
    )
    Area.objects.create(
        location=location,
        area=MultiPolygon(Polygon(POLYGON_2), Polygon(POLYGON_1)),
    )

    assert (
        qs_deal_versions.filter(
            q_all_location_georeferenced_or_high_accuracy(),
        ).count()
        == 1
    )
    assert (
        qs_deal_versions.filter(
            ~q_all_location_georeferenced_or_high_accuracy(),
        ).count()
        == 0
    )


def test_q_any_location_georeferenced(deal_with_active_version):
    version = deal_with_active_version.active_version

    qs_deal_versions = DealVersion.objects.all().annotate(counts=annotate_counts())

    assert not qs_deal_versions.filter(
        q_any_location_georeferenced()
    ).count(), "Deal has no locations."

    Location.objects.create(
        dealversion=version,
        level_of_accuracy=LocationAccuracyEnum.EXACT_LOCATION,
    )

    location = Location.objects.create(
        dealversion=version,
        level_of_accuracy=LocationAccuracyEnum.COUNTRY,
    )

    assert not qs_deal_versions.filter(
        q_any_location_georeferenced()
    ).count(), "Deal has no location with areas."

    Area.objects.create(
        location=location,
        area=MultiPolygon(Polygon(POLYGON_1), Polygon(POLYGON_2)),
    )
    Area.objects.create(
        location=location,
        area=MultiPolygon(Polygon(POLYGON_2), Polygon(POLYGON_1)),
    )

    assert qs_deal_versions.filter(
        q_any_location_georeferenced()
    ).count(), "Deal has location with areas."


def test_q_all_location_georeferenced(deal_with_active_version):
    version = deal_with_active_version.active_version

    qs_deal_versions = DealVersion.objects.all().annotate(counts=annotate_counts())

    assert (
        qs_deal_versions.filter(q_all_location_georeferenced()).count() == 0
    ), "No deal has no locations."

    location_1 = Location.objects.create(
        dealversion=version,
        level_of_accuracy=LocationAccuracyEnum.EXACT_LOCATION,
    )

    location_2 = Location.objects.create(
        dealversion=version,
        level_of_accuracy=LocationAccuracyEnum.COUNTRY,
    )

    assert not qs_deal_versions.filter(
        q_all_location_georeferenced()
    ).count(), "No locations has areas."

    Area.objects.create(
        location=location_1,
        area=MultiPolygon(Polygon(POLYGON_1), Polygon(POLYGON_2)),
    )

    assert not qs_deal_versions.filter(
        q_all_location_georeferenced()
    ).count(), "Not all locations have areas."

    Area.objects.create(
        location=location_2,
        area=MultiPolygon(Polygon(POLYGON_2), Polygon(POLYGON_1)),
    )

    assert qs_deal_versions.filter(
        q_all_location_georeferenced()
    ).count(), "All locations have areas."


def test_q_any_location_georeferenced_as(deal_with_active_version):
    version = deal_with_active_version.active_version

    qs_deal_versions = DealVersion.objects.all().annotate(counts=annotate_counts())

    assert (
        qs_deal_versions.filter(q_any_location_georeferenced_as_production()).count()
        == 0
    ), "No deals with production areas."

    assert (
        qs_deal_versions.filter(q_any_location_georeferenced_as_contract()).count() == 0
    ), "No deals with contract areas."

    location_1 = Location.objects.create(
        dealversion=version,
        level_of_accuracy=LocationAccuracyEnum.EXACT_LOCATION,
    )

    location_2 = Location.objects.create(
        dealversion=version,
        level_of_accuracy=LocationAccuracyEnum.COUNTRY,
    )

    Area.objects.create(
        location=location_1,
        type=AreaTypeEnum.production_area,
        area=MultiPolygon(Polygon(POLYGON_1), Polygon(POLYGON_2)),
    )

    assert (
        qs_deal_versions.filter(q_any_location_georeferenced_as_production()).count()
        == 1
    ), "One deal with single production area."

    assert (
        qs_deal_versions.filter(q_any_location_georeferenced_as_contract()).count() == 0
    ), "No deals with single contract area."

    Area.objects.create(
        location=location_2,
        type=AreaTypeEnum.production_area,
        area=MultiPolygon(Polygon(POLYGON_2), Polygon(POLYGON_1)),
    )

    assert (
        qs_deal_versions.filter(q_any_location_georeferenced_as_production()).count()
        == 1
    ), "One deal with multiple production areas."

    assert (
        qs_deal_versions.filter(q_any_location_georeferenced_as_contract()).count() == 0
    ), "No deals with single contract area."

    Area.objects.create(
        location=location_1,
        type=AreaTypeEnum.contract_area,
        area=MultiPolygon(Polygon(POLYGON_2), Polygon(POLYGON_1)),
    )

    assert (
        qs_deal_versions.filter(q_any_location_georeferenced_as_production()).count()
        == 1
    ), "One deal with multiple production areas."

    assert (
        qs_deal_versions.filter(q_any_location_georeferenced_as_contract()).count() == 1
    ), "No deals with single contract area."


def test_q_multiple_datasource(deal_with_active_version):
    version = deal_with_active_version.active_version

    qs_deal_versions = DealVersion.objects.all().annotate(counts=annotate_counts())

    assert qs_deal_versions.filter(q_multiple_datasource()).count() == 0

    DealDataSource.objects.create(dealversion=version)

    assert qs_deal_versions.filter(q_multiple_datasource()).count() == 0

    DealDataSource.objects.create(dealversion=version)

    assert qs_deal_versions.filter(q_multiple_datasource()).count() == 1


def test_q_all_datasource_valid(deal_with_active_version):
    version = deal_with_active_version.active_version

    qs_deal_versions = DealVersion.objects.all().annotate(counts=annotate_counts())

    assert not (
        qs_deal_versions.filter(q_all_datasource_valid()).exists()
    ), "Deal does not have data sources."

    DealDataSource.objects.create(
        dealversion=version,
        type=DatasourceTypeEnum.OTHER,
    )

    assert not (
        qs_deal_versions.filter(q_all_datasource_valid()).exists()
    ), "Deal does not have data sources that require file."

    DealDataSource.objects.create(
        dealversion=version,
        type=DatasourceTypeEnum.COMPANY_SOURCES,
        file="document.pdf",
    )

    assert (
        qs_deal_versions.filter(q_all_datasource_valid()).count() == 1
    ), "Deal has one data source that does require file and has it."

    DealDataSource.objects.create(
        dealversion=version,
        type=DatasourceTypeEnum.GOVERNMENT_SOURCES,
    )

    assert not (
        qs_deal_versions.filter(q_all_datasource_valid()).exists()
    ), "Deal has one data source that does require file but does not have it."


def test_q_all_status(deal_with_active_version):
    version = deal_with_active_version.active_version

    qs_deal_versions = DealVersion.objects.all().annotate(counts=annotate_counts())

    assert (
        qs_deal_versions.filter(q_all_status()).count() == 0
    ), "Deal does not have negotiation status and implementation status."

    version.negotiation_status = []
    version.implementation_status = []
    version.save()

    assert (
        qs_deal_versions.filter(q_all_status()).count() == 0
    ), "Deal still does not have negotiation status and implementation status."

    version.negotiation_status = [
        {
            "choice": NegotiationStatusEnum.EXPRESSION_OF_INTEREST,
            "date": "2020",
            "current": True,
        }
    ]
    version.save()

    assert (
        qs_deal_versions.filter(q_all_status()).count() == 0
    ), "Deal still does have negotiation status but no implementation status."

    version.implementation_status = [
        {
            "choice": ImplementationStatusEnum.PROJECT_NOT_STARTED,
            "date": "2020",
            "current": False,
        },
        {
            "choice": ImplementationStatusEnum.IN_OPERATION,
            "date": "2022",
            "current": True,
        },
    ]
    version.save()

    assert (
        qs_deal_versions.filter(q_all_status()).count() == 1
    ), "Deal still has negotiation status and implementation status."


def test_q_all_status_dated(deal_with_active_version):
    version = deal_with_active_version.active_version

    qs_deal_versions = DealVersion.objects.all().annotate(counts=annotate_counts())

    assert (
        qs_deal_versions.filter(q_all_status_dated()).count() == 0
    ), "Deal does not have negotiation status and implementation status."

    version.negotiation_status = []
    version.implementation_status = []
    version.save()

    assert (
        qs_deal_versions.filter(q_all_status_dated()).count() == 0
    ), "Deal still does not have negotiation status and implementation status."

    version.negotiation_status = [
        {
            "choice": NegotiationStatusEnum.EXPRESSION_OF_INTEREST,
            "current": True,
        }
    ]
    version.implementation_status = [
        {
            "choice": ImplementationStatusEnum.PROJECT_NOT_STARTED,
        },
        {
            "choice": ImplementationStatusEnum.IN_OPERATION,
            "date": "2022",
            "current": True,
        },
    ]
    version.save()

    assert (
        qs_deal_versions.filter(q_all_status_dated()).count() == 0
    ), "Deal is missing date for negotiation status."

    version.negotiation_status = [
        {
            "choice": NegotiationStatusEnum.EXPRESSION_OF_INTEREST,
        },
        {
            "choice": NegotiationStatusEnum.CONTRACT_SIGNED,
            "date": "2021",
            "current": True,
        },
    ]
    version.save()

    assert (
        qs_deal_versions.filter(q_all_status_dated()).count() == 1
    ), "Deal is has date for negotiation status and implementation status."


def test_q_any_area_dated(deal_with_active_version):
    version = deal_with_active_version.active_version

    qs_deal_versions = DealVersion.objects.all().annotate(counts=annotate_counts())

    assert qs_deal_versions.filter(q_any_area_dated()).count() == 0, "No sizes."

    version.contract_size = [{"area": 123.45, "current": True}]
    version.production_size = []
    version.save()

    assert (
        qs_deal_versions.filter(q_any_area_dated()).count() == 0
    ), "Contract size not dated."

    version.contract_size = [{"area": 123.45, "current": True}]
    version.production_size = [
        {"area": 0.0},
        {"area": 123.45, "date": "2000", "current": True},
    ]
    version.save()

    assert (
        qs_deal_versions.filter(q_any_area_dated()).count() == 1
    ), "Production size dated."


def test_q_any_produce_info(deal_with_active_version):
    version = deal_with_active_version.active_version

    qs_deal_versions = DealVersion.objects.all().annotate(counts=annotate_counts())

    assert qs_deal_versions.filter(q_any_produce_info()).count() == 0

    version.crops = [
        {
            "choices": [CropsEnum.TEK, CropsEnum.VIN],
            "current": True,
        }
    ]
    version.save()

    assert qs_deal_versions.filter(q_any_produce_info()).count() == 1


def test_q_all_basic_fields(deal_with_active_version):
    version = deal_with_active_version.active_version

    qs_deal_versions = DealVersion.objects.all().annotate(counts=annotate_counts())

    assert qs_deal_versions.filter(q_all_basic_fields()).count() == 0

    version.contract_size = [{"area": 123.45, "current": True}]
    version.save()

    assert qs_deal_versions.filter(q_all_basic_fields()).count() == 0

    version.intention_of_investment = [
        {
            "area": 123.45,
            "choices": [IntentionOfInvestmentEnum.FORESTRY_UNSPECIFIED],
            "current": True,
        }
    ]
    version.save()

    assert qs_deal_versions.filter(q_all_basic_fields()).count() == 0

    version.negotiation_status = [
        {
            "choice": NegotiationStatusEnum.EXPRESSION_OF_INTEREST,
            "current": True,
        }
    ]
    version.save()

    assert qs_deal_versions.filter(q_all_basic_fields()).count() == 0

    version.implementation_status = [
        {
            "choice": ImplementationStatusEnum.IN_OPERATION,
            "current": True,
        },
    ]
    version.save()

    assert qs_deal_versions.filter(q_all_basic_fields()).count() == 0

    version.nature_of_deal = [
        NatureOfDealEnum.OUTRIGHT_PURCHASE,
        NatureOfDealEnum.LEASE,
    ]
    version.save()

    assert qs_deal_versions.filter(q_all_basic_fields()).count() == 0

    # any produce info
    version.animals = [
        {
            "choices": [AnimalsEnum.AQU, AnimalsEnum.BEE],
            "current": True,
        }
    ]
    version.save()

    assert qs_deal_versions.filter(q_all_basic_fields()).count() == 1


def test_q_operating_company_in_target_country():
    spain = Country.objects.get(id=724, name="Spain")
    portugal = Country.objects.get(id=620, name="Portugal")

    deal = DealHull.objects.create(country=spain)
    investor = InvestorHull.objects.create()

    deal_version = DealVersion.objects.create(deal_id=deal.id)
    deal.active_version = deal_version
    deal.save()

    qs_deal_versions = DealVersion.objects.all()
    assert (
        qs_deal_versions.filter(q_operating_company_in_target_country()).count() == 0
    ), "No operating company."

    investor.active_version = InvestorVersion.objects.create(
        investor_id=investor.id,
        country=portugal,
    )
    investor.save()

    deal_version.operating_company = investor
    deal_version.save()

    assert (
        qs_deal_versions.filter(q_operating_company_in_target_country()).count() == 0
    ), "Operating company from another country."

    investor.active_version = InvestorVersion.objects.create(
        investor_id=investor.id,
        country=spain,
    )
    investor.save()

    deal_version.operating_company = investor
    deal_version.save()
    assert (
        qs_deal_versions.filter(q_operating_company_in_target_country()).count() == 1
    ), "Operating company from same country."


# Annotations: Counts and quality indicators
def test_annotate_counts(deal_with_active_version):
    counts = (
        DealVersion.objects.all()
        .annotate(counts=annotate_counts())
        .values_list("counts", flat=True)
        .first()
    )
    assert all(
        name in counts
        for name in [
            "intention_of_investment",
            "negotiation_status",
            "implementation_status",
            "production_size",
            "contract_size",
            "nature_of_deal",
            "produce",
        ]
    )


def test_produce_counts(deal_with_active_version):
    version = deal_with_active_version.active_version

    version.crops = [{"choices": [CropsEnum.TEK]}, {"choices": [CropsEnum.BOT]}]
    version.animals = [{"choices": []}]
    version.mineral_resources = [{"choices": [MineralsEnum.BAR]}]
    version.contract_farming_crops = [{"choices": [CropsEnum.TEK, CropsEnum.BOT]}]
    version.contract_farming_animals = []
    version.electricity_generation = [
        {"choices": [ElectricityGenerationEnum.WIND]},
        {"choices": [ElectricityGenerationEnum.SOLAR_HEAT]},
        {"choices": [ElectricityGenerationEnum.PHOTOVOLTAIC]},
    ]
    version.carbon_sequestration = [{"choices": [CarbonSequestrationEnum.OTHER]}]
    version.save()

    assert list(
        DealVersion.objects.all()
        .annotate(counts=produce_counts())
        .values_list("counts", flat=True)
    ) == [
        {
            "crops": 2,
            "animals": 1,
            "mineral_resources": 1,
            "contract_farming_crops": 1,
            "contract_farming_animals": 0,
            "electricity_generation": 3,
            "carbon_sequestration": 1,
        }
    ]


POLYGON_1 = [[0, 0], [0, 1], [1, 1], [0, 0]]
POLYGON_2 = [[1, 1], [1, 2], [2, 2], [1, 1]]
