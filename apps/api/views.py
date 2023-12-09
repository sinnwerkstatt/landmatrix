from datetime import datetime, timedelta
from typing import TypedDict

from django.core.handlers.wsgi import WSGIRequest
from django.db.models import F, Prefetch, Q
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseServerError,
    JsonResponse,
)
from django.utils import timezone, translation
from django.utils.timezone import make_aware
from django.views import View
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotAuthenticated

from apps.accounts.models import UserRole
from apps.blog.models import BlogCategory
from apps.graphql.resolvers.charts import create_statistics
from apps.landmatrix.forms.deal import DealForm
from apps.landmatrix.forms.deal_submodels import get_submodels_fields
from apps.landmatrix.forms.investor import InvestorForm, InvestorVentureInvolvementForm
from apps.landmatrix.models.deal import Deal, DealVersion, DealWorkflowInfo
from apps.landmatrix.models.investor import (
    Investor,
    InvestorVersion,
    InvestorWorkflowInfo,
)
from apps.message.models import Message
from apps.wagtailcms.models import ChartDescriptionsSettings
from .utils.to_dict import create_lookups, deal_to_dict, investor_to_dict


@api_view()
def messages_json(request) -> HttpResponse:
    msgs = []
    for msg in Message.objects.filter(is_active=True).exclude(
        expires_at__lte=timezone.localdate()
    ):
        msg: Message
        msgs += [msg.to_dict()]
    return JsonResponse({"messages": msgs})


class Filter(TypedDict):
    staff: bool
    q: Q


class Management(View):
    def __init__(self):
        super().__init__()

    @staticmethod
    def filters(request, is_deal=True) -> dict[str, Filter]:
        # TODO should admins see all?
        # user_groups = list(request.user.groups.values_list("name", flat=True))
        region_or_country = Q()
        if country_id := request.user.country_id:
            region_or_country |= Q(country_id=country_id)
        if region_id := request.user.region_id:
            region_or_country |= Q(country__region_id=region_id)

        return {
            "todo_feedback": {
                "staff": False,
                "q": (
                    Q(
                        workflowinfos__draft_status_before=F(
                            "workflowinfos__draft_status_after"
                        )
                    )
                    | (
                        Q(workflowinfos__draft_status_before=None)
                        & Q(workflowinfos__draft_status_after=None)
                    )
                )
                & Q(workflowinfos__to_user_id=request.user.id)
                & Q(workflowinfos__resolved=False),
            },
            "todo_improvement": {
                "staff": False,
                "q": Q(draft_status=1)
                & Q(workflowinfos__draft_status_before__in=[2, 3])
                & Q(workflowinfos__draft_status_after=1)
                & Q(workflowinfos__to_user_id=request.user.id)
                & Q(workflowinfos__resolved=False),
            },
            "todo_review": {
                "staff": True,
                "q": region_or_country & Q(draft_status=2) & ~Q(current_draft=None),
            },
            "todo_activation": {
                "staff": True,
                "q": region_or_country & Q(draft_status=3) & ~Q(current_draft=None),
            },
            "requested_feedback": {
                "staff": False,
                "q": (
                    Q(
                        workflowinfos__draft_status_before=F(
                            "workflowinfos__draft_status_after"
                        )
                    )
                    | (
                        Q(workflowinfos__draft_status_before=None)
                        & Q(workflowinfos__draft_status_after=None)
                    )
                )
                & Q(workflowinfos__from_user_id=request.user.id)
                & Q(workflowinfos__to_user_id__isnull=False)
                & Q(workflowinfos__resolved=False),
            },
            "requested_improvement": {
                "staff": True,
                "q": ~Q(current_draft=None)
                & (
                    Q(workflowinfos__deal_version_id=F("current_draft_id"))
                    if is_deal
                    else Q(workflowinfos__investor_version_id=F("current_draft_id"))
                )
                & Q(workflowinfos__draft_status_before__in=[2, 3])
                & Q(workflowinfos__draft_status_after=1)
                & Q(workflowinfos__from_user_id=request.user.id),
            },
            "my_drafts": {
                "staff": False,
                "q": Q(current_draft__created_by_id=request.user.id)
                & ~Q(draft_status=None),
            },
            "created_by_me": {
                "staff": False,
                "q": Q(created_by__id=request.user.id),
            },
            "modified_by_me": {
                "staff": False,
                "q": ~Q(created_by__id=request.user.id)
                & Q(versions__created_by_id=request.user.id),
            },
            "reviewed_by_me": {
                "staff": True,
                "q": Q(workflowinfos__draft_status_before=2)
                & Q(workflowinfos__draft_status_after=3)
                & Q(workflowinfos__from_user_id=request.user.id),
            },
            "activated_by_me": {
                "staff": True,
                "q": Q(workflowinfos__draft_status_before=3)
                & Q(workflowinfos__from_user_id=request.user.id),
            },
            "all_items": {
                "staff": True,
                "q": ~Q(status=4),
            },
            "all_drafts": {
                "staff": True,
                "q": ~Q(status=4) & ~Q(current_draft=None),
            },
            "all_deleted": {
                "staff": True,
                "q": Q(status=4),
            },
        }

    def get(self, request, *args, **kwargs) -> HttpResponse:
        if not request.user.is_authenticated:
            return HttpResponseServerError("unauthorized")

        is_deal = not request.GET.get("model") == "investor"
        filters = self.filters(request, is_deal)

        action = request.GET.get("action")
        if action == "counts":
            return JsonResponse(
                {
                    metric: (Deal if is_deal else Investor)
                    .objects.filter(filters[metric]["q"])
                    .distinct()
                    .count()
                    for metric in filters.keys()
                    if request.user.role > UserRole.REPORTER
                    or not filters[metric]["staff"]
                }
            )
        elif action in filters.keys():
            lookups = create_lookups()
            obj_to_dict = deal_to_dict if is_deal else investor_to_dict

            qs = (Deal if is_deal else Investor).objects.prefetch_related(
                Prefetch(
                    "versions",
                    queryset=(DealVersion if is_deal else InvestorVersion)
                    .objects.defer("serialized_data")
                    .order_by("created_at"),
                ),
                Prefetch(
                    "workflowinfos",
                    queryset=(
                        DealWorkflowInfo if is_deal else InvestorWorkflowInfo
                    ).objects.order_by("-timestamp"),
                ),
            )

            ret = [
                obj_to_dict(obj, lookups)
                for obj in qs.filter(filters[action]["q"]).order_by("-id").distinct()
            ]

            return JsonResponse({"objects": ret})
        else:
            return HttpResponseBadRequest("unknown request")


