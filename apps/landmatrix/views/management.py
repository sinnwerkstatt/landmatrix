from datetime import datetime, timedelta
from typing import TypedDict

from django.core.exceptions import PermissionDenied
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Q, F, Prefetch, Count, Case, When, BooleanField
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.utils.timezone import make_aware
from django.views import View

from apps.accounts.models import UserRole
from apps.api.utils.to_dict import deal_to_dict, investor_to_dict
from apps.landmatrix.models.new import (
    DealHull,
    InvestorHull,
    DealWorkflowInfo2,
    InvestorWorkflowInfo2,
)


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
                    Q(workflowinfos__status_before=F("workflowinfos__status_after"))
                    | Q(
                        workflowinfos__status_before=None,
                        workflowinfos__status_after=None,
                    )
                )
                & Q(workflowinfos__to_user=request.user, workflowinfos__resolved=False),
            },
            # "todo_improvement": {
            #     "staff": False,
            #     "q": Q(draft_status=1)
            #     & Q(workflowinfos__draft_status_before__in=[2, 3])
            #     & Q(workflowinfos__draft_status_after=1)
            #     & Q(workflowinfos__to_user_id=request.user.id)
            #     & Q(workflowinfos__resolved=False),
            # },
            "todo_review": {
                "staff": True,
                "q": region_or_country & Q(draft_version__status="REVIEW"),
            },
            "todo_activation": {
                "staff": True,
                "q": region_or_country & Q(draft_version__status="ACTIVATION"),
            },
            # "requested_feedback": {
            #     "staff": False,
            #     "q": (
            #         Q(
            #             workflowinfos__draft_status_before=F(
            #                 "workflowinfos__draft_status_after"
            #             )
            #         )
            #         | (
            #             Q(workflowinfos__draft_status_before=None)
            #             & Q(workflowinfos__draft_status_after=None)
            #         )
            #     )
            #     & Q(workflowinfos__from_user_id=request.user.id)
            #     & Q(workflowinfos__to_user_id__isnull=False)
            #     & Q(workflowinfos__resolved=False),
            # },
            # "requested_improvement": {
            #     "staff": True,
            #     "q": ~Q(current_draft=None)
            #     & (
            #         Q(workflowinfos__deal_version_id=F("current_draft_id"))
            #         if is_deal
            #         else Q(workflowinfos__investor_version_id=F("current_draft_id"))
            #     )
            #     & Q(workflowinfos__draft_status_before__in=[2, 3])
            #     & Q(workflowinfos__draft_status_after=1)
            #     & Q(workflowinfos__from_user_id=request.user.id),
            # },
            # "my_drafts": {
            #     "staff": False,
            #     "q": Q(draft_version__created_by=request.user),
            # },
            # "created_by_me": {
            #     "staff": False,
            #     "q": Q(first_created_by=request.user),
            # },
            # TODO could be defined differently now
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
            "all_items": {
                "staff": True,
                "q": Q(deleted=False),
            },
            "all_drafts": {
                "staff": True,
                "q": Q(deleted=False) & ~Q(draft_version=None),
            },
            "all_deleted": {
                "staff": True,
                "q": Q(deleted=True),
            },
        }

    def get(self, request, *args, **kwargs) -> HttpResponse:
        if not request.user.is_authenticated and not request.user.role:
            raise PermissionDenied("unauthorized")

        is_deal = request.GET.get("model") != "investor"
        filters = self.filters(request, is_deal)

        action = request.GET.get("action")
        if action == "counts":
            Obj = DealHull if is_deal else InvestorHull
            return JsonResponse(
                {
                    metric: Obj.objects.filter(filters[metric]["q"]).distinct().count()
                    for metric in filters.keys()
                    if request.user.role > UserRole.REPORTER
                    or not filters[metric]["staff"]
                }
            )
        elif action in filters.keys():
            obj_to_dict = deal_to_dict if is_deal else investor_to_dict

            qs = (DealHull if is_deal else InvestorHull).objects.prefetch_related(
                # Prefetch(
                #     "versions",
                #     queryset=(
                #         DealVersion2 if is_deal else InvestorVersion2
                #     ).objects.order_by("created_at"),
                # ),
                Prefetch("active_version"),
                Prefetch("draft_version"),
                Prefetch(
                    "workflowinfos",
                    queryset=(
                        DealWorkflowInfo2 if is_deal else InvestorWorkflowInfo2
                    ).objects.order_by("-timestamp"),
                ),
            )

            ret = [
                obj_to_dict(obj)
                for obj in qs.filter(filters[action]["q"]).order_by("-id").distinct()
            ]
            # ret = list(
            #     qs.filter(filters[action]["q"])
            #     .order_by("-id")
            #     .distinct()
            #     .values(
            #         "id",
            #         "country_id",
            #         "fully_updated_at",
            #         "active_version__deal_size",
            #         "first_created_at",
            #         "first_created_by_id",
            #         "active_version__deal_size",
            #         "active_version__created_at",
            #         "active_version__created_by_id",
            #         "workflowinfos",
            #     )[:100]
            # )

            return JsonResponse({"objects": ret})
        else:
            return HttpResponseBadRequest("unknown request")


