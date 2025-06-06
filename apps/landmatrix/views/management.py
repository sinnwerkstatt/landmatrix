from datetime import datetime, timedelta
from typing import TypedDict

from django.contrib.postgres.expressions import ArraySubquery
from django.core.exceptions import PermissionDenied
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Case, F, OuterRef, Q, QuerySet, When
from django.db.models.functions import JSONObject
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.utils.timezone import make_aware
from django.views import View

from apps.accounts.models import User
from apps.landmatrix.models.abstract import VersionStatus
from apps.landmatrix.models.deal import DealHull, DealWorkflowInfo
from apps.landmatrix.models.investor import InvestorHull, InvestorWorkflowInfo
from apps.landmatrix.permissions import (
    is_admin,
    is_editor_or_higher,
    is_reporter_or_higher,
)


class Filter(TypedDict):
    staff: bool
    q: Q


# TODO: Add openAPI schema
class Management(View):
    # def __init__(self):
    #     super().__init__()

    @staticmethod
    def filters(request, is_deal=True) -> dict[str, Filter]:
        # TODO Later should admins see all?
        region_or_country = Q()
        if country_id := request.user.country_id:
            region_or_country |= (
                Q(country_id=country_id) if is_deal else Q()  # See: Issue #833
                # else Q(active_version__country_id=country_id)
            )
        if region_id := request.user.region_id:
            region_or_country |= (
                Q(country__region_id=region_id) if is_deal else Q()  # See: Issue #833
                # else Q(active_version__country__region_id=region_id)
            )

        return {
            "todo_feedback": {
                "staff": False,
                "q": (
                    Q(workflowinfos__status_before=F("workflowinfos__status_after"))
                    | Q(
                        workflowinfos__status_before=None,
                        workflowinfos__status_after=None,
                    )
                )
                & Q(workflowinfos__to_user=request.user, workflowinfos__resolved=False),
            },
            "todo_improvement": {
                "staff": False,
                "q": Q(draft_version__isnull=False)
                & Q(
                    workflowinfos__status_before__in=[
                        VersionStatus.REVIEW,
                        VersionStatus.ACTIVATION,
                    ]
                )
                & Q(workflowinfos__status_after=VersionStatus.DRAFT)
                & Q(workflowinfos__to_user_id=request.user.id)
                & Q(workflowinfos__resolved=False),
            },
            "todo_review": {
                "staff": True,
                "q": region_or_country & Q(draft_version__status=VersionStatus.REVIEW),
            },
            "todo_activation": {
                "staff": True,
                "q": region_or_country
                & Q(draft_version__status=VersionStatus.ACTIVATION),
            },
            "requested_feedback": {
                "staff": False,
                "q": (
                    Q(workflowinfos__status_before=F("workflowinfos__status_after"))
                    | (
                        Q(workflowinfos__status_before=None)
                        & Q(workflowinfos__status_after=None)
                    )
                )
                & Q(workflowinfos__from_user=request.user)
                & Q(workflowinfos__to_user__isnull=False)
                & Q(workflowinfos__resolved=False),
            },
            "requested_improvement": {
                "staff": True,
                "q": Q(draft_version__isnull=False)
                & (
                    Q(workflowinfos__deal_version_id=F("draft_version_id"))
                    if is_deal
                    else Q(workflowinfos__investor_version_id=F("draft_version_id"))
                )
                & Q(
                    workflowinfos__status_before__in=[
                        VersionStatus.REVIEW,
                        VersionStatus.ACTIVATION,
                    ]
                )
                & Q(workflowinfos__status_after=VersionStatus.DRAFT)
                & Q(workflowinfos__from_user=request.user),
            },
            "my_drafts": {
                "staff": False,
                "q": Q(
                    draft_version__created_by=request.user,
                    draft_version__status=VersionStatus.DRAFT,
                ),
            },
            "created_by_me": {
                "staff": False,
                "q": Q(first_created_by=request.user),
            },
            "modified_by_me": {
                "staff": False,
                "q": ~Q(first_created_by=request.user)
                & Q(versions__created_by=request.user),
            },
            "reviewed_by_me": {
                "staff": True,
                "q": Q(versions__sent_to_activation_by=request.user),
            },
            "activated_by_me": {
                "staff": True,
                "q": Q(versions__activated_by=request.user),
            },
            "all_active": {
                "staff": True,
                "q": Q(active_version__isnull=False),
            },
            "all_drafts": {
                "staff": True,
                "q": Q(draft_version__isnull=False),
            },
            "all_deleted": {"staff": True, "q": Q(deleted=True)},
        }

    def get(self, request, *args, **kwargs) -> HttpResponse:
        user: User = request.user

        if not is_reporter_or_higher(user):
            raise PermissionDenied("MISSING_AUTHORIZATION")

        is_deal = request.GET.get("model") != "investor"
        filters = self.filters(request, is_deal)
        # noinspection PyPep8Naming
        Obj = DealHull if is_deal else InvestorHull

        action = request.GET.get("action")
        if action == "counts":
            return JsonResponse(
                {
                    metric_name: Obj.objects.normal()
                    .filter(mtrx["q"])
                    .order_by("-id")
                    .distinct()
                    .count()
                    for metric_name, mtrx in filters.items()
                    if is_editor_or_higher(user) or not mtrx["staff"]
                }
            )
        elif action in filters.keys():
            if action == "all_deleted":
                # WATCH OUT, DELETED DEALS!
                if not is_admin(user):
                    raise PermissionDenied("MISSING_AUTHORIZATION")
                qs = Obj.objects.filter(deleted=True)
            else:
                qs = Obj.objects.normal()

            qs = qs.filter(filters[action]["q"]).order_by("-id").distinct()
            if is_deal:
                qs: QuerySet[DealHull]
                wflos = ArraySubquery(
                    DealWorkflowInfo.objects.filter(deal_id=OuterRef("id"))
                    .order_by("-id")
                    .values(
                        json=JSONObject(
                            id="id",
                            from_user_id="from_user_id",
                            to_user_id="to_user_id",
                            status_before="status_before",
                            status_after="status_after",
                            timestamp="timestamp",
                            comment="comment",
                            resolved="resolved",
                            replies="replies",
                        )
                    )
                )
                ret = (
                    qs.annotate(
                        # we're turning the default "first active, then draft" around
                        # because in the management interface the draft is more relevant
                        selected_version=Case(
                            When(
                                draft_version_id__isnull=False,
                                then=JSONObject(
                                    id="draft_version_id",
                                    modified_at="draft_version__modified_at",
                                    modified_by_id="draft_version__modified_by_id",
                                    deal_size="draft_version__deal_size",
                                    fully_updated="draft_version__fully_updated",
                                    current_intention_of_investment="draft_version__current_intention_of_investment",
                                ),
                            ),
                            default=JSONObject(
                                id="active_version_id",
                                modified_at="active_version__modified_at",
                                modified_by_id="active_version__modified_by_id",
                                deal_size="active_version__deal_size",
                                fully_updated="active_version__fully_updated",
                                current_intention_of_investment="active_version__current_intention_of_investment",
                            ),
                        ),
                    )
                    .values(
                        "id",
                        "active_version_id",
                        "draft_version_id",
                        "deleted",
                        "first_created_at",
                        "first_created_by_id",
                        "selected_version",
                        "country_id",
                        "fully_updated_at",
                    )
                    .annotate(workflowinfos=wflos, status=F("draft_version__status"))
                )
            else:
                qs: QuerySet[InvestorHull]
                wflos = ArraySubquery(
                    InvestorWorkflowInfo.objects.filter(investor_id=OuterRef("id"))
                    .order_by("-id")
                    .values(
                        json=JSONObject(
                            id="id",
                            from_user_id="from_user_id",
                            to_user_id="to_user_id",
                            status_before="status_before",
                            status_after="status_after",
                            timestamp="timestamp",
                            comment="comment",
                            resolved="resolved",
                            replies="replies",
                        )
                    )
                )
                ret = (
                    qs.annotate(
                        # we're turning the default "first active, then draft" around
                        # because in the management interface the draft is more relevant
                        selected_version=Case(
                            When(
                                draft_version_id__isnull=False,
                                then=JSONObject(
                                    id="draft_version_id",
                                    modified_at="draft_version__modified_at",
                                    modified_by_id="draft_version__modified_by_id",
                                    name="draft_version__name",
                                    name_unknown="draft_version__name_unknown",
                                    country_id="draft_version__country_id",
                                ),
                            ),
                            default=JSONObject(
                                id="active_version_id",
                                modified_at="active_version__modified_at",
                                modified_by_id="active_version__modified_by_id",
                                name="active_version__name",
                                name_unknown="active_version__name_unknown",
                                country_id="active_version__country_id",
                            ),
                        )
                    )
                    .values(
                        "id",
                        "active_version_id",
                        "draft_version_id",
                        "deleted",
                        "first_created_at",
                        "first_created_by_id",
                        "selected_version",
                    )
                    .annotate(workflowinfos=wflos, status=F("draft_version__status"))
                )

            return JsonResponse({"objects": list(ret)})

        return HttpResponseBadRequest("unknown request")


