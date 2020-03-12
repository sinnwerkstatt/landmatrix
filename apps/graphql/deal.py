from typing import Any

from graphql import GraphQLResolveInfo

from apps.greennewdeal.documents import DealDocument


def get_fields(info: GraphQLResolveInfo):
    fields = set()
    for fnode in info.field_nodes:
        fields.update({f.name.value for f in fnode.selection_set.selections})
    return list(fields)


def resolve_deal(obj: Any, info: GraphQLResolveInfo, id):
    deal = DealDocument.search().filter("term", id=id)

    fields = get_fields(info)
    if fields:
        deal = deal.source(fields)

    deal = deal.execute()[0]
    return deal.to_dict()


def resolve_deals(obj: Any, info: GraphQLResolveInfo, sort, limit=None):
    deals = DealDocument.search().filter("terms", status=[2, 3]).sort(sort)

    fields = get_fields(info)
    if fields:
        deals = deals.source(fields)
    deals = [d.to_dict() for d in deals[:20].execute()]
    return deals
