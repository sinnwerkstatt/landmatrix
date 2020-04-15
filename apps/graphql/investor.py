from typing import Any

from graphql import GraphQLResolveInfo

from apps.graphql.tools import get_fields
from apps.greennewdeal.documents import InvestorDocument


def resolve_investor(obj: Any, info: GraphQLResolveInfo, id):
    investor = InvestorDocument.search().filter("term", id=id)

    fields = get_fields(info)
    if fields:
        investor.source(fields)

    investor = investor.execute()[0]
    return investor.to_dict()


def resolve_investors(obj: Any, info: GraphQLResolveInfo, sort="id", limit=20):
    limit = max(1, min(limit, 500))
    investors = InvestorDocument.search().filter("terms", status=[2, 3]).sort(sort)

    fields = get_fields(info)
    if fields:
        investors.source(fields)

    investors = [d.to_dict() for d in investors[:limit].execute()]
    return investors
