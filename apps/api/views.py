import json

from django.core.exceptions import PermissionDenied
from django.db.models import F, Q, QuerySet, Count, Sum
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.utils import timezone, translation
from django.views.decorators.http import require_GET
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotAuthenticated, PermissionDenied

from apps.blog.models import BlogCategory, BlogPage
from apps.landmatrix.charts import get_deal_top_investments, web_of_transnational_deals
from apps.landmatrix.forms.deal import DealForm
from apps.landmatrix.forms.deal_submodels import get_submodels_fields
from apps.landmatrix.forms.investor import InvestorForm, InvestorVentureInvolvementForm
from apps.landmatrix.models.investor import Investor
from apps.landmatrix.models.new import (
    DealHull,
    DealWorkflowInfo2,
    InvestorWorkflowInfo2,
)
from apps.landmatrix.views.newviews import _parse_filter
from apps.wagtailcms.models import ChartDescriptionsSettings


def investor_search(request):
    if not request.user.is_authenticated:
        raise NotAuthenticated
    q = request.GET.get("q")
    if not q or len(q) <= 2:
        return JsonResponse({"investors": []})

    fltr = ~Q(status=4)
    # qs = Investor.objects.filter(status__ne=4)
    for term in q.split(" "):
        fltr &= Q(name__icontains=term) | Q(country__name__icontains=term)

    investors = (
        Investor.objects.filter(fltr)
        .order_by("id")
        .values("id", "name", "country__name", "status")
    )
    return JsonResponse({"investors": list(investors)})


def chart_descriptions(request):
    language = request.GET.get("lang", "en")
    with translation.override(language):
        return JsonResponse(
            ChartDescriptionsSettings.load(request_or_site=request).to_dict()
        )


def blog_categories(request):
    language = request.GET.get("lang", "en")
    with translation.override(language):
        return JsonResponse(
            [
                x
                for x in BlogCategory.objects.all().values(
                    "id", "name", "slug", "description"
                )
            ],
            safe=False,
        )


def blog_pages(request):
    language = request.GET.get("lang", "en")
    category = request.GET.get("category")
    qs: QuerySet[BlogPage] = (
        BlogPage.objects.live()
        .prefetch_related("tags")
        .prefetch_related("blog_categories")
    )
    if category:
        qs = qs.filter(blog_categories__slug=category)

    with translation.override(language):
        return JsonResponse(
            [
                x.get_dict("fill-500x500|jpegquality-60")
                for x in qs.order_by("-date", "-id")
            ],
            safe=False,
        )


def legacy_formfields(request):
    language = request.GET.get("lang", "en")
    with translation.override(language):
        return JsonResponse(
            {
                "deal": DealForm().as_json(),
                **get_submodels_fields(),
                "investor": InvestorForm().as_json(),
                "involvement": InvestorVentureInvolvementForm().as_json(),
            }
        )


@require_GET
def get_csrf(request):
    return JsonResponse({"token": get_token(request)})


@require_GET
def country_investments_and_rankings(request):
    country_id = request.GET.get("CID")
    investments = get_deal_top_investments(request)
    return JsonResponse(
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
    deals = DealHull.objects.public().filter(_parse_filter(request))
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
    if not (request.user.is_authenticated and request.user.role):
        raise PermissionDenied("MISSING_AUTHORIZATION")

    data = json.loads(request.body)

    if wfitype == "deal":
        wfi: DealWorkflowInfo2 = DealWorkflowInfo2.objects.get(pk=pk)
    elif wfitype == "investor":
        wfi: InvestorWorkflowInfo2 = InvestorWorkflowInfo2.objects.get(pk=pk)
    else:
        return JsonResponse({"ok": False})

    if not wfi.replies:
        wfi.replies = []
    wfi.replies += [
        {
            "timestamp": timezone.now().isoformat(),
            "user_id": request.user.id,
            "comment": data["comment"],
        }
    ]
    wfi.save()
    return JsonResponse({"ok": True})


def workflow_info_resolve(
    request,
    wfitype: str,
    pk: int,
) -> JsonResponse:
    if not (request.user.is_authenticated and request.user.role):
        raise PermissionDenied("MISSING_AUTHORIZATION")

    if wfitype == "deal":
        wfi: DealWorkflowInfo2 = DealWorkflowInfo2.objects.get(pk=pk)
    elif wfitype == "investor":
        wfi: InvestorWorkflowInfo2 = InvestorWorkflowInfo2.objects.get(pk=pk)
    else:
        return JsonResponse({"ok": False})

    wfi.resolved = True
    wfi.save()
    return JsonResponse({"ok": True})


# def global_rankings(_obj, _info, count=10, filters=None):
#     qs = Deal.objects.active()
#
#     if filters:
#         qs = qs.filter(parse_filters(filters))
#
#     return {
#         "ranking_deal": list(qs.get_deal_country_rankings())[:count],
#         "ranking_investor": list(qs.get_investor_country_rankings())[:count],
#     }
