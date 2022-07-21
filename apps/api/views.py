import io
import json
import zipfile

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.utils import timezone

from apps.graphql.tools import parse_filters
from apps.landmatrix.models.deal import Deal
from apps.message.models import Message
from apps.utils import qs_values_to_dict


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

    fields = ["id", "country__name", "country__fk_region__name", "geojson"]

    for deal in qs_values_to_dict(deals, fields):
        for feat in deal["geojson"].get("features"):
            props = feat.get("properties", {})
            props["deal_id"] = deal["id"]
            if deal.get("country"):
                props["country"] = deal["country"].get("name")
                props["region"] = deal["country"].get("fk_region", {}).get("name")
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
