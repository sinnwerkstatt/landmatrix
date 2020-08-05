from typing import Any

from graphql import GraphQLResolveInfo

from apps.landmatrix.models import Country, Region, Mineral, Animal, Crop


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
