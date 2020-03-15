from django.http import JsonResponse
from django.shortcuts import render

from apps.greennewdeal.documents import DealDocument
from apps.greennewdeal.documents.deal import LocationDocument


def vuedeal(request, path=None):
    return render(request, template_name="greennewdeal/vuedeal.html", context={})


def get_value_from_datevaluedict(obj):
    if obj:
        return obj[0]["value"]
    return None


# @cache_page(5)
def api_deal_map(request):
    s = [
        loc.to_dict()
        for loc in LocationDocument.search()[:5000]
        .filter("terms", deal__status=[2, 3])
        .source(["id", "point", "deal", "level_of_accuracy_display"])
        .sort("deal.id")
        .execute()
    ]
    features = []
    for location in s:
        if not location.get("point"):
            continue
        deal = location["deal"]
        feat = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [location["point"]["lon"], location["point"]["lat"]],
            },
            "properties": {
                "url": f"/deal/{deal['id']}/",
                "intention": [
                    intention.get("value")
                    for intention in deal.get("intention_of_investment", [])
                ]
                or "Unknown",  # FIXME: srsly? not just empty array or null??
                "implementation": [
                    impl.get("value") for impl in deal.get("implementation_status", [])
                ]
                or "Unknown",  # FIXME: srsly? not just empty array or null??
                "intended_size": deal.get("intended_size"),
                "contract_size": deal.get("contract_size", [{}])[0].get("value"),
                "production_size": deal.get("production_size", [{}])[0].get("value"),
                "investor": deal.get("operating_company", {}).get("id"),
                "identifier": deal["id"],
                "level_of_accuracy": location.get("level_of_accuracy_display"),
            },
        }
        features += [feat]
    ret = {"type": "FeatureCollection", "features": features}
    return JsonResponse(ret)
