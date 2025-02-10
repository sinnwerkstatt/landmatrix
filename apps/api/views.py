import json

from django.db.models import Case, CharField, Count, F, Q, Sum, Value, When
from django.db.models.functions import Concat, JSONObject
from django.http import HttpRequest, JsonResponse
from django.middleware.csrf import get_token
from django.utils import timezone, translation
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_GET
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework.response import Response
from wagtail.rich_text import expand_db_html

from apps.accounts.models import User
from apps.api.serializers import (
    ChartDescriptions,
    CountryInvestmentsAndRankings,
    SearchedInvestorSerializer,
)
from apps.landmatrix.charts import get_deal_top_investments, web_of_transnational_deals
from apps.landmatrix.models.deal import DealHull, DealWorkflowInfo
from apps.landmatrix.models.investor import InvestorHull, InvestorWorkflowInfo
from apps.landmatrix.permissions import is_reporter_or_higher
from apps.landmatrix.utils import openapi_filters_parameters, parse_filters
from apps.wagtailcms.models import ChartDescriptionsSettings


def quick_search(request: HttpRequest) -> JsonResponse:
    q = request.GET.get("q")

    items = list(
        DealHull.objects.visible(request.user, "ACTIVE")
        .filter(id__contains=q)
        .annotate(
            is_public=Case(
                When(active_version_id__isnull=False, then="active_version__is_public"),
                default="draft_version__is_public",
            )
        )
        .values("id", "is_public")
        .annotate(
            country_name=F("country__name"),
            type=Value("deal"),
            href=Concat(
                Value("/deal/"),
                "id",
                Value("/"),
                output_field=CharField(),
            ),
        )
    ) + list(
        InvestorHull.objects.visible(request.user, "ACTIVE")
        .filter(Q(id__icontains=q) | Q(active_version__name__icontains=q))
        .values("id")
        .annotate(
            name=F("active_version__name"),
            name_unknown=F("active_version__name_unknown"),
            type=Value("investor"),
            href=Concat(
                Value("/investor/"),
                "id",
                Value("/"),
                output_field=CharField(),
            ),
        )
    )
    return JsonResponse({"items": items})


@extend_schema(
    parameters=[
        OpenApiParameter("q", description="Query string", required=True, type=str)
    ],
    responses={200: SearchedInvestorSerializer(many=True)},
)
@api_view(["GET"])
def investor_search(request) -> Response:
    if not request.user.is_authenticated:
        raise NotAuthenticated
    q = request.GET.get("q")
    if not q or len(q) <= 2:
        return Response([])

    qs = InvestorHull.objects.normal().annotate(
        selected_version=Case(
            When(
                active_version_id__isnull=False,
                then=JSONObject(
                    id="active_version_id",
                    modified_at="active_version__modified_at",
                    name="active_version__name",
                    name_unknown="active_version__name_unknown",
                    country_id="active_version__country_id",
                    country_name="active_version__country__name",
                ),
            ),
            default=JSONObject(
                id="draft_version_id",
                modified_at="draft_version__modified_at",
                name="draft_version__name",
                name_unknown="draft_version__name_unknown",
                country_id="draft_version__country_id",
                country_name="draft_version__country__name",
            ),
        )
    )

    for term in q.split(" "):
        qs = qs.filter(
            Q(selected_version__name__icontains=term)
            | Q(selected_version__country_name__icontains=term)
        )

    investors = qs.order_by("id").values(
        "id",
        "active_version_id",
        "draft_version_id",
        "deleted",
        "first_created_at",
        "first_created_by_id",
        "selected_version",
    )

    return Response(investors)


@extend_schema(responses=ChartDescriptions)
@api_view(["GET"])
def chart_descriptions(request):
    language = request.GET.get("lang", "en")
    with translation.override(language):
        cds: ChartDescriptionsSettings = ChartDescriptionsSettings.load(
            request_or_site=request
        )
        return Response(
            {
                "web_of_transnational_deals": expand_db_html(
                    cds.web_of_transnational_deals
                ),
                "dynamics_overview": expand_db_html(cds.dynamics_overview),
                "produce_info_map": expand_db_html(cds.produce_info_map),
                "global_web_of_investments": expand_db_html(
                    cds.global_web_of_investments
                ),
            }
        )


