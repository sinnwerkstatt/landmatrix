from typing import Any, Literal, TypedDict

# Unfortunately, I wasn't able to find a stub library for geojson data.
# These TypedDicts are not exhaustive. They only include the keys I needed.
GeometryType = Literal["Point", "Polygon", "MultiPolygon"]

# https://www.rfc-editor.org/rfc/rfc7946#section-3.2
FeatureProperties = dict[str, object]  # any JSON object or null


class Geometry(TypedDict):
    type: GeometryType
    coordinates: Any


class Feature(TypedDict):
    type: Literal["Feature"]
    geometry: Geometry
    properties: FeatureProperties


class FeatureCollection(TypedDict):
    type: Literal["FeatureCollection"]
    features: list[Feature]


def is_geometry_type(geometry_type: GeometryType, feature: Feature) -> bool:
    return feature["geometry"]["type"] == geometry_type


def create_feature(geometry: Geometry, properties: FeatureProperties) -> Feature:
    return {
        "type": "Feature",
        "geometry": geometry,
        "properties": properties,
    }


def create_feature_collection(features: list[Feature]) -> FeatureCollection:
    return {
        "type": "FeatureCollection",
        "features": features,
    }


def add_properties(
    properties: FeatureProperties,
    feature: Feature,
) -> Feature:
    return {
        **feature,  # type: ignore
        "properties": {
            **feature["properties"],
            **properties,
        },
    }