class CaseStatistics(View):
    def get(self, request: WSGIRequest) -> HttpResponse:
        action = request.GET.get("action")

        if action == "counts":
            return self._counts(request)

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
    def _create_statistics(country_id=None, region_id=None):
        qs = DealHull.objects.public()

        if country_id:
            qs = qs.filter(country_id=country_id)
        if region_id:
            qs = qs.filter(country__region_id=region_id)

        deals_public_count = qs.count()

        deals_public_multi_ds_count = (
            qs.annotate(num_ds=Count("active_version__datasources"))
            .filter(num_ds__gt=1)
            .count()
        )

        deals_public_high_geo_accuracy = (
            qs.annotate(
                high_accuracy=Case(
                    When(
                        active_version__locations__level_of_accuracy__in=[
                            "EXACT_LOCATION",
                            "COORDINATES",
                        ],
                        then=True,
                    ),
                    default=False,
                    output_field=BooleanField(),
                ),
                num_ds=Count("active_version__locations__areas"),
            )
            .filter(Q(num_ds__gt=0) | Q(high_accuracy=True))
            .count()
        )

        deals_public_polygons = (
            qs.annotate(num_areas=Count("active_version__locations__areas"))
            .filter(num_areas__gt=0)
            .count()
        )

        return {
            "deals_public_count": deals_public_count,
            "deals_public_multi_ds_count": deals_public_multi_ds_count,
            "deals_public_high_geo_accuracy": deals_public_high_geo_accuracy,
            "deals_public_polygons": deals_public_polygons,
        }

    def _counts(self, request) -> JsonResponse:
        country_id = request.GET.get("country")
        region_id = request.GET.get("region")
        counts = self._create_statistics(country_id, region_id)
        public_investors = InvestorHull.objects.active()
        counts["investors_public_count"] = public_investors.count()
        counts["investors_public_known"] = public_investors.filter(
            active_version__name_unknown=False
        ).count()
        return JsonResponse(counts)

    @staticmethod
    def __deals_query():
        return (
            DealHull.objects.with_mode()
            .annotate(
                region_id=F("country__region_id"),
                created_at=F("first_created_at"),
                modified_at=F("active_version__modified_at"),  # TODO sensible value?
            )
            .values(
                "id",
                "mode",
                "active_version_id",
                "draft_version_id",
                "draft_version__status",
                "country_id",
                "region_id",
                "created_at",
                "modified_at",
                # deal specific
                "fully_updated_at",
                "active_version__fully_updated",
                "confidential",
                "active_version__deal_size",
                "active_version__is_public",
            )
        )

    @staticmethod
    def __investors_query():
        return (
            InvestorHull.objects.with_mode()
            .annotate(
                country_id=F("active_version__country_id"),
                region_id=F("active_version__country__region_id"),
                created_at=F("first_created_at"),
                modified_at=F("active_version__modified_at"),  # TODO sensible value?
            )
            .values(
                "id",
                "mode",
                "active_version_id",
                "draft_version_id",
                "draft_version__status",
                "country_id",
                "region_id",
                "created_at",
                "modified_at",
                # investor specific
                "active_version__name",
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
            "updated": Q(
                active_version__modified_at__range=(start, end)
            ),  # TODO is this okay?
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
            "updated": Q(
                active_version__modified_at__range=(start, end)
            ),  # TODO is this okay?
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
