import json
from typing import Any, Callable, Literal, TypedDict, cast

# noinspection PyPep8Naming
import ramda as R  # type: ignore

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from rest_framework.decorators import api_view

from apps.graphql.tools import parse_filters
from apps.landmatrix.models.deal import Deal
from apps.utils import qs_values_to_dict

# Unfortunately, I wasn't able to find a stub library for geojson data.
# These TypedDicts are not exhaustive. They only include the keys I needed.
GeometryType = Literal["Point", "Polygon", "MultiPolygon"]


class Geometry(TypedDict):
    type: GeometryType
    coordinates: Any


class Feature(TypedDict):
    type: Literal["Feature"]
    geometry: Geometry
    properties: dict[str, str]


class FeatureCollection(TypedDict):
    type: Literal["FeatureCollection"]
    features: list[Feature]


DealValues = dict[str, Any]

ExportType = Literal["points", "areas"]

VALID_EXPORT_TYPES: list[ExportType] = ["points", "areas"]


@api_view()
def gis_export(request) -> HttpResponse:
    """Export deal gis data."""
    export_type = request.GET.get("type")

    if not export_type:
        return HttpResponseBadRequest(
            "Missing query parameter 'type'. "
            f"Valid values are: {', '.join(VALID_EXPORT_TYPES)}."
        )

    if export_type not in VALID_EXPORT_TYPES:
        return HttpResponseBadRequest(
            f"Invalid 'type' value: '{export_type}'. "
            f"Valid values are: {', '.join(VALID_EXPORT_TYPES)}."
        )

    deal_values = get_deal_values(request)
    export_features = create_export_features(export_type, deal_values)
    response = JsonResponse(create_feature_collection(export_features))
    response["Content-Disposition"] = f'attachment; filename="{export_type}.geojson"'
    return response


def get_deal_values(request: WSGIRequest) -> list[DealValues]:
    qs_deals = Deal.objects.visible(
        user=request.user, subset=request.GET.get("subset", "PUBLIC")
    ).exclude(geojson=None)

    if filters := request.GET.get("filters"):
        qs_deals = qs_deals.filter(parse_filters(json.loads(filters)))

    fields = ["id", "country__name", "country__region__name", "geojson"]
    return qs_values_to_dict(qs_deals, fields)


def create_export_features(
    export_type: ExportType,
    deal_values: list[DealValues],
) -> list[Feature]:
    all_features: list[Feature] = []
    for deal in deal_values:
        features = R.pipe(
            R.path(["geojson", "features"]),
            R.default_to([]),
            R.filter(get_feature_filter_fn(export_type)),
            R.map(fix_feature_properties(deal)),
        )(deal)
        all_features.extend(features)

    return all_features


def fix_feature_properties(deal: DealValues) -> Callable[[Feature], Feature]:
    return lambda feature: cast(
        Feature,
        {
            **feature,
            "properties": {
                **get_location_properties(feature),
                **create_deal_properties(deal),
            },
        },
    )


def get_location_properties(feature: Feature) -> dict[str, str]:
    location_keys = ["id", "type", "name", "spatial_accuracy"]

    all_props = feature.get("properties") or {}
    return {key: all_props.get(key) or "" for key in location_keys}


def is_geometry_type(geometry_type: GeometryType, feature: Feature) -> bool:
    return feature["geometry"]["type"] == geometry_type


def is_point(feature: Feature) -> bool:
    return is_geometry_type("Point", feature)


def is_polygon(feature: Feature) -> bool:
    polygon_types: list[GeometryType] = ["Polygon", "MultiPolygon"]
    return any(is_geometry_type(x, feature) for x in polygon_types)


def create_feature_collection(features: list[Feature]) -> FeatureCollection:
    return {
        "type": "FeatureCollection",
        "features": features,
    }


def get_feature_filter_fn(export_type: ExportType):
    feature_filter_fns: dict[ExportType, Callable[[Feature], bool]] = {
        "areas": is_polygon,
        "points": is_point,
    }
    return feature_filter_fns[export_type]


def create_deal_properties(deal: dict[str, Any]) -> dict[str, str]:
    # prefer or syntax over get(key, default_val) in case val is None
    country = deal.get("country") or {}
    region = country.get("region") or {}
    return {
        "deal_id": str(deal.get("id")),
        "country": country.get("name") or "",
        "region": region.get("name") or "",
    }
