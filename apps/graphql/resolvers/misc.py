from typing import Any

from django.db.models import Count, Q
from graphql import GraphQLResolveInfo

from apps.landmatrix.models import Country, Region, Mineral, Animal, Crop, Deal
from apps.wagtailcms.models import ChartDescriptionsSettings


def resolve_countries(obj: Any, info: GraphQLResolveInfo):
    countries = [
        {
            "id": c.id,
            "name": c.name,
            "slug": c.slug,
            "point_lat": c.point_lat,
            "point_lon": c.point_lon,
            "country_page_id": c.country_page_id,
            "observatory_page_id": c.observatory_page_id,
            "short_description": c.short_description,
            "deals": c.deal_set.all(),
        }
        for c in Country.objects.all().prefetch_related("deal_set")
    ]
    return countries


def resolve_regions(obj: Any, info: GraphQLResolveInfo):
    return Region.objects.all()


def resolve_minerals(obj: Any, info: GraphQLResolveInfo):
    return Mineral.objects.all()


def resolve_animals(obj: Any, info: GraphQLResolveInfo):
    return Animal.objects.all()


def resolve_crops(obj: Any, info: GraphQLResolveInfo):
    return Crop.objects.all()


def resolve_statistics(obj, info: GraphQLResolveInfo, country_id=None, region_id=None):
    public_deals = Deal.objects.public()
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


def resolve_chart_descriptions(obj, info):
    return ChartDescriptionsSettings.for_site(info.context.site).to_dict()
