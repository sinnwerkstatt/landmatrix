import json
from typing import Literal, TypedDict, Callable, Any

from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from rest_framework.decorators import api_view

from apps.graphql.tools import parse_filters
from apps.landmatrix.models.deal import Deal
from apps.utils import qs_values_to_dict

GeometryType = Literal["Point", "Polygon", "MultiPolygon"]


# Unfortunately, I wasn't able to find a stub library for geojson data.
# These TypedDicts are not exhaustive. They only include the keys I needed.
class Geometry(TypedDict):
    type: GeometryType


class Feature(TypedDict, total=False):
    properties: dict[str, str]
    geometry: Geometry


class FeatureCollection(TypedDict):
    type: Literal["FeatureCollection"]
    features: list[Feature]


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

    qs = create_deal_qs(request)
    response = JsonResponse(create_export_data(export_type, qs))
    response["Content-Disposition"] = f'attachment; filename="{export_type}.geojson"'
    return response


def create_deal_qs(request: WSGIRequest) -> QuerySet:
    qs_deals = Deal.objects.visible(
        user=request.user, subset=request.GET.get("subset", "PUBLIC")
    ).exclude(geojson=None)

    if filters := request.GET.get("filters"):
        qs_deals = qs_deals.filter(parse_filters(json.loads(filters)))

    return qs_deals


def create_export_data(export_type: ExportType, qs: QuerySet) -> FeatureCollection:
    export_type_to_filter_map: dict[ExportType, Callable[[Feature], bool]] = {
        "areas": is_polygon,
        "points": is_point,
    }

    fields = ["id", "country__name", "country__region__name", "geojson"]

    location_keys = ["id", "type", "name", "spatial_accuracy"]

    all_features: list[Feature] = []
    for deal in qs_values_to_dict(qs, fields):
        deal_props = create_deal_properties(deal)
        features = filter(
            export_type_to_filter_map[export_type],
            deal["geojson"].get("features") or [],
        )

        for feat in features:
            old_props = feat.get("properties") or {}
            location_props = {key: old_props.get(key) or "" for key in location_keys}

            all_features += [{**feat, "properties": {**location_props, **deal_props}}]

    return create_feature_collection(all_features)


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


def create_deal_properties(deal: dict[str, Any]) -> dict[str, str]:
    # prefer or syntax over get(key, default_val) in case val is None
    country = deal.get("country") or {}
    region = country.get("region") or {}
    return {
        "deal_id": str(deal.get("id")),
        "country": country.get("name") or "",
        "region": region.get("name") or "",
    }
