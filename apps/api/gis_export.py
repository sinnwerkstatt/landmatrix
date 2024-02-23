import json
from typing import Literal, TypedDict, cast

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from rest_framework.decorators import api_view

from apps.api.utils.geojson import (
    Feature,
    FeatureCollection,
    FeatureProperties,
    add_properties,
    create_feature,
    create_feature_collection,
)
from apps.landmatrix.models.deal import DealOld
from apps.utils import qs_values_to_dict

ExportType = Literal["locations", "areas"]

VALID_EXPORT_TYPES: list[ExportType] = ["locations", "areas"]


from django.db.models import Q


filter_ops = {
    "EQ": "",
    "LT": "__lt",
    "LE": "__lte",
    "GE": "__gte",
    "GT": "__gt",
    "IN": "__in",
    "CONTAINS": "__contains",
    "CONTAINED_BY": "__contained_by",
    "OVERLAP": "__overlap",
}


def parse_filters(filters):
    ret = Q()
    if not filters:
        return ret
    for filtr in filters:
        field = filtr["field"].replace(".", "__")
        op = filtr.get("operation") or "EQ"
        val = filtr["value"]
        if (
            isinstance(val, list)
            and len(val) == 1
            and op in ["EQ", "LT", "LE", "GE", "GT"]
        ):
            val = val[0]
        operation = filter_ops[op]

        filter_operation = Q(**{f"{field}{operation}": val})
        if filtr.get("allow_null"):
            filter_operation |= Q(**{f"{field}": None})
        if filtr.get("exclusion"):
            filter_operation = ~filter_operation
        ret &= filter_operation
    return ret


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
    return JsonResponse(
        create_feature_collection(export_features),
        headers={
            "Content-Disposition": f"attachment; filename={export_type}.geojson",
        },
    )


class Point(TypedDict):
    lat: float
    lng: float


class BaseLocation(TypedDict):
    id: str


class Location(BaseLocation, total=False):
    name: str
    point: Point | None
    areas: FeatureCollection | None
    comment: str
    description: str
    old_id: int
    old_group_id: int
    facility_name: str
    level_of_accuracy: str


class RegionValues(TypedDict):
    name: str


class CountryValues(TypedDict):
    name: str
    region: RegionValues | None


class DealValues(TypedDict):
    id: int
    locations: list[Location]
    country: CountryValues | None


def get_deal_values(request: WSGIRequest) -> list[DealValues]:
    qs_deals = DealOld.objects.visible(
        user=request.user, subset=request.GET.get("subset", "PUBLIC")
    ).exclude(geojson=None)

    if filters := request.GET.get("filters"):
        qs_deals = qs_deals.filter(parse_filters(json.loads(filters)))

    fields = ["id", "country__name", "country__region__name", "locations"]
    return qs_values_to_dict(qs_deals, fields)


def create_export_features(
    export_type: ExportType,
    deal_values: list[DealValues],
) -> list[Feature]:
    all_features: list[Feature] = []
    for deal in deal_values:
        deal_properties = create_deal_properties(deal)

        features: list[Feature] = []
        for location in deal["locations"]:
            if export_type == "locations":
                if "point" in location.keys() and location["point"]:
                    features += [create_point_feature(location)]

            if export_type == "areas":
                if "areas" in location.keys() and location["areas"]:
                    features += create_area_features(location)

        all_features += [add_properties(deal_properties, f) for f in features]

    return all_features


def create_point_feature(
    location: Location,
) -> Feature:
    point = cast(Point, location["point"])

    return create_feature(
        geometry={
            "type": "Point",
            "coordinates": [point["lng"], point["lat"]],
        },
        properties={
            "type": "point",
            **create_location_properties(location),
        },
    )


def create_area_features(
    location: Location,
) -> list[Feature]:
    areas = cast(FeatureCollection, location["areas"])

    return [
        create_feature(
            geometry=f["geometry"],
            properties={
                "type": f["properties"].get("type") or "",
                **create_location_properties(location),
            },
        )
        for f in areas["features"]
    ]


def create_deal_properties(deal: DealValues) -> FeatureProperties:
    # prefer or syntax over get(key, default_val) in case val is None
    country = deal.get("country") or cast(CountryValues, {})
    region = country.get("region") or cast(RegionValues, {})
    return {
        "deal_id": deal.get("id"),
        "country": country.get("name") or "",
        "region": region.get("name") or "",
    }


def create_location_properties(location: Location) -> FeatureProperties:
    return {
        k: location.get(k) or "" if k in location else ""  # type: ignore
        for k in [
            "id",
            "name",
            "comment",
            "description",
            "facility_name",
            "level_of_accuracy",
        ]
    }
