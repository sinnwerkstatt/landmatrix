from __future__ import annotations

import csv
import io
import json
import zipfile

from django.contrib.auth import get_user_model
from django.db import connection
from django.db.models import Q, F
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.utils import timezone
from django.views import View
from openpyxl.workbook import Workbook

from apps.graphql.tools import parse_filters
from apps.landmatrix.models.country import Country
from apps.landmatrix.models.deal import Deal
from apps.landmatrix.models.investor import Investor
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
            u.id: {"id": u.id, "username": u.username} for u in User.objects.all()
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
        if hasattr(request.user, "userregionalinfo"):
            if country := request.user.userregionalinfo.country:
                region_or_country |= Q(country=country)
            if region := request.user.userregionalinfo.region:
                region_or_country |= Q(country__region=region)

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
                & Q(workflowinfos__to_user_id__isnull=False),
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
                "q": Q(current_draft__created_by_id=request.user.id),
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
                x["country"] = x.get("country", {}).get("name")
                x["created_by"] = x.get("created_by", {}).get("username")
                x["modified_by"] = x.get("modified_by", {}).get("username")
                del x["workflowinfos"]
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
                    "created_at": draft["created_at"],
                    "created_by": self.users_map.get(draft["created_by"]),
                    "modified_at": draft["modified_at"],
                    "modified_by": self.users_map.get(draft["modified_by"]),
                }
            )
            if is_deal:
                obj_dict["deal_size"] = draft.get("deal_size")
                obj_dict["fully_updated_at"] = draft["fully_updated_at"]
            else:
                obj_dict["name"] = draft.get("name")

        else:
            obj_dict.update(
                {
                    "country": self.countries_map[obj.country_id]
                    if obj.country_id
                    else None,
                    "created_at": obj.created_at,
                    "created_by": self.users_map.get(obj.created_by_id),
                    "modified_at": obj.modified_at,
                    "modified_by": self.users_map.get(obj.modified_by_id),
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

        from_clause = "FROM landmatrix_deal d"
        where_clause = "WHERE status IN (2,3) AND is_public=True"

        if country_id:
            where_clause += f" AND country_id={country_id}"
        elif region_id:
            from_clause = "FROM landmatrix_deal d INNER JOIN landmatrix_country c ON (d.country_id = c.id)"
            where_clause += f" AND c.region_id={region_id}"

        cursor = connection.cursor()

        cursor.execute(f"SELECT count(*) {from_clause} {where_clause}")
        deals_public_count = cursor.fetchone()[0]

        cursor.execute(
            f"SELECT count(d.id) {from_clause} {where_clause} AND jsonb_array_length(d.datasources) > 1"
        )
        deals_public_multi_ds_count = cursor.fetchone()[0]

        cursor.execute(
            f"SELECT count(d.id) {from_clause}, jsonb_array_elements(d.locations) l {where_clause}"
            f" AND l->>'level_of_accuracy' in ('EXACT_LOCATION','COORDINATES') AND l->>'areas' IS NOT NULL"
        )
        deals_public_high_geo_accuracy = cursor.fetchone()[0]

        cursor.execute(
            f"SELECT count(d.id) {from_clause}, jsonb_array_elements(d.locations) l {where_clause}"
            f" AND l->>'areas' IS NOT NULL"
        )
        deals_public_polygons = cursor.fetchone()[0]

        return JsonResponse(
            {
                "deals_public_count": deals_public_count,
                "deals_public_multi_ds_count": deals_public_multi_ds_count,
                "deals_public_high_geo_accuracy": deals_public_high_geo_accuracy,
                "deals_public_polygons": deals_public_polygons,
            }
        )

    def get(self, request, *args, **kwargs):
        # is_deal = not request.GET.get("model") == "investor"
        # Obj = Deal if is_deal else Investor
        # filters = self.filters(request, is_deal)
        action = request.GET.get("action")

        if action == "counts":
            return self._counts(request)
