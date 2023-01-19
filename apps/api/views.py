from __future__ import annotations

import csv
import datetime
import io
import json
import pytz
import zipfile

from django.contrib.auth import get_user_model
from django.db.models import Q, F
from django.http import (
    JsonResponse,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseServerError,
)
from django.shortcuts import render
from django.utils import timezone
from django.views import View
from openpyxl.workbook import Workbook

from apps.graphql.resolvers.charts import create_statistics
from apps.graphql.tools import parse_filters
from apps.landmatrix.models.country import Country
from apps.landmatrix.models.deal import Deal, DealVersion
from apps.landmatrix.models.investor import Investor, InvestorVersion
from apps.message.models import Message
from apps.utils import qs_values_to_dict

User = get_user_model()


def vuebase(request, *args, **kwargs):
    # this template file comes from `npm run build` in frontend
    return render(request, template_name="vuebase.html")


def gis_export(request):
    point_res = {"type": "FeatureCollection", "features": []}
    area_res = {"type": "FeatureCollection", "features": []}

    deals = Deal.objects.visible(
        user=request.user, subset=request.GET.get("subset", "PUBLIC")
    ).exclude(geojson=None)

    filters = request.GET.get("filters")
    if filters:
        deals = deals.filter(parse_filters(json.loads(filters)))

    fields = ["id", "country__name", "country__region__name", "geojson"]

    for deal in qs_values_to_dict(deals, fields):
        for feat in deal["geojson"].get("features"):
            props = feat.get("properties", {})
            props["deal_id"] = deal["id"]
            if deal.get("country"):
                props["country"] = deal["country"].get("name")
                props["region"] = deal["country"].get("region", {}).get("name")
            if feat["geometry"]["type"] == "Point":
                point_res["features"] += [feat]
            else:
                area_res["features"] += [feat]

    request_type = request.GET.get("type")
    if request_type == "points":
        response = JsonResponse(point_res)
        response["Content-Disposition"] = 'attachment; filename="locations.geojson"'
        return response
    elif request_type == "areas":
        response = JsonResponse(area_res)
        response["Content-Disposition"] = 'attachment; filename="areas.geojson"'
        return response

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED, False) as zip_file:
        zip_file.writestr("points.geojson", json.dumps(point_res))
        zip_file.writestr("areas.geojson", json.dumps(area_res))
    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer, content_type="application/zip")
    response["Content-Disposition"] = 'attachment; filename="geojson.zip"'
    return response


def messages_json(request):
    msgs = [
        msg.to_dict()
        for msg in Message.objects.filter(is_active=True).exclude(
            expires_at__lte=timezone.localdate()
        )
    ]
    return JsonResponse({"messages": msgs})