@require_GET
def get_csrf(request):
    return JsonResponse({"token": get_token(request)})


@extend_schema(
    parameters=[
        OpenApiParameter("CID", description="Country ID", required=True, type=int)
    ]
    + openapi_filters_parameters,
    responses=CountryInvestmentsAndRankings,
)
@api_view(["get"])
def country_investments_and_rankings(request) -> Response:
    country_id = request.GET.get("CID")
    investments = get_deal_top_investments(request)
    return Response(
        {
            "investing": [
                {
                    "country_id": country_id,
                    "size": bucket["size"],
                    "count": bucket["count"],
                }
                for country_id, bucket in investments["incoming"][
                    int(country_id)
                ].items()
            ],
            "invested": [
                {
                    "country_id": country_id,
                    "size": bucket["size"],
                    "count": bucket["count"],
                }
                for country_id, bucket in investments["outgoing"][
                    int(country_id)
                ].items()
            ],
        }
    )


@require_GET
def deal_aggregations(request):
    deals = DealHull.objects.public().filter(parse_filters(request)).distinct()
    return JsonResponse(
        {
            "current_negotiation_status": list(
                deals.order_by("active_version__current_negotiation_status", "id")
                .values(value=F("active_version__current_negotiation_status"))
                .annotate(count=Count("pk"))
                .annotate(size=Sum("active_version__deal_size"))
            )
        }
    )


def get_web_of_transnational_deals(request):
    return JsonResponse(web_of_transnational_deals(request))


def global_map_of_investments(request):
    return JsonResponse(get_deal_top_investments(request))


def workflow_info_add_reply(
    request,
    wfitype: str,
    pk: int,
) -> JsonResponse:
    user: User = request.user

    if not is_reporter_or_higher(user):
        raise PermissionDenied("MISSING_AUTHORIZATION")

    data = json.loads(request.body)

    if wfitype == "deal":
        wfi: DealWorkflowInfo = DealWorkflowInfo.objects.get(pk=pk)
    elif wfitype == "investor":
        wfi: InvestorWorkflowInfo = InvestorWorkflowInfo.objects.get(pk=pk)
    else:
        return JsonResponse({"ok": False})

    if not wfi.replies:
        wfi.replies = []
    wfi.replies += [
        {
            "timestamp": timezone.now().isoformat(),
            "user_id": user.id,
            "comment": data["comment"],
        }
    ]
    wfi.save()

    sending_user = f"{user.first_name} {user.last_name} ({user.username})"
    comment = f"The user {sending_user} left the following response at {wfi.get_object_url()}:\n\n"
    comment += f'"{data["comment"]}"'

    relevant_user_ids = [wfi.from_user_id, wfi.to_user_id] + [
        x["user_id"] for x in wfi.replies
    ]
    receiving_users = User.objects.filter(id__in=relevant_user_ids).exclude(id=user.id)
    for recipient in receiving_users:
        recipient.email_user("[Land Matrix] " + _("New feedback reply"), comment)

    return JsonResponse({"ok": True})


def workflow_info_resolve(
    request,
    wfitype: str,
    pk: int,
) -> JsonResponse:
    user: User = request.user

    if not is_reporter_or_higher(user):
        raise PermissionDenied("MISSING_AUTHORIZATION")

    if wfitype == "deal":
        wfi: DealWorkflowInfo = DealWorkflowInfo.objects.get(pk=pk)
    elif wfitype == "investor":
        wfi: InvestorWorkflowInfo = InvestorWorkflowInfo.objects.get(pk=pk)
    else:
        return JsonResponse({"ok": False})

    wfi.resolved = True
    wfi.save()
    return JsonResponse({"ok": True})


# def global_rankings(_obj, _info, count=10, filters=None):
#     qs = DealOld.objects.active()
#
#     if filters:
#         qs = qs.filter(parse_filters(filters))
#
#     return {
#         "ranking_deal": list(qs.get_deal_country_rankings())[:count],
#         "ranking_investor": list(qs.get_investor_country_rankings())[:count],
#     }
