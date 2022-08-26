import csv
import io
import json
import zipfile

from django.contrib.auth import get_user_model
from django.db.models import Q, F
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.utils import timezone
from django.views import View
from openpyxl.workbook import Workbook

from apps.graphql.tools import parse_filters
from apps.landmatrix.models.country import Country
from apps.landmatrix.models.deal import Deal
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
    def filters(request):
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
                & Q(workflowinfos__to_user_id=request.user.id),
            },
            "todo_improvement": {
                "staff": False,
                "q": Q(workflowinfos__draft_status_before__in=[2, 3])
                & Q(workflowinfos__draft_status_after=1)
                & Q(workflowinfos__to_user_id=request.user.id)
                & Q(workflowinfos__processed_by_receiver=False),
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
                & Q(workflowinfos__from_user_id=request.user.id),
            },
            "requested_improvement": {
                "staff": True,
                "q": ~Q(current_draft=None)
                & Q(workflowinfos__deal_version_id=F("current_draft_id"))
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
        filters = self.filters(request)

        action = request.GET.get("action")
        if action == "counts":
            return JsonResponse(
                {
                    metric: Deal.objects.filter(filters[metric]["q"]).count()
                    for metric in filters.keys()
                    if request.user.is_staff or not filters[metric]["staff"]
                }
            )
        elif action in filters.keys():
            ret = [
                self._deal_dict(deal)
                for deal in Deal.objects.filter(filters[action]["q"]).distinct()
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

        return JsonResponse({"deals": ret})

    def _deal_dict(self, deal: Deal):
        deal_dict = {
            "id": deal.id,
            "status": deal.status,
            "draft_status": deal.draft_status,
            "workflowinfos": [
                {
                    "id": w.id,
                    "from_user": self.users_map.get(w.from_user_id),
                    "to_user": self.users_map.get(w.to_user_id),
                    "draft_status_before": w.draft_status_before,
                    "draft_status_after": w.draft_status_after,
                    "deal_version_id": w.deal_version_id,
                    "timestamp": w.timestamp,
                    "comment": w.comment,
                    "processed_by_receiver": w.processed_by_receiver,
                }
                for w in deal.workflowinfos.order_by("-id")
            ],
        }
        if deal.current_draft and (draft := deal.current_draft.serialized_data):
            deal_dict.update(
                {
                    "draft_id": deal.current_draft.id,
                    "country": self.countries_map[draft["country"]]
                    if draft["country"]
                    else None,
                    "deal_size": draft["deal_size"],
                    "created_at": draft["created_at"],
                    "created_by": self.users_map.get(draft["created_by"]),
                    "modified_at": draft["modified_at"],
                    "modified_by": self.users_map.get(draft["modified_by"]),
                    "fully_updated_at": draft["fully_updated_at"],
                }
            )
        else:
            deal_dict.update(
                {
                    "country": self.countries_map[deal.country_id]
                    if deal.country_id
                    else None,
                    "deal_size": int(deal.deal_size),
                    "created_at": deal.created_at,
                    "created_by": self.users_map.get(deal.created_by_id),
                    "modified_at": deal.modified_at,
                    "modified_by": self.users_map.get(deal.modified_by_id),
                    "fully_updated_at": deal.fully_updated_at,
                }
            )
        return deal_dict

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
        ws = wb.create_sheet(title="Deals")
        ws.append(list(data[0].keys()))
        [ws.append(list(item.values())) for item in data]
        wb.save(response)
