from typing import Any

from django.db.models import Count, Q
from graphql import GraphQLResolveInfo

from apps.landmatrix.models import Country, Region, Mineral, Animal, Crop, Deal


def resolve_countries(obj: Any, info: GraphQLResolveInfo):
    countries = Country.objects.all()  # .filter(deal__status__in=(2, 3))
    # countries = [{"title": r.name, "slug": r.slug} for r in Country.objects.all()]

    # fields = get_fields(info)

    return countries


def resolve_regions(obj: Any, info: GraphQLResolveInfo):
    return Region.objects.all()
    # regions = (
    #     RegionPage.objects.filter(live=True, region__isnull=False)
    #         .order_by("title")
    #         .values("id", "region_id", "slug", "title")
    # )
    # return [{"id": r["id"], "name": r["title"], "slug": r["slug"]} for r in regions]


def resolve_minerals(obj: Any, info: GraphQLResolveInfo):
    return Mineral.objects.all()


def resolve_animals(obj: Any, info: GraphQLResolveInfo):
    return Animal.objects.all()


def resolve_crops(obj: Any, info: GraphQLResolveInfo):
    return Crop.objects.all()


def resolve_statistics(obj, info: GraphQLResolveInfo, country_id=None, region_id=None):
    public_deals = Deal.objects.public().filter(status__in=(2, 3))
    if country_id:
        public_deals = public_deals.filter(country_id=country_id)
    if region_id:
        public_deals = public_deals.filter(country__fk_region_id=region_id)

    q_has_at_least_one_polygon = Q(locations__areas__isnull=False)

    return {
        "deals_public_count": public_deals.count(),
        "deals_public_multi_ds_count": public_deals.annotate(
            ds_count=Count("datasources")
        )
        .filter(ds_count__gte=2)
        .count(),
        "deals_public_high_geo_accuracy": public_deals.filter(
            Q(locations__level_of_accuracy__in=["EXACT_LOCATION", "COORDINATES"])
            | q_has_at_least_one_polygon
        ).count(),
        "deals_public_polygons": public_deals.filter(
            q_has_at_least_one_polygon
        ).count(),
    }
