from django.db.models import F, Sum, Count
from graphql import GraphQLResolveInfo

from apps.landmatrix.models import Deal

REGION_COORDINATES = {
    2: [6.06433, 17.082249],
    9: [-22.7359, 140.0188],
    21: [54.526, -105.2551],
    142: [34.0479, 100.6197],
    150: [52.0055, 37.9587],
    419: [-4.442, -61.3269],
}


def resolve_markers(
    obj, info: GraphQLResolveInfo, subset="PUBLIC", region_id=None, country_id=None
):

    deals = Deal.objects.visible(
        user=info.context["request"].user, subset=subset
    ).exclude(country=None)

    if region_id:
        markers = (
            deals.filter(country__fk_region_id=region_id)
            .values("country_id", "country__point_lat", "country__point_lon")
            .annotate(count=Count("pk"))
            # .annotate(size=Sum("deal_size"))
        )
        [
            x.update(
                {"coordinates": [x["country__point_lat"], x["country__point_lon"]]}
            )
            for x in markers
        ]
        return markers

    if country_id:
        all_geojson = list(
            deals.filter(country_id=country_id)
            .exclude(geojson=None)
            .values_list("geojson", flat=True)
        )
        markers = []
        for deal_geojson in all_geojson:
            markers += [
                {"coordinates": list(reversed(feature["geometry"]["coordinates"]))}
                for feature in deal_geojson.get("features", [])
                if feature["geometry"]["type"] == "Point"
            ]
        return markers

    # global
    markers = (
        deals.values(region_id=F("country__fk_region_id")).annotate(count=Count("pk"))
        # .annotate(size=Sum("deal_size"))
    )
    [x.update({"coordinates": REGION_COORDINATES[x["region_id"]]}) for x in markers]
    return markers
