import json

from django.contrib.gis.geos import MultiPolygon, Point, Polygon
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from apps.landmatrix.models.country import Country
from apps.landmatrix.models.new import Area, DealHull, DealVersion, Location

from .gis_export import _build_area_features, _build_location_features
from .utils.geojson import is_feature_collection


def test_gis_export_locations() -> None:
    client = APIClient()

    response: Response = client.get("/api/gis_export/locations/")

    assert response.status_code == status.HTTP_200_OK
    assert response["Content-Disposition"] == "attachment; filename=locations.geojson"

    data = json.loads(response.content)
    assert is_feature_collection(data)


def test_gis_export_areas() -> None:
    client = APIClient()

    response: Response = client.get("/api/gis_export/areas/")

    assert response.status_code == status.HTTP_200_OK
    assert response["Content-Disposition"] == "attachment; filename=areas.geojson"

    data = json.loads(response.content)
    assert is_feature_collection(data)


def create_test_locations() -> None:
    BAHAMAS = Country.objects.get(name="Bahamas")

    d = DealHull.objects.create(country=BAHAMAS)
    dv = DealVersion.objects.create(deal=d, is_public=True)
    loc = Location.objects.create(
        dealversion=dv,
        point=Point(*POINT),
    )
    Area.objects.create(
        location=loc,
        type="production_area",
        area=MultiPolygon(Polygon(POLYGON_1), Polygon(POLYGON_2)),
    )
    Area.objects.create(
        location=loc,
        type="contract_area",
        area=MultiPolygon(Polygon(POLYGON_2), Polygon(POLYGON_1)),
    )


def test_build_location_features() -> None:
    create_test_locations()

    qs_deal_version = DealVersion.objects.all()
    features = _build_location_features(qs_deal_version)

    assert len(features) == 1

    assert all(f["type"] == "Feature" for f in features)
    assert all(f["geometry"]["type"] == "Point" for f in features)

    assert all(key in f["properties"] for f in features for key in PROP_KEYS)
    assert all(f["properties"]["type"] == "point" for f in features)

    assert features[0]["geometry"]["coordinates"] == POINT


def test_build_area_features() -> None:
    create_test_locations()

    qs_deal_version = DealVersion.objects.all()
    features = _build_area_features(qs_deal_version)

    assert len(features) == 2

    assert all(f["type"] == "Feature" for f in features)
    assert all(f["geometry"]["type"] == "MultiPolygon" for f in features)

    assert all(key in f["properties"] for f in features for key in PROP_KEYS)

    assert features[0]["properties"]["type"] == "production_area"
    assert features[0]["geometry"]["coordinates"] == [[POLYGON_1], [POLYGON_2]]

    assert features[1]["properties"]["type"] == "contract_area"
    assert features[1]["geometry"]["coordinates"] == [[POLYGON_2], [POLYGON_1]]


POINT = [20.5, -40.324]

POLYGON_1 = [[0, 0], [0, 1], [1, 1], [0, 0]]
POLYGON_2 = [[1, 1], [1, 2], [2, 2], [1, 1]]

PROP_KEYS = [
    "type",
    "deal_id",
    "country",
    "region",
    "id",
    "name",
    "level_of_accuracy",
    "facility_name",
    "description",
    "comment",
]
