from django.contrib.gis.geos import MultiPolygon, Polygon

from apps.landmatrix.models.choices import AreaTypeEnum, LocationAccuracyEnum
from apps.landmatrix.models.deal import Area, Location

from .queries import q_is_georeferenced, q_is_georeferenced_as, q_is_high_accuracy


def test_q_is_high_accuracy(deal_with_active_version):
    version = deal_with_active_version.active_version

    Location.objects.create(
        dealversion=version,
        level_of_accuracy=LocationAccuracyEnum.EXACT_LOCATION,
    )
    Location.objects.create(
        dealversion=version,
        level_of_accuracy=LocationAccuracyEnum.COORDINATES,
    )

    assert Location.objects.count() == 2
    assert Location.objects.filter(q_is_high_accuracy()).count() == 2, (
        f"Deals with level of accuracy {LocationAccuracyEnum.EXACT_LOCATION} or "
        f"{LocationAccuracyEnum.COORDINATES} are considered high accuracy."
    )

    Location.objects.create(
        dealversion=version,
        level_of_accuracy=LocationAccuracyEnum.COUNTRY,
    )
    Location.objects.create(
        dealversion=version,
        level_of_accuracy=LocationAccuracyEnum.ADMINISTRATIVE_REGION,
    )
    Location.objects.create(
        dealversion=version,
        level_of_accuracy=LocationAccuracyEnum.APPROXIMATE_LOCATION,
    )

    assert Location.objects.count() == 5
    assert Location.objects.filter(q_is_high_accuracy()).count() == 2, (
        f"Deals without level of accuracy {LocationAccuracyEnum.EXACT_LOCATION} or "
        f"{LocationAccuracyEnum.COORDINATES} are considered low accuracy."
    )


def test_q_is_georeferenced(deal_with_active_version):
    version = deal_with_active_version.active_version

    location = Location.objects.create(
        dealversion=version,
        level_of_accuracy=LocationAccuracyEnum.COUNTRY,
    )

    assert Location.objects.filter(q_is_georeferenced()).count() == 0, (
        "Location without areas does not meet quality goal."
    )

    Area.objects.create(
        location=location,
        area=MultiPolygon(Polygon(POLYGON_1)),
    )

    assert Location.objects.filter(q_is_georeferenced()).count() == 1, (
        "Locations with single area meets quality goal."
    )

    Area.objects.create(
        location=location,
        area=MultiPolygon(Polygon(POLYGON_2)),
    )
    Area.objects.create(
        location=location,
        area=MultiPolygon(Polygon(POLYGON_2), Polygon(POLYGON_1)),
    )

    assert Location.objects.filter(q_is_georeferenced()).count() == 1, (
        "Locations with three (any number of) area meets quality goal."
    )


def test_q_is_georeferenced_as(deal_with_active_version):
    version = deal_with_active_version.active_version

    location = Location.objects.create(
        dealversion=version,
        level_of_accuracy=LocationAccuracyEnum.COUNTRY,
    )

    assert not Location.objects.filter(
        q_is_georeferenced_as(AreaTypeEnum.intended_area)
    ).exists(), "Location has no intended areas."

    assert not Location.objects.filter(
        q_is_georeferenced_as(AreaTypeEnum.contract_area)
    ).exists(), "Location has no contract areas."

    assert not Location.objects.filter(
        q_is_georeferenced_as(AreaTypeEnum.production_area)
    ).exists(), "Location has no production areas."

    Area.objects.create(
        location=location,
        type=AreaTypeEnum.intended_area,
        area=MultiPolygon(Polygon(POLYGON_1)),
    )

    assert (
        Location.objects.filter(
            q_is_georeferenced_as(AreaTypeEnum.intended_area)
        ).count()
        == 1
    ), "Location has intended areas."

    Area.objects.create(
        location=location,
        type=AreaTypeEnum.contract_area,
        area=MultiPolygon(Polygon(POLYGON_1)),
    )

    assert (
        Location.objects.filter(
            q_is_georeferenced_as(AreaTypeEnum.contract_area)
        ).count()
        == 1
    ), "Location has contract areas."

    Area.objects.create(
        location=location,
        type=AreaTypeEnum.production_area,
        area=MultiPolygon(Polygon(POLYGON_1)),
    )

    assert (
        Location.objects.filter(
            q_is_georeferenced_as(AreaTypeEnum.production_area)
        ).count()
        == 1
    ), "Location has production areas."


POLYGON_1 = [[0, 0], [0, 1], [1, 1], [0, 0]]
POLYGON_2 = [[1, 1], [1, 2], [2, 2], [1, 1]]
