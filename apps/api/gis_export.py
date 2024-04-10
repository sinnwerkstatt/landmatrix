from typing import Literal

from django.db.models import QuerySet, Value
from django.db.models.functions import JSONObject
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.request import Request

from apps.api.utils.geojson import Feature, create_feature_collection

from apps.landmatrix.models.new import DealHull, DealVersion
from apps.landmatrix.utils import parse_filters

ExportType = Literal["locations", "areas"]

VALID_EXPORT_TYPES: list[ExportType] = ["locations", "areas"]


@api_view()
def gis_export_areas(request: Request) -> JsonResponse:
    qs_deal_version = get_deal_version_qs(request)

    # ensure that all deal versions have locations with areas
    qs_deal_version = qs_deal_version.filter(
        locations__isnull=False,
        locations__areas__isnull=False,
    ).distinct()

    area_features = build_area_features(qs_deal_version)

    return JsonResponse(
        create_feature_collection(area_features),
        headers={"Content-Disposition": f"attachment; filename=areas.geojson"},
    )


@api_view()
def gis_export_locations(request: Request) -> JsonResponse:
    qs_deal_version = get_deal_version_qs(request)

    # ensure that all deal versions have locations with points
    qs_deal_version = qs_deal_version.filter(
        locations__isnull=False,
        locations__point__isnull=False,
    )

    location_features = build_location_features(qs_deal_version)

    return JsonResponse(
        create_feature_collection(location_features),
        headers={
            "Content-Disposition": f"attachment; filename=locations.geojson",
        },
    )


def get_deal_version_qs(request: Request) -> QuerySet[DealVersion]:
    qs_deal_hull: QuerySet[DealHull] = DealHull.objects.visible(
        user=request.user,
        subset=request.GET.get("subset", "PUBLIC"),
    ).filter(parse_filters(request))

    return DealVersion.objects.filter(
        id__in=qs_deal_hull.values_list("active_version_id", flat=True)
    ).order_by("deal_id")


DEAL_PROPS = dict(
    deal_id="deal__id",
    country="deal__country__name",
    region="deal__country__region__name",
)

LOCATION_PROPS = dict(
    id="locations__nid",
    name="locations__name",
    level_of_accuracy="locations__level_of_accuracy",
    facility_name="locations__facility_name",
    description="locations__description",
    comment="locations__comment",
)


def build_area_features(qs: QuerySet[DealVersion]) -> list[Feature]:
    return list(
        qs.annotate(
            as_feature=JSONObject(
                type=Value("Feature"),
                geometry="locations__areas__area",
                properties=JSONObject(
                    type="locations__areas__type",
                    **DEAL_PROPS,
                    **LOCATION_PROPS,
                ),
            ),
        ).values_list("as_feature", flat=True)
    )


def build_location_features(qs: QuerySet[DealVersion]) -> list[Feature]:
    return list(
        qs.annotate(
            as_feature=JSONObject(
                type=Value("Feature"),
                geometry="locations__point",
                properties=JSONObject(
                    type=Value("point"),
                    **DEAL_PROPS,
                    **LOCATION_PROPS,
                ),
            ),
        ).values_list("as_feature", flat=True)
    )
