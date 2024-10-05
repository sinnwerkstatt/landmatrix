from drf_spectacular.utils import OpenApiParameter, extend_schema, inline_serializer

from django.db.models.expressions import F
from django.http import HttpResponse, HttpResponseBadRequest
from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response

from apps.landmatrix.models.deal import DealHull, DealVersion
from apps.landmatrix.models.investor import InvestorHull, InvestorVersion
from apps.landmatrix.permissions import IsEditorOrHigher
from apps.landmatrix.quality_indicators import DEAL_QIS, INVESTOR_QIS
from apps.landmatrix.quality_indicators.deal import annotate_counts, DEAL_SUBSETS

from .serializers import (
    QualityIndicatorSerializer,
    QueryParamsSerializer,
    DealQISnapshotSerializer,
    InvestorQISnapshotSerializer,
    QualityIndicatorSubsetSerializer,
)
from apps.landmatrix.models.quality_indicators import DealQISnapshot, InvestorQISnapshot


@extend_schema(
    operation_id="qi_specs",
    responses={
        200: inline_serializer(
            name="QISpecsResponse",
            fields={
                "investor": QualityIndicatorSerializer(many=True),
                "deal": QualityIndicatorSerializer(many=True),
                "deal_subset": QualityIndicatorSubsetSerializer(many=True),
            },
        )
    },
)
@api_view()
@permission_classes([IsEditorOrHigher])
def specs(request: Request) -> Response:
    return Response(
        data={
            "investor": QualityIndicatorSerializer(INVESTOR_QIS, many=True).data,
            "deal": QualityIndicatorSerializer(DEAL_QIS, many=True).data,
            "deal_subset": QualityIndicatorSubsetSerializer(
                DEAL_SUBSETS, many=True
            ).data,
        }
    )


@extend_schema(
    operation_id="qi_counts",
    parameters=[
        OpenApiParameter(
            "region_id",
            description="Filter by Land Matrix region.",
            required=False,
            type=int,
        ),
        OpenApiParameter(
            "country_id",
            description="Filter by country.",
            required=False,
            type=int,
        ),
    ],
    responses={
        200: inline_serializer(
            name="QICountsResponse",
            fields={
                "investor": inline_serializer(
                    name="InvestorQICounts",
                    fields={qi.key: serializers.IntegerField() for qi in INVESTOR_QIS}
                    | {"total": serializers.IntegerField()},
                ),
                "deal": inline_serializer(
                    name="DealQICounts",
                    fields={qi.key: serializers.IntegerField() for qi in DEAL_QIS}
                    | {"total": serializers.IntegerField()},
                ),
            },
        ),
    },
)
@api_view()
@permission_classes([IsEditorOrHigher])
def counts(request: Request) -> Response:
    region_id = request.query_params.get("region_id")
    country_id = request.query_params.get("country_id")

    def get_deal_counts():
        qs = DealHull.objects.public()
        if region_id:
            qs = qs.filter(country__region_id=region_id)
        if country_id:
            qs = qs.filter(country__id=country_id)
        ids = qs.values_list("active_version_id", flat=True)
        return {
            qi.key: DealVersion.objects.filter(id__in=ids)
            .annotate(counts=annotate_counts())
            .distinct()
            .filter(qi.query())
            .distinct()
            .count()
            for qi in DEAL_QIS
        } | {"total": qs.count()}

    def get_investor_counts():
        qs = InvestorHull.objects.active()
        if region_id:
            qs = qs.filter(active_version__country__region_id=region_id)
        if country_id:
            qs = qs.filter(active_version__country__id=country_id)
        ids = qs.values_list("active_version_id", flat=True)

        return {
            qi.key: (
                InvestorVersion.objects.filter(id__in=ids)
                .filter(qi.query())
                .distinct()
                .count()
            )
            for qi in INVESTOR_QIS
        } | {"total": qs.count()}

    return Response(
        data={
            "deal": get_deal_counts(),
            "investor": get_investor_counts(),
        }
    )


@extend_schema(
    operation_id="qi_stats",
    responses={
        200: inline_serializer(
            name="QIStatsResponse",
            fields={
                "deal": DealQISnapshotSerializer(many=True),
                "investor": InvestorQISnapshotSerializer(many=True),
            },
        ),
    },
)
@api_view()
@permission_classes([IsEditorOrHigher])
def stats(request: Request) -> Response:

    return Response(
        data={
            "deal": DealQISnapshotSerializer(
                DealQISnapshot.objects.all(),
                many=True,
            ).data,
            "investor": InvestorQISnapshotSerializer(
                InvestorQISnapshot.objects.all(),
                many=True,
            ).data,
        }
    )


