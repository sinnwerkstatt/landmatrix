from django.db.models import QuerySet, Value
from django.db.models.functions import JSONObject
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.response import Response

from apps.landmatrix.models.deal import DealHull, DealVersion
from apps.landmatrix.utils import openapi_filters_parameters, parse_filters

from .utils.geojson import Feature, create_feature_collection

GEOJSON_FEATURE_COLLECTION_SCHEMA = {
    "type": "object",
    "properties": {
        "type": {"type": "string", "enum": ["FeatureCollection"]},
        "features": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "type": {"type": "string", "enum": ["Feature"]},
                    "geometry": {
                        "type": "object",
                        "properties": {
                            "type": {
                                "type": "string",
                                "enum": ["Point", "Polygon", "MultiPolygon"],
                            },
                            "coordinates": {"type": "array"},
                        },
                        "required": ["type", "coordinates"],
                    },
                    "properties": {"type": "object"},
                },
                "required": ["type", "geometry", "properties"],
            },
        },
    },
    "required": ["type", "features"],
}


@extend_schema(
    parameters=openapi_filters_parameters,
    responses={200: GEOJSON_FEATURE_COLLECTION_SCHEMA},
)
@api_view()
def gis_export_areas(request: Request) -> Response:
    qs_deal_versions = _get_deal_version_qs(request)
    # ensure that all deal versions have locations with areas
    qs_deal_version = qs_deal_versions.filter(
        locations__isnull=False,
        locations__areas__isnull=False,
    ).distinct()

    area_features = _build_area_features(qs_deal_version)

    headers = None
    if request.query_params.get("format") == "json":
        if deal_id := request.query_params.get("deal_id"):
            filename = f"areas_{deal_id}.geojson"
        else:
            filename = "areas.geojson"
        headers = {"Content-Disposition": f"attachment; filename={filename}"}
    return Response(create_feature_collection(area_features), headers=headers)


@extend_schema(
    parameters=openapi_filters_parameters,
    responses={200: GEOJSON_FEATURE_COLLECTION_SCHEMA},
)
@api_view()
def gis_export_locations(request: Request) -> Response:
    qs_deal_versions = _get_deal_version_qs(request)
    # ensure that all deal versions have locations with points
    qs_deal_versions = qs_deal_versions.filter(
        locations__isnull=False,
        locations__point__isnull=False,
    )

    location_features = _build_location_features(qs_deal_versions)

    headers = None
    if request.query_params.get("format") == "json":
        if deal_id := request.query_params.get("deal_id"):
            filename = f"locations_{deal_id}.geojson"
        else:
            filename = "locations.geojson"
        headers = {"Content-Disposition": f"attachment; filename={filename}"}
    return Response(create_feature_collection(location_features), headers=headers)


def _get_deal_version_qs(request: Request) -> QuerySet[DealVersion]:
    qs_deal_hull: QuerySet[DealHull] = DealHull.objects.visible(
        user=request.user,
        subset=request.GET.get("subset", "PUBLIC"),
    )
    if deal_id := request.query_params.get("deal_id"):
        try:
            hull = qs_deal_hull.get(id=deal_id)
        except DealHull.DoesNotExist:
            raise NotFound(f"Deal {deal_id} does not exist.")
        return DealVersion.objects.filter(id=hull.active_version_id).order_by("deal_id")

    qs_deal_hull = qs_deal_hull.filter(parse_filters(request))

    return DealVersion.objects.filter(
        id__in=qs_deal_hull.values_list("active_version_id", flat=True)
    ).order_by("deal_id")


_DEAL_PROPS = dict(
    deal_id="deal__id",
    country="deal__country__name",
    region="deal__country__region__name",
)

_LOCATION_PROPS = dict(
    id="locations__nid",
    name="locations__name",
    level_of_accuracy="locations__level_of_accuracy",
    facility_name="locations__facility_name",
    description="locations__description",
    comment="locations__comment",
)


def _build_area_features(qs: QuerySet[DealVersion]) -> list[Feature]:
    return list(
        qs.annotate(
            as_feature=JSONObject(
                type=Value("Feature"),
                geometry="locations__areas__area",
                properties=JSONObject(
                    type="locations__areas__type",
                    **_DEAL_PROPS,
                    **_LOCATION_PROPS,
                ),
            ),
        ).values_list("as_feature", flat=True)
    )


def _build_location_features(qs: QuerySet[DealVersion]) -> list[Feature]:
    return list(
        qs.annotate(
            as_feature=JSONObject(
                type=Value("Feature"),
                geometry="locations__point",
                properties=JSONObject(
                    type=Value("point"),
                    **_DEAL_PROPS,
                    **_LOCATION_PROPS,
                ),
            ),
        ).values_list("as_feature", flat=True)
    )