class CaseStatistics(View):
    @staticmethod
    def _counts(request) -> JsonResponse:
        country_id = request.GET.get("country")
        region_id = request.GET.get("region")
        counts = create_statistics(country_id, region_id)
        public_investors = Investor.objects.filter(status__in=[2, 3])
        counts["investors_public_count"] = public_investors.count()
        counts["investors_public_known"] = public_investors.filter(
            is_actually_unknown=False
        ).count()
        return JsonResponse(counts)

    @staticmethod
    def _deals() -> JsonResponse:
        deals = Deal.objects.values(
            "id",
            "deal_size",
            "fully_updated",
            "fully_updated_at",
            "status",
            "draft_status",
            "confidential",
            "country",
            "country__region_id",
            "created_at",
            "modified_at",
            "is_public",
        )
        for d in deals:
            # this is here for CaseStatisticsTable.svelte -> DisplayField
            d["country"] = {"id": d["country"]}

        return JsonResponse({"deals": list(deals)})

    @staticmethod
    def _deal_buckets(
        start: datetime,
        end: datetime,
        region: str | None,
        country: str | None,
    ) -> JsonResponse:
        queries = {
            "added": Q(created_at__gte=start) & Q(created_at__lte=end),
            "updated": Q(modified_at__gte=start) & Q(modified_at__lte=end),
            "fully_updated": Q(fully_updated_at__gte=start)
            & Q(fully_updated_at__lte=end),
            "activated": Q(workflowinfos__draft_status_before=3)
            & Q(workflowinfos__draft_status_after__isnull=True)
            & Q(workflowinfos__timestamp__gte=start)
            & Q(workflowinfos__timestamp__lte=end),
        }

        buckets = {}
        for name in queries.keys():
            if region:
                queries[name] &= Q(country__region_id=region)
            if country:
                queries[name] &= Q(country_id=country)

            buckets[name] = list(
                Deal.objects.filter(queries[name]).values(
                    "id",
                    "deal_size",
                    "status",
                    "draft_status",
                    "country",
                    "created_at",
                    "modified_at",
                    "fully_updated",
                    "fully_updated_at",
                    "confidential",
                )
            )

            for deal in buckets[name]:
                # this is here for CaseStatisticsTable.svelte -> DisplayField
                deal["country"] = {"id": deal["country"]}

        return JsonResponse({"buckets": buckets})

    @staticmethod
    def _investors() -> JsonResponse:
        investors = Investor.objects.values(
            "id",
            "name",
            "country",
            "country__region_id",
            "status",
            "draft_status",
            "created_at",
            "modified_at",
        )
        for inv in investors:
            # this is here for CaseStatisticsTable.svelte -> DisplayField
            inv["country"] = {"id": inv["country"]}

        return JsonResponse({"investors": list(investors)})

    @staticmethod
    def _investor_buckets(
        start: datetime,
        end: datetime,
        region: str | None,
        country: str | None,
    ) -> JsonResponse:
        queries = {
            "added": Q(created_at__gte=start) & Q(created_at__lte=end),
            "updated": Q(modified_at__gte=start) & Q(modified_at__lte=end),
            "activated": Q(workflowinfos__draft_status_before=3)
            & Q(workflowinfos__draft_status_after__isnull=True)
            & Q(workflowinfos__timestamp__gte=start)
            & Q(workflowinfos__timestamp__lte=end),
        }

        buckets = {}
        for name in queries.keys():
            if region:
                queries[name] &= Q(country__region_id=region)
            if country:
                queries[name] &= Q(country_id=country)

            buckets[name] = list(
                Investor.objects.filter(queries[name]).values(
                    "id",
                    "name",
                    "status",
                    "draft_status",
                    "country",
                    "created_at",
                    "modified_at",
                )
            )

            for inv in buckets[name]:
                # this is here for CaseStatisticsTable.svelte -> DisplayField
                inv["country"] = {"id": inv["country"]}

        return JsonResponse({"buckets": buckets})

    def get(self, request: WSGIRequest) -> HttpResponse:
        action = request.GET.get("action")

        if action == "counts":
            return self._counts(request)

        if action == "deals":
            return self._deals()

        if action == "investors":
            return self._investors()

        if action in ["deal_buckets", "investor_buckets"]:
            start = request.GET.get("start")
            end = request.GET.get("end")

            if not (start and end):
                return JsonResponse({})

            dt_start = _parse_date(start)
            # add one day to include end day (important when end = current)
            dt_end = _parse_date(end) + timedelta(1)

            region = request.GET.get("region")
            country = request.GET.get("country")

            if action == "deal_buckets":
                return self._deal_buckets(dt_start, dt_end, region, country)
            return self._investor_buckets(dt_start, dt_end, region, country)

        return HttpResponseBadRequest(f"Unknown action: {action}")


def _parse_date(date_str: str) -> datetime:
    return make_aware(datetime.strptime(date_str, "%Y-%m-%d"))


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
