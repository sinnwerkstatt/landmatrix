from typing import Any

from graphql import GraphQLResolveInfo

from apps.graphql.tools import get_fields
from apps.greennewdeal.documents import DealDocument


def resolve_deal(obj: Any, info: GraphQLResolveInfo, id):
    deal = DealDocument.search().filter("term", id=id)

    fields = get_fields(info)
    if fields:
        deal = deal.source(fields)

    deal = deal.execute()[0]
    return deal.to_dict()


def resolve_deals(obj: Any, info: GraphQLResolveInfo, sort="id", limit=20):
    limit = max(1, min(limit, 500))
    deals = DealDocument.search().filter("terms", status=[2, 3]).sort(sort)

    fields = get_fields(info)
    if fields:
        deals = deals.source(fields)
    # if after:
    #     deals = deals.filter('range', id={'gt': after})
    deals = [d.to_dict() for d in deals[:limit].execute()]
    return deals


def resolve_aggregations(obj: Any, info: GraphQLResolveInfo):
    s = DealDocument.search().filter("terms", status=[2, 3])[:0]
    s.aggs.metric("deal_size_sum", "sum", field="deal_size")
    # s.aggs.metric("current_negotiation_status")
    s.aggs.bucket(
        "by_negotiation_status", "terms", field="negotiation_status.value"
    ).metric("deal_size", "sum", field="deal_size.value")

    aggs_dict = s.execute().aggregations.to_dict()
    aggs = {
        "deal_size_sum": aggs_dict["deal_size_sum"]["value"],
        "deal_count": s.count(),
        "by_negotiation_status": aggs_dict["by_negotiation_status"]["buckets"],
    }
    # aggs = {k: v["value"] for k, v in aggs.items()}
    return aggs
