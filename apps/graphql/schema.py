import pathlib

from ariadne import (
    ObjectType,
    load_schema_from_path,
    make_executable_schema,
)
from ariadne.contrib.django.scalars import datetime_scalar, date_scalar

from apps.graphql.resolvers.country import resolve_countries, resolve_regions
from apps.graphql.resolvers.deal import (
    resolve_deal,
    resolve_deals,
    resolve_aggregations,
    resolve_locations,
    deal_type,
    resolve_dealversions,
)
from apps.graphql.resolvers.investor import (
    resolve_investor,
    resolve_investors,
    investor_type,
    resolve_involvements,
)
from apps.graphql.resolvers.user import (
    resolve_user,
    resolve_login,
    resolve_logout,
    resolve_users,
    user_regional_info_type,
)
from apps.graphql.scalars import geopoint_scalar

schema_folder = pathlib.Path(__file__).parent.joinpath("schema")
type_defs = load_schema_from_path(schema_folder)

query = ObjectType("Query")
query.set_field("me", resolve_user)
query.set_field("user", resolve_user)
query.set_field("users", resolve_users)
query.set_field("deal", resolve_deal)
query.set_field("deals", resolve_deals)
query.set_field("dealversions", resolve_dealversions)
query.set_field("locations", resolve_locations)
query.set_field("investor", resolve_investor)
query.set_field("investors", resolve_investors)
query.set_field("involvements", resolve_involvements)
query.set_field("aggregations", resolve_aggregations)
query.set_field("countries", resolve_countries)
query.set_field("regions", resolve_regions)

mutation = ObjectType("Mutation")
mutation.set_field("login", resolve_login)
mutation.set_field("logout", resolve_logout)

schema = make_executable_schema(
    type_defs,
    [datetime_scalar, date_scalar, geopoint_scalar],
    query,
    mutation,
    deal_type,
    investor_type,
    user_regional_info_type,
)