class Management(View):
    def __init__(self):
        super().__init__()
        self.users_map = {
            u.id: {"id": u.id, "username": u.username, "full_name": u.full_name}
            for u in User.objects.all()
        }
        self.countries_map = {
            c.id: {
                "id": c.id,
                "name": c.name,
                "region": {"id": c.region_id} if c.region_id else None,
            }
            for c in Country.objects.all()
        }

    @staticmethod
    def filters(request, is_deal=True):
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
            "created_by_me": {"staff": False, "q": Q(created_by__id=request.user.id)},
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
            "all_items": {"staff": True, "q": Q()},
            "all_drafts": {"staff": True, "q": ~Q(current_draft=None)},
            "all_deleted": {"staff": True, "q": Q(status=4)},
        }

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseServerError("unauthorized")

        is_deal = not request.GET.get("model") == "investor"
        Obj = Deal if is_deal else Investor
        filters = self.filters(request, is_deal)

        action = request.GET.get("action")
        if action == "counts":
            return JsonResponse(
                {
                    metric: Obj.objects.filter(filters[metric]["q"]).distinct().count()
                    for metric in filters.keys()
                    if request.user.is_staff or not filters[metric]["staff"]
                }
            )
        elif action in filters.keys():
            ret = [
                self._obj_dict(obj)
                for obj in Obj.objects.filter(filters[action]["q"]).distinct()
            ]
        else:
            return HttpResponseBadRequest("unknown request")

        if rformat := request.GET.get("format"):
            for x in ret:
                # safe get if field is undefined or None
                x["country"] = (x.get("country", {}) or {}).get("name")
                x["created_by"] = (x.get("created_by", {}) or {}).get("username")
                x["modified_by"] = (x.get("modified_by", {}) or {}).get("username")

                del x["workflowinfos"]

                # remove tzinfo from datetime fields and format as string
                for datetime_field in ["created_at", "modified_at", "fully_updated_at"]:
                    if isinstance(x[datetime_field], datetime.datetime):
                        x[datetime_field] = (
                            x[datetime_field]
                            .astimezone(pytz.UTC)
                            .replace(tzinfo=None)
                            .isoformat(timespec="seconds")
                            + "Z"
                        )

            if rformat == "csv":
                response = HttpResponse(self._csv_writer(ret), content_type="text/csv")
                response["Content-Disposition"] = f'attachment; filename="{action}.csv"'
                return response
            if rformat == "xlsx":
                response = HttpResponse(content_type="application/ms-excel")
                response[
                    "Content-Disposition"
                ] = f'attachment; filename="{action}.xlsx"'
                self._xlsx_writer(ret, response)
                return response

        return JsonResponse({"objects": ret})

    def _obj_dict(self, obj: Deal | Investor):
        is_deal = isinstance(obj, Deal)
        obj_dict = {
            "id": obj.id,
            "status": obj.status,
            "draft_status": obj.draft_status,
            "workflowinfos": [
                {
                    "id": w.id,
                    "from_user": self.users_map.get(w.from_user_id),
                    "to_user": self.users_map.get(w.to_user_id),
                    "draft_status_before": w.draft_status_before,
                    "draft_status_after": w.draft_status_after,
                    "obj_version_id": w.deal_version_id
                    if is_deal
                    else w.investor_version_id,
                    "timestamp": w.timestamp,
                    "comment": w.comment,
                    "resolved": w.resolved,
                    "replies": w.replies or [],
                    "__typename": "DealWorkflowInfo"
                    if is_deal
                    else "InvestorWorkflowInfo",
                }
                for w in obj.workflowinfos.order_by("-id")
            ],
        }
        if obj.current_draft and (draft := obj.current_draft.serialized_data):
            obj_dict.update(
                {
                    "current_draft_id": obj.current_draft_id,
                    "country": self.countries_map[draft["country"]]
                    if draft["country"]
                    else None,
                    # TODO: @version_overhaul hacky solution to fix modified fields
                    # creation time
                    "created_at": obj.created_at,
                    # creator
                    "created_by": self.users_map.get(obj.created_by_id),
                    # last modification time of latest version
                    "modified_at": obj.current_draft.modified_at,
                    # creator or latest version
                    "modified_by": self.users_map.get(obj.current_draft.created_by_id),
                }
            )
            if is_deal:
                obj_dict["deal_size"] = draft.get("deal_size")
                obj_dict["fully_updated_at"] = draft["fully_updated_at"]
            else:
                obj_dict["name"] = draft.get("name")

        else:
            newest_version = obj.versions.first()
            obj_dict.update(
                {
                    "country": self.countries_map[obj.country_id]
                    if obj.country_id
                    else None,
                    # TODO: @version_overhaul hacky solution to fix modified fields
                    "created_at": obj.created_at,
                    "created_by": self.users_map.get(obj.created_by_id),
                    "modified_at": newest_version.modified_at,
                    "modified_by": self.users_map.get(newest_version.created_by_id),
                }
            )
            if is_deal:
                obj_dict["deal_size"] = int(obj.deal_size)
                obj_dict["fully_updated_at"] = obj.fully_updated_at
            else:
                obj_dict["name"] = obj.name

        if not is_deal:
            # TODO not performant
            obj_dict["deals"] = list(
                Deal.objects.filter(operating_company_id=obj.id)
                .order_by("id")
                .values_list("id", "country__region_id")
            )
        return obj_dict

    @staticmethod
    def _csv_writer(data):
        file = io.StringIO()
        writer = csv.writer(file, delimiter=";")  # encoding='cp1252'
        writer.writerow(data[0].keys())
        [writer.writerow(item.values()) for item in data]
        file.seek(0)
        return file.getvalue()

    @staticmethod
    def _xlsx_writer(data, response: HttpResponse):
        wb = Workbook(write_only=True)
        ws = wb.create_sheet(title="Management")
        ws.append(list(data[0].keys()))
        [ws.append(list(item.values())) for item in data]
        wb.save(response)


