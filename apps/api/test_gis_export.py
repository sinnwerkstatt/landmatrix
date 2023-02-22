from rest_framework import status
from rest_framework.test import APIClient

from apps.api.gis_export import (
    Feature,
    Geometry,
    create_deal_properties,
    create_export_features,
    create_feature_collection,
    get_location_properties,
    is_point,
    is_polygon,
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
    assert create_feature_collection([]) == {
        "type": "FeatureCollection",
        "features": [],
    }


def test_is_geometry_type():
    point_feature = Feature(
        type="Feature",
        properties={},
        geometry=Geometry(type="Point", coordinates=[]),
    )
    polygon_feature = Feature(
        type="Feature",
        properties={},
        geometry=Geometry(type="Polygon", coordinates=[]),
    )
    multi_polygon_feature = Feature(
        type="Feature",
        properties={},
        geometry=Geometry(type="MultiPolygon", coordinates=[]),
    )

    assert is_point(point_feature)
    assert not is_point(polygon_feature)
    assert not is_point(multi_polygon_feature)

    assert not is_polygon(point_feature)
    assert is_polygon(polygon_feature)
    assert is_polygon(multi_polygon_feature)


def test_create_deal_properties():
    deal = {
        "id": 50,
    }
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


def test_get_location_properties():
    feature = Feature(
        type="Feature",
        geometry=Geometry(type="Point", coordinates=[]),
        properties={},
    )
    assert get_location_properties(feature) == {
        "id": "",
        "type": "",
        "name": "",
        "spatial_accuracy": "",
    }, "Location properties default to empty string."

    feature = Feature(
        type="Feature",
        geometry=Geometry(type="Point", coordinates=[]),
        properties={
            "id": "ujOv1WP8",
            "name": "El Menia, Algeria",
            "type": "point",
            "spatial_accuracy": "APPROXIMATE_LOCATION",
            "other": "to_be_discarded",
        },
    )
    assert get_location_properties(feature) == {
        "id": "ujOv1WP8",
        "name": "El Menia, Algeria",
        "type": "point",
        "spatial_accuracy": "APPROXIMATE_LOCATION",
    }, "Discard non-location properties."


def test_create_export_data():
    point_feature1 = Feature(
        type="Feature",
        properties={},
        geometry=Geometry(type="Point", coordinates=[1.65963, 28.03389]),
    )
    point_feature2 = Feature(
        type="Feature",
        properties={},
        geometry=Geometry(type="Point", coordinates=[-0.179372, 27.8624853]),
    )
    polygon_feature = Feature(
        type="Feature",
        properties={},
        geometry=Geometry(
            type="Polygon",
            coordinates=[
                [
                    [-0.179372807503682, 27.86248531830949],
                    [-0.125126146033089, 27.86545380301335],
                    [-0.084284913295407, 27.887849642760354],
                    [-0.160808408511052, 27.89447061853726],
                    [-0.179372807503682, 27.86248531830949],
                ]
            ],
        ),
    )
    deals = [
        {"geojson": {"features": [point_feature1]}},
        {"geojson": {"features": [point_feature2, polygon_feature]}},
    ]

    export_data_point_features = create_export_features("points", deals)
    export_data_area_features = create_export_features("areas", deals)

    assert len(export_data_point_features) == 2
    assert len(export_data_area_features) == 1

    assert all(len(f["properties"]) == 7 for f in export_data_point_features)
    assert all(len(f["properties"]) == 7 for f in export_data_area_features)
