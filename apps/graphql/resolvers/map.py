from graphql import GraphQLResolveInfo

from apps.landmatrix.models import Deal


def resolve_markers(
    obj, info: GraphQLResolveInfo, subset="PUBLIC", region_id=None, country_id=None
):
    return Deal.get_geo_markers(region_id, country_id)