class CaseStatistics(View):
    @staticmethod
    def _counts(request):
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
    def _deals():
        deals = Deal.objects.values(
            "id",
            "deal_size",
            "fully_updated",
            "fully_updated_at",
            "status",
            "draft_status",
            "confidential",
            "country_id",
            "country__region_id",
            "created_at",
            "modified_at",
            "is_public",
        )
        for d in deals:
            # this is here for CaseStatisticsTable.svelte -> DisplayField
            d["country"] = {"id": d["country_id"]}
        return JsonResponse({"deals": list(deals)})

    @staticmethod
    def _deal_versions(start: str, end: str, region: int = None, country: int = None):
        versions = DealVersion.objects.filter(
            created_at__gte=start, created_at__lte=end
        )
        if region:
            versions = versions.filter(deal__country__region_id=region)
        elif country:
            versions = versions.filter(deal__country_id=country)
        deals = Deal.objects.filter(id__in=versions.values_list("object_id")).values(
            "id",
            "deal_size",
            "status",
            "draft_status",
            "country_id",
            "created_at",
            "modified_at",
            "fully_updated",
            "fully_updated_at",
            "confidential",
        )

        for d in deals:
            # this is here for CaseStatisticsTable.svelte -> DisplayField
            d["country"] = {"id": d["country_id"]}
        return JsonResponse({"deals": list(deals)})

    @staticmethod
    def _investors():
        investors = Investor.objects.values(
            "id",
            "name",
            "country_id",
            "country__region_id",
            "status",
            "draft_status",
            "created_at",
            "modified_at",
        )
        for inv in investors:
            # this is here for CaseStatisticsTable.svelte -> DisplayField
            inv["country"] = {"id": inv["country_id"]}
        return JsonResponse({"investors": list(investors)})

    @staticmethod
    def _investor_versions(
        start: str, end: str, region: int = None, country: int = None
    ):
        versions = InvestorVersion.objects.filter(
            created_at__gte=start, created_at__lte=end
        )
        if region:
            versions = versions.filter(deal__country__region_id=region)
        elif country:
            versions = versions.filter(deal__country_id=country)
        investors = Investor.objects.filter(
            id__in=versions.values_list("object_id")
        ).values(
            "id",
            "name",
            "status",
            "draft_status",
            "country_id",
            "created_at",
            "modified_at",
        )

        for d in investors:
            # this is here for CaseStatisticsTable.svelte -> DisplayField
            d["country"] = {"id": d["country_id"]}
        return JsonResponse({"investors": list(investors)})

    def get(self, request, *args, **kwargs):
        # is_deal = not request.GET.get("model") == "investor"
        # Obj = Deal if is_deal else Investor
        # filters = self.filters(request, is_deal)
        action = request.GET.get("action")

        if action == "counts":
            return self._counts(request)

        if action == "deals":
            return self._deals()

        if action == "investors":
            return self._investors()

        if action in ["deal_versions", "investor_versions"]:
            start = request.GET.get("start")
            end = request.GET.get("end")
            region = request.GET.get("region")
            country = request.GET.get("country")
            if not (start and end):
                return JsonResponse({})
            if action == "deal_versions":
                return self._deal_versions(start, end, region, country)
            return self._investor_versions(start, end, region, country)
