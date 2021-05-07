import pathlib

from ariadne import (
    ObjectType,
    load_schema_from_path,
    make_executable_schema,
)
from ariadne.contrib.django.scalars import datetime_scalar, date_scalar

from apps.graphql.resolvers.blog import (
    resolve_blogpages,
    resolve_blogpage,
    resolve_blogcategories,
)
from apps.graphql.resolvers.charts import (
    resolve_web_of_transnational_deals,
    country_investments_and_rankings,
    global_rankings,
    resolve_statistics,
    resolve_deal_aggregations,
)
from apps.graphql.resolvers.deal import (
    resolve_deal,
    resolve_deals,
    resolve_dealversions,
    resolve_change_deal_status,
)
from apps.graphql.resolvers.formfields import resolve_formfields
from apps.graphql.resolvers.investor import (
    resolve_investor,
    resolve_investors,
    # resolve_involvements,
    resolve_investorversions,
)
from apps.graphql.resolvers.map import resolve_markers
from apps.graphql.resolvers.misc import (
    resolve_countries,
    resolve_regions,
    resolve_minerals,
    resolve_crops,
    resolve_animals,
    resolve_chart_descriptions,
    resolve_currencies,
)
from apps.graphql.resolvers.user import (
    resolve_user,
    resolve_login,
    resolve_logout,
    resolve_users,
    user_regional_info_type,
    user_type,
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
query.set_field("deal_aggregations", resolve_deal_aggregations)
query.set_field("investor", resolve_investor)
query.set_field("investors", resolve_investors)
query.set_field("investorversions", resolve_investorversions)
# query.set_field("involvements", resolve_involvements)
query.set_field("countries", resolve_countries)
query.set_field("regions", resolve_regions)
query.set_field("currencies", resolve_currencies)
query.set_field("animals", resolve_animals)
query.set_field("crops", resolve_crops)
query.set_field("minerals", resolve_minerals)
query.set_field("formfields", resolve_formfields)
query.set_field("statistics", resolve_statistics)
query.set_field("blogpages", resolve_blogpages)
query.set_field("blogpage", resolve_blogpage)
query.set_field("blogcategories", resolve_blogcategories)
query.set_field("transnational_deals", resolve_web_of_transnational_deals)
query.set_field("country_investments_and_rankings", country_investments_and_rankings)
query.set_field("global_rankings", global_rankings)
query.set_field("chart_descriptions", resolve_chart_descriptions)
query.set_field("markers", resolve_markers)

mutation = ObjectType("Mutation")
mutation.set_field("login", resolve_login)
mutation.set_field("logout", resolve_logout)
mutation.set_field("change_deal_status", resolve_change_deal_status)

schema = make_executable_schema(
    type_defs,
    [datetime_scalar, date_scalar, geopoint_scalar],
    query,
    mutation,
    user_type,
    user_regional_info_type,
)
