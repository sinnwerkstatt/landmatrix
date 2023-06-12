import pytest

from rest_framework import status
from rest_framework.test import APIClient

from apps.api.gis_export import (
    DealValues,
    Location,
    create_area_features,
    create_deal_properties,
    create_export_features,
    create_location_properties,
    create_point_feature,
)
from apps.api.utils.geojson import Geometry, create_feature, create_feature_collection


def test_gis_export_type() -> None:
    client = APIClient()
    response = client.get("/api/gis_export/")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.content.startswith(b"Missing query parameter 'type'.")

    response = client.get("/api/gis_export/?type=other")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.content.startswith(b"Invalid 'type' value: 'other'.")

    response = client.get("/api/gis_export/?type=locations")
    assert response.status_code == status.HTTP_200_OK
    assert response["Content-Disposition"] == "attachment; filename=locations.geojson"

    response = client.get("/api/gis_export/?type=areas")
    assert response.status_code == status.HTTP_200_OK
    assert response["Content-Disposition"] == "attachment; filename=areas.geojson"


def test_create_point_feature() -> None:
    location_without_point: Location = {"id": "pEYNmo1F"}

    with pytest.raises(KeyError, match=r"point"):
        create_point_feature(location_without_point)

    location_with_point: Location = {
        "id": "pEYNmo1F",
        "point": {"lat": -20.1129, "lng": 32.71813},
    }

    assert create_point_feature(location_with_point)["geometry"] == {
        "type": "Point",
        "coordinates": [32.71813, -20.1129],
    }, "Sets point geometry with coordinates."

    assert (
        create_point_feature(location_with_point)["properties"]["type"] == "point"
    ), "Type property set to poitn."


def test_create_deal_properties() -> None:
    deal_without_country: DealValues = {
        "id": 50,
        "locations": [],
        "country": None,
    }
    assert create_deal_properties(deal_without_country) == {
        "deal_id": 50,
        "country": "",
        "region": "",
    }

    deal_with_country: DealValues = {
        "id": 50,
        "locations": [],
        "country": {"name": "Albania", "region": None},
    }
    assert create_deal_properties(deal_with_country) == {
        "deal_id": 50,
        "country": "Albania",
        "region": "",
    }

    deal_with_country_and_region: DealValues = {
        "id": 50,
        "locations": [],
        "country": {
            "name": "Albania",
            "region": {"name": "Balkan"},
        },
    }
    assert create_deal_properties(deal_with_country_and_region) == {
        "deal_id": 50,
        "country": "Albania",
        "region": "Balkan",
    }


def test_create_location_properties() -> None:
    location_with_min_values: Location = {"id": "pEYNmo1F"}

    assert create_location_properties(location_with_min_values) == {
        "id": "pEYNmo1F",
        "name": "",
        "comment": "",
        "description": "",
        "facility_name": "",
        "level_of_accuracy": "",
    }, "Location props default to empty string."

    location_with_max_values: Location = {
        "id": "pEYNmo1F",
        "point": None,
        "areas": None,
        "name": "Chipinge, Zimbabwe",
        "comment": "Spatial data derived from the Mapathon 2020.",
        "description": "",
        "facility_name": "Clearwater estate",
        "level_of_accuracy": "EXACT_LOCATION",
        "old_id": 4,
        "old_group_id": 13210345,
    }

    assert create_location_properties(location_with_max_values) == {
        "id": "pEYNmo1F",
        "name": "Chipinge, Zimbabwe",
        "comment": "Spatial data derived from the Mapathon 2020.",
        "description": "",
        "facility_name": "Clearwater estate",
        "level_of_accuracy": "EXACT_LOCATION",
    }, "Old props are discarded."


def test_create_export_data() -> None:
    polygon_feature = create_feature(
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
        properties={},
    )
    deals: list[DealValues] = [
        {
            "id": 1,
            "country": None,
            "locations": [
                {"id": "pEYNmo1F", "point": {"lng": 28.03389, "lat": 1.65963}}
            ],
        },
        {
            "id": 1,
            "country": None,
            "locations": [
                {"id": "pEYNmo1F", "point": {"lng": 27.8624853, "lat": -0.179372}},
                {
                    "id": "pEYNmo1F",
                    "areas": create_feature_collection([polygon_feature]),
                },
            ],
        },
    ]

    export_data_point_features = create_export_features("locations", deals)
    export_data_area_features = create_export_features("areas", deals)

    assert len(export_data_point_features) == 2
    assert len(export_data_area_features) == 1

    location_keys = [
        "id",
        "name",
        "comment",
        "description",
        "facility_name",
        "level_of_accuracy",
    ]
    deal_keys = [
        "deal_id",
        "country",
        "region",
    ]
    all_keys = {*location_keys, *deal_keys, "type"}

    assert {
        *export_data_point_features[0]["properties"]
    } == all_keys, "Point feature has location and deal props."

    assert {
        *export_data_area_features[0]["properties"]
    } == all_keys, "Area feature has location and deal props."


def test_create_area_features() -> None:
    location_without_areas: Location = {"id": "pEYNmo1F"}

    with pytest.raises(KeyError, match=r"areas"):
        create_area_features(location_without_areas)

    location_with_empty_areas: Location = {
        "id": "pEYNmo1F",
        "areas": create_feature_collection([]),
    }
    assert (
        len(create_area_features(location_with_empty_areas)) == 0
    ), "No features are created."

    polygon_feature_1 = create_feature(
        geometry=Geometry(
            type="Polygon",
            coordinates=[
                [
                    [29.428485828059678, -17.49703600739376],
                    [29.53962202957308, -17.83144463535156],
                    [29.95784510369191, -17.67825118667062],
                    [29.943221919282394, -17.37705569674266],
                    [29.832085717768194, -17.622512031346076],
                    [29.428485828059678, -17.49703600739376],
                ]
            ],
        ),
        properties={},
    )
    polygon_feature_2 = create_feature(
        geometry=Geometry(
            type="Polygon",
            coordinates=[
                [
                    [29.141871413628365, -17.184364935803544],
                    [29.12139895545417, -17.547236849512586],
                    [29.65075823108731, -18.315221349029912],
                    [29.141871413628365, -17.184364935803544],
                ]
            ],
        ),
        properties={"type": "contract_area"},
    )
    location_with_two_areas: Location = {
        "id": "pEYNmo1F",
        "areas": create_feature_collection([polygon_feature_1, polygon_feature_2]),
    }
    assert (
        len(create_area_features(location_with_two_areas)) == 2
    ), "Creates one feature per area."

    assert (
        create_area_features(location_with_two_areas)[0]["properties"]["type"] == ""
    ), "Type property defaults to empty string."

    assert (
        create_area_features(location_with_two_areas)[1]["properties"]["type"]
        == "contract_area"
    ), "Type property holds area type."
