from apps.api.utils.geojson import (
    Feature,
    add_properties,
    create_feature_collection,
)


def test_create_feature_collection() -> None:
    features: list[Feature] = []
    assert create_feature_collection(features) == {
        "type": "FeatureCollection",
        "features": features,
    }


def test_add_properties() -> None:
    feature: Feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [32.71813, -20.1129],
        },
        "properties": {
            "first": "string",
            "second": 123,
        },
    }

    assert add_properties({"third": 0.321}, feature)["properties"] == {
        "first": "string",
        "second": 123,
        "third": 0.321,
    }, "Adds new properties."

    assert add_properties({"first": 0.321}, feature)["properties"] == {
        "first": 0.321,
        "second": 123,
    }, "Overwrites existing properties."