class CaseStatistics(View):
    def get(self, request: WSGIRequest) -> HttpResponse:
        action = request.GET.get("action")

        if action == "deals":
            return JsonResponse({"deals": list(self.__deals_query())})

        if action == "investors":
            return JsonResponse({"investors": list(self.__investors_query())})

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

    @staticmethod
    def __deals_query():
        return (
            DealHull.objects.normal()
            .annotate(
                region_id=F("country__region_id"),
                created_at=F("first_created_at"),
                modified_at=F("active_version__modified_at"),
                deal_size=F("active_version__deal_size"),
                status=F("draft_version__status"),
            )
            .values(
                "id",
                "active_version_id",
                "draft_version_id",
                "draft_version__status",
                "status",
                "country_id",
                "region_id",
                "created_at",
                "modified_at",
                # deal specific
                "fully_updated_at",
                "active_version__fully_updated",
                "confidential",
                "deal_size",
                "active_version__is_public",
            )
        )

    @staticmethod
    def __investors_query():
        return (
            InvestorHull.objects.normal()
            .annotate(
                country_id=F("active_version__country_id"),
                region_id=F("active_version__country__region_id"),
                created_at=F("first_created_at"),
                modified_at=F("active_version__modified_at"),
                name=F("active_version__name"),
                status=F("draft_version__status"),
            )
            .values(
                "id",
                "active_version_id",
                "draft_version_id",
                "draft_version__status",
                "status",
                "country_id",
                "region_id",
                "created_at",
                "modified_at",
                # investor specific
                "name",
            )
        )

    def _deal_buckets(
        self,
        start: datetime,
        end: datetime,
        region: str | None,
        country: str | None,
    ) -> JsonResponse:
        queries = {
            "added": Q(first_created_at__range=(start, end)),
            "added_and_activated": Q(
                first_created_at__range=(start, end),
                active_version__isnull=False,
            ),
            "updated": Q(active_version__modified_at__range=(start, end)),
            "fully_updated": Q(fully_updated_at__range=(start, end)),
            "activated": Q(active_version__activated_at__range=(start, end)),
        }

        buckets = {}
        for name, query in queries.items():
            if region:
                query &= Q(country__region_id=region)
            if country:
                query &= Q(country_id=country)

            buckets[name] = list(self.__deals_query().filter(query))

        return JsonResponse({"buckets": buckets})

    def _investor_buckets(
        self,
        start: datetime,
        end: datetime,
        region: str | None,
        country: str | None,
    ) -> JsonResponse:
        queries = {
            "added": Q(first_created_at__range=(start, end)),
            "added_and_activated": Q(
                first_created_at__range=(start, end),
                active_version__isnull=False,
            ),
            "updated": Q(active_version__modified_at__range=(start, end)),
            "activated": Q(active_version__activated_at__range=(start, end)),
        }

        buckets = {}
        for name, query in queries.items():
            if region:
                query &= Q(active_version__country__region_id=region)
            if country:
                query &= Q(active_version__country_id=country)

            buckets[name] = list(self.__investors_query().filter(query))

        return JsonResponse({"buckets": buckets})


def _parse_date(date_str: str) -> datetime:
    return make_aware(datetime.strptime(date_str, "%Y-%m-%d"))
