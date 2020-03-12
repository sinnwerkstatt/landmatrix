from django.http import JsonResponse
from django.shortcuts import render

from apps.greennewdeal.documents import DealDocument
from apps.greennewdeal.documents.deal import LocationDocument


def vuedeal(request, path=None):
    return render(request, template_name="greennewdeal/vuedeal.html", context={})


def api_deal_list(request):
    fields = [
        "id",
        "target_country",
        "top_investors",
        "intention_of_investment",
        "negotiation_status",
        "implementation_status",
        "deal_size",
        "geojson",
    ]
    deals = [
        d.to_dict()
        for d in DealDocument.search()
        .filter("terms", status=[2, 3])
        .sort("id")
        .source(fields)[:3]
    ]
    return JsonResponse({"deals": deals})


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
