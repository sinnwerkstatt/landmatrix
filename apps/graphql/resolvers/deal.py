from typing import Any

from ariadne import ObjectType
from django.db.models import Sum
from graphql import GraphQLResolveInfo
from reversion.models import Version, Revision

from apps.graphql.tools import get_fields, parse_filters
from apps.landmatrix.models import Deal, Location


def _resolve_deals_prefetching(info: GraphQLResolveInfo):
    qs = Deal.objects.visible(info.context.user)

    fields = get_fields(info)
    if "country" in fields:
        qs = qs.prefetch_related("country")
    if "locations" in fields:
        qs = qs.prefetch_related("locations")
    if "contracts" in fields:
        qs = qs.prefetch_related("contracts")
    if "datasources" in fields:
        qs = qs.prefetch_related("datasources")
    return qs


def resolve_deal(obj, info: GraphQLResolveInfo, id, version=None):
    if version:
        return (
            Revision.objects.get(id=version)
            .version_set.get(content_type__model="deal")
            ._object_version.object
        )
    deal = _resolve_deals_prefetching(info)
    return deal.get(id=id)


def resolve_deals(
    obj, info: GraphQLResolveInfo, filters=None, sort="id", limit=20, after=None
):
    qs = _resolve_deals_prefetching(info).order_by(sort)
    if filters:
        qs = qs.filter(**parse_filters(filters))

    if after:
        qs = qs.filter(**{f"{sort}__gt": after})

    # limit = max(1, min(limit, 500))
    if limit != 0:
        qs = qs[:limit]
    return qs


deal_type = ObjectType("Deal")


@deal_type.field("locations")
def get_deal_locations(obj: Deal, info: GraphQLResolveInfo, version=None):
    if version:
        return [
            r._object_version.object
            for r in Revision.objects.get(id=version)
            .version_set.filter(content_type__model="location")
            .order_by("id")
        ]
    return obj.locations.all().order_by("id")


@deal_type.field("datasources")
def get_deal_datasources(obj: Deal, info: GraphQLResolveInfo, version=None):
    if version:
        return [
            r._object_version.object
            for r in Revision.objects.get(id=version)
            .version_set.filter(content_type__model="datasource")
            .order_by("id")
        ]
    return obj.datasources.all().order_by("id")


@deal_type.field("contracts")
def get_deal_contracts(obj: Deal, info: GraphQLResolveInfo, version=None):
    if version:
        return [
            r._object_version.object
            for r in Revision.objects.get(id=version)
            .version_set.filter(content_type__model="contract")
            .order_by("id")
        ]
    return obj.contracts.all().order_by("id")


@deal_type.field("versions")
def get_deal_versions(obj, info: GraphQLResolveInfo):
    versions = Version.objects.get_for_object(obj, model_db=None).select_related(
        "revision"
    )
    return [
        {"id": x.id, "deal": x.field_dict, "revision": x.revision} for x in versions
    ]


def resolve_dealversions(obj, info: GraphQLResolveInfo, filters=None):
    qs = Version.objects.get_for_model(Deal)  # .filter(revision__date_created="")
    # qs = _resolve_deals_prefetching(info).order_by(sort)
    print(qs.count())
    if filters:
        qs = qs.filter(**parse_filters(filters))
    print(qs.count())

    return [{"id": x.id, "deal": x.field_dict, "revision": x.revision} for x in qs]


def resolve_locations(obj, info: GraphQLResolveInfo, filters=None, limit=20):
    qs = Location.objects.visible(info.context.user)

    fields = get_fields(info)
    if "deal" in fields:
        qs = qs.select_related("deal")

    if filters:
        qs = qs.filter(**parse_filters(filters))

    if limit != 0:
        qs = qs[:limit]
    return qs


def resolve_aggregations(obj: Any, info: GraphQLResolveInfo):
    neg = Deal.objects.values("current_negotiation_status").annotate(Sum("deal_size"))
