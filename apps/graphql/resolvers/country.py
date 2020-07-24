from typing import Any

from graphql import GraphQLResolveInfo

from apps.landmatrix.models import Country, Region


def resolve_countries(obj: Any, info: GraphQLResolveInfo, sort="id", limit=20):
    countries = Country.objects.all()  # .filter(deal__status__in=(2, 3))
    # countries = [{"title": r.name, "slug": r.slug} for r in Country.objects.all()]

    # fields = get_fields(info)

    return countries


def resolve_regions(obj: Any, info: GraphQLResolveInfo, sort="id", limit=20):
    return Region.objects.all()
    # regions = (
    #     RegionPage.objects.filter(live=True, region__isnull=False)
    #         .order_by("title")
    #         .values("id", "region_id", "slug", "title")
    # )
    # return [{"id": r["id"], "name": r["title"], "slug": r["slug"]} for r in regions]
