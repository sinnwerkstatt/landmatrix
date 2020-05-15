from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_page

from apps.greennewdeal.models import Country, Deal, Location


@cache_page(5)
def vuebase(request, path=None):
    return render(request, template_name="greennewdeal/vuebase.html")


# this is only used for the old global map
def old_api_deals_json(request):
    locations = [
        loc.to_dict()
        for loc in Location.search()[:10_000]  # FIXME broken
        .filter("terms", deal__status=[2, 3])
        .source(["id", "point", "deal", "level_of_accuracy_display"])
        .sort("deal.id")
        .execute()
    ]
    features = []
    for location in locations:
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
                or "Unknown",
                # FIXME: srsly? not just empty array or null??
                "implementation": [
                    impl.get("value") for impl in deal.get("implementation_status", [])
                ]
                or "Unknown",
                # FIXME: srsly? not just empty array or null??
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


def old_api_country_deals_json(request):
    return JsonResponse({})
    # features = []
    #
    # target_countries = collections.defaultdict(PropertyCounter)
    #
    # for result in result_list:
    #     if result.get("target_country"):
    #         target_countries[str(result["target_country"])].increment(**result)
    #
    features = []
    for country in Country.objects.defer("geom").all():  # .filter(id__in=ids):
        properties = {
            "name": country.name,
            "deals": 100,
            # len(target_countries[str(country.id)].activity_identifiers),
            "url": country.get_absolute_url(),
            "centre_coordinates": [country.point_lon, country.point_lat],
        }
        properties.update(
            {
                "intention": "intention",
                "implementation": "implementation_status",
                "level_of_accuracy": "level_of_accuracy",
            }
        )
        # properties.update(target_countries[str(country.id)].get_properties())
        # properties["intention"] = self.get_intentions(properties.get("intention"))
        features.append(
            {
                "type": "Feature",
                "id": country.code_alpha3,
                # 'geometry': json.loads(country.geom) if country.geom else None,
                "properties": properties,
            }
        )
    ret = {"type": "FeatureCollection", "features": features}
    return JsonResponse(ret)


def old_api_latest_changes(request):
    """
    # FIXME: solve this directly via graphql in the future:
    {
      deals(sort:"-timestamp"){
        id
        timestamp
        target_country {
          name
        }
      }
    }
    """
    default_filters = {"status__in": (2, 3), "confidential": False}
    deals = [
        {
            "action": "add/change",  # TODO: Map an action here
            "deal_id": deal["id"],
            "change_date": deal["timestamp"],
            "target_country": deal["target_country__name"],
        }
        for deal in Deal.objects.all()
        .filter(**default_filters)
        .values("id", "timestamp", "target_country__name", "status")
        .order_by("-timestamp")[:20]
    ]
    return JsonResponse(deals, safe=False)
