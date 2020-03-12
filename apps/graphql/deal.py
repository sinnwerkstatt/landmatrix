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

    return list(deal)[0]


def resolve_deals(obj: Any, info: GraphQLResolveInfo, sort):
    deals = DealDocument.search().filter("terms", status=[2, 3]).sort(sort)

    fields = get_fields(info)
    if fields:
        deals = deals.source(fields)

    return list(deals[:100])