@extend_schema(
    operation_id="qi_investor_list",
    parameters=[
        OpenApiParameter(
            "qi",
            description="Filter investors by quality indicator.",
            required=True,
            type=str,
            enum=[qi.key for qi in INVESTOR_QIS],
        ),
        OpenApiParameter(
            "inverse",
            description="Get the inverse query set.",
            required=False,
            default=False,
            type=bool,
        ),
        OpenApiParameter(
            "region_id",
            description="Filter by Land Matrix region.",
            required=False,
            type=int,
        ),
        OpenApiParameter(
            "country_id",
            description="Filter by country.",
            required=False,
            type=int,
        ),
    ],
    responses={
        200: inline_serializer(
            name="QIInvestorListResponse",
            fields={
                "id": serializers.IntegerField(),
                "name": serializers.CharField(),
                "version_id": serializers.IntegerField(),
                "country_id": serializers.IntegerField(),
                "created_at": serializers.DateTimeField(),
                "modified_at": serializers.DateTimeField(),
            },
            many=True,
        ),
    },
)
@api_view()
@permission_classes([IsEditorOrHigher])
def investors(request: Request) -> Response | HttpResponse:
    qi = request.query_params.get("qi")
    keys = [qi.key for qi in INVESTOR_QIS]

    if qi not in keys:
        return HttpResponseBadRequest("Invalid qi")

    qi_index = keys.index(qi)
    query = INVESTOR_QIS[qi_index].query()

    serializer = QueryParamsSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)

    if serializer.validated_data["inverse"]:
        query = ~query

    ids = InvestorHull.objects.active().values_list(
        "active_version_id",
        flat=True,
    )
    qs = InvestorVersion.objects.filter(id__in=ids).filter(query)
    if region_id := request.query_params.get("region_id"):
        qs = qs.filter(country__region_id=region_id)
    if country_id := request.query_params.get("country_id"):
        qs = qs.filter(country__id=country_id)
    qs = (
        qs.distinct()
        .order_by("id")
        .values(
            version_id=F("id"),
        )
        .values(
            "name",
            id=F("investor_id"),
            country_id=F("country_id"),
            created_at=F("investor__first_created_at"),
            modified_at=F("created_at"),
        )
    )
    return Response(data=list(qs))


@extend_schema(
    operation_id="qi_deal_list",
    parameters=[
        OpenApiParameter(
            "qi",
            description="Filter deals by quality indicator.",
            required=True,
            type=str,
            enum=[qi.key for qi in DEAL_QIS],
        ),
        OpenApiParameter(
            "inverse",
            description="Get the inverse query set.",
            required=False,
            default=False,
            type=bool,
        ),
        OpenApiParameter(
            "region_id",
            description="Filter by Land Matrix region.",
            required=False,
            type=int,
        ),
        OpenApiParameter(
            "country_id",
            description="Filter by country.",
            required=False,
            type=int,
        ),
    ],
    responses={
        200: inline_serializer(
            name="QIDealListResponse",
            fields={
                "id": serializers.IntegerField(),
                "deal_size": serializers.FloatField(),
                "version_id": serializers.IntegerField(),
                "country_id": serializers.IntegerField(),
                "created_at": serializers.DateTimeField(),
                "modified_at": serializers.DateTimeField(),
                "fully_updated_at": serializers.DateTimeField(),
                "current_intention_of_investment": serializers.ListField(
                    child=serializers.CharField()
                ),
                "current_negotiation_status": serializers.ListField(
                    child=serializers.CharField()
                ),
                "current_implementation_status": serializers.ListField(
                    child=serializers.CharField()
                ),
            },
            many=True,
        ),
    },
)
@api_view()
@permission_classes([IsEditorOrHigher])
def deals(request: Request) -> Response | HttpResponse:
    qi = request.query_params.get("qi")
    keys = [qi.key for qi in DEAL_QIS]

    try:
        qi_index = keys.index(qi)
    except ValueError:
        return HttpResponseBadRequest("Invalid qi")

    query = DEAL_QIS[qi_index].query()

    serializer = QueryParamsSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)

    if serializer.validated_data["inverse"]:
        query = ~query

    qs = DealHull.objects.public()

    if region_id := request.query_params.get("region_id"):
        qs = qs.filter(country__region_id=region_id)
    if country_id := request.query_params.get("country_id"):
        qs = qs.filter(country__id=country_id)

    deal_ids = qs.values_list("active_version_id", flat=True)

    version_ids = (
        DealVersion.objects.filter(id__in=deal_ids)
        .annotate(counts=annotate_counts())
        .filter(query)
        .distinct()
        .values_list("id", flat=True)
    )

    qs = (
        DealHull.objects.filter(active_version_id__in=version_ids)
        .values(
            "id",
            "country_id",
            "fully_updated_at",
            deal_size=F("active_version__deal_size"),
            version_id=F("active_version_id"),
            created_at=F("first_created_at"),
            modified_at=F("active_version__created_at"),
            current_intention_of_investment=F(
                "active_version__current_intention_of_investment",
            ),
            current_negotiation_status=F(
                "active_version__current_negotiation_status",
            ),
            current_implementation_status=F(
                "active_version__current_implementation_status",
            ),
        )
        .order_by("id")
    )
    return Response(data=list(qs))
