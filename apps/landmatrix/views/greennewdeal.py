import io
import json
import warnings
import zipfile

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from apps.landmatrix.models import Deal


# @cache_page(5)
def vuebase(request, *args, **kwargs):
    return render(request, template_name="landmatrix/vuebase.html")


def gis_export(request):
    point_json = []
    area_json = []
    for deal in Deal.objects.public().exclude(geojson=None).prefetch_related("country"):
        for feat in deal.geojson.get("features"):
            props = feat.get("properties", {})
            if deal.country:
                country = deal.country.to_dict()
                region = deal.country.fk_region.to_dict()
            else:
                country = region = None
            props.update({"deal_id": deal.id, "country": country, "region": region})
            if feat["geometry"]["type"] == "Point":
                point_json += [feat]
            else:
                area_json += [feat]

    point_res = {"type": "FeatureCollection", "features": point_json}
    area_res = {"type": "FeatureCollection", "features": area_json}
    request_type = request.GET.get("type")
    if request_type == "points":
        return JsonResponse(point_res)
    elif request_type == "areas":
        return JsonResponse(area_res)

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED, False) as zip_file:
        zip_file.writestr("points.geojson", json.dumps(point_res))
        zip_file.writestr("areas.geojson", json.dumps(area_json))
    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer, content_type="application/zip")
    response["Content-Disposition"] = 'attachment; filename="geojson.zip"'
    return response


# def gis_export(request):
#     jsons = [
#         x.areas["features"] for x in Location.objects.filter(deal__status__in=(2, 3)) if x.areas
#     ]
#     import geopandas
#     import fiona
#
#     fiona.supported_drivers["KML"] = "rw"
#     # pts = [x for x in self.geojson["features"] if x["geometry"]["type"] != "Point"]
#     x = geopandas.GeoDataFrame.from_features(jsons)
#     gisdir = mkdtemp(prefix="gis_export")
#     x.to_file(f"{gisdir}/export.shp")
#     # x.to_file("/tmp/mbla.shp")
#     x.to_file(f"{gisdir}/export.kml", driver="KML")
#     return


# def case_statistics(request):
#     Version.objects.get_for_model(Deal).filter(revision__date_created)


def old_api_latest_changes(request):
    warnings.warn("GND Obsoletion Warning", FutureWarning)
    """
    This can be done like so:
    {
      deals(sort:"-timestamp"){
        id
        timestamp
        country { name }
      }
    }
    """
    deals = [
        {
            "action": "Add" if deal["status"] == 2 else "Change",
            "deal_id": deal["id"],
            "change_date": deal["timestamp"],
            "country": deal["country__name"],
        }
        for deal in Deal.objects.visible()
        .values("id", "timestamp", "country__name", "status")
        .order_by("-timestamp")[:20]
    ]
    return JsonResponse(deals, safe=False)
