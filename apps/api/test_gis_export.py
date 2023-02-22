from rest_framework.test import APIClient
from rest_framework import status

from apps.api.gis_export import (
    create_feature_collection,
    Feature,
    is_point,
    is_polygon,
    create_deal_properties,
)


def test_gis_export_type():
    client = APIClient()
    response = client.get("/api/gis_export/")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.content.startswith(b"Missing query parameter 'type'.")

    response = client.get("/api/gis_export/?type=other")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.content.startswith(b"Invalid 'type' value: 'other'.")

    response = client.get("/api/gis_export/?type=points")
    assert response.status_code == status.HTTP_200_OK
    assert response["Content-Disposition"] == 'attachment; filename="points.geojson"'

    response = client.get("/api/gis_export/?type=areas")
    assert response.status_code == status.HTTP_200_OK
    assert response["Content-Disposition"] == 'attachment; filename="areas.geojson"'


def test_create_feature_collection():
    features = [
        Feature(geometry={"type": "Point"}),
        Feature(geometry={"type": "Polygon"}),
    ]

    assert create_feature_collection(features) == {
        "type": "FeatureCollection",
        "features": features,
    }


def test_is_geometry_type():
    point_feature = Feature(geometry={"type": "Point"})
    polygon_feature = Feature(geometry={"type": "Polygon"})
    multi_polygon_feature = Feature(geometry={"type": "MultiPolygon"})

    assert is_point(point_feature)
    assert not is_point(polygon_feature)
    assert not is_point(multi_polygon_feature)

    assert not is_polygon(point_feature)
    assert is_polygon(polygon_feature)
    assert is_polygon(multi_polygon_feature)


def test_create_deal_properties():
    deal = {"id": 50}
    assert create_deal_properties(deal) == {
        "deal_id": "50",
        "country": "",
        "region": "",
    }

    deal = {
        "id": 50,
        "country": None,
    }
    assert create_deal_properties(deal) == {
        "deal_id": "50",
        "country": "",
        "region": "",
    }

    deal = {
        "id": 50,
        "country": {"name": "MysteryLand"},
    }
    assert create_deal_properties(deal) == {
        "deal_id": "50",
        "country": "MysteryLand",
        "region": "",
    }

    deal = {
        "id": 50,
        "country": {
            "name": "MysteryLand",
            "region": None,
        },
    }
    assert create_deal_properties(deal) == {
        "deal_id": "50",
        "country": "MysteryLand",
        "region": "",
    }

    deal = {
        "id": 50,
        "country": {
            "name": "MysteryLand",
            "region": {"name": "Heaven"},
        },
    }
    assert create_deal_properties(deal) == {
        "deal_id": "50",
        "country": "MysteryLand",
        "region": "Heaven",
    }
