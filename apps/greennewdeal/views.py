import json

from django.core.serializers import serialize
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from apps.greennewdeal.documents import DealDocument
from apps.greennewdeal.documents.deal import LocationDocument
from apps.greennewdeal.models import Deal


def deal_detail(request, deal_id):
    ctx = {"deal_id": deal_id}
    return render(request, template_name="greennewdeal/deal_detail.html", context=ctx)


def api_deal_detail(request, deal_id):
    deal = list(DealDocument.search().filter("term", id=deal_id))[0]
    return JsonResponse(deal.to_dict())


# def api_deal_detail(request, deal_id):
#     deal = Deal.objects.get(id=deal_id)
#     res = {
#         "id": deal.id,
#         "general_info": {
#             "Land Area": {"intended_size": deal.intended_size},
#             "Intention of investment": {
#                 "intention_of_investment": deal.intention_of_investment,
#                 "intention_of_investment_comment": deal.intention_of_investment_comment,
#             },
#         },
#         "overall_comment": deal.overall_comment,
#     }
#     res["locations"] = []
#     res["geojson"] = json.loads(serialize(
#         "geojson",
#         deal.locations.all(),
#         geometry_field="intended_area",
#         fields=("name",),
#     ))
#     for location in deal.locations.all():
#         res["locations"] += [
#             {
#                 "point": location.point.coords,
#                 "intended_area": location.intended_area.json
#                 if location.intended_area
#                 else None,
#             }
#         ]
#     return JsonResponse(res)


def api_deal_map(request):
    s = LocationDocument.search().source(["id", "point", "deal"]).execute()

    xx = []
    for hit in s:
        if not hit.point:
            continue
        feat = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [hit.point.lon, hit.point.lat],
            },
            "properties": {
                "url": f"/deal/{hit.deal.id}/",
                "intention": ["Agriculture"],
                "implementation": ["In operation (production)"],
                "intended_size": hit.deal.intended_size,
                "contract_size": "263",
                "production_size": None,
                "investor": "37762",
                "identifier": hit.deal.id,
                "level_of_accuracy": hit.level_of_accuracy,
            },
        }
        xx += [feat]
    ret = {"type": "FeatureCollection", "features": xx}
    return JsonResponse(ret)
    # .filter("term", color="red")
