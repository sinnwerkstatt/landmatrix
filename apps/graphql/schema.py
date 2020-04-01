import pathlib

from ariadne import (
    ObjectType,
    load_schema_from_path,
    make_executable_schema,
)
from ariadne.contrib.django.scalars import datetime_scalar

from apps.graphql.deal import resolve_deal, resolve_deals
from apps.graphql.investor import resolve_investor, resolve_investors
from apps.graphql.user import resolve_user, resolve_login, resolve_logout, resolve_users

schema_file = pathlib.Path(__file__).parent.joinpath("schema.graphql")
type_defs = load_schema_from_path(schema_file)

query = ObjectType("Query")
query.set_field("me", resolve_user)
query.set_field("user", resolve_user)
query.set_field("users", resolve_users)
query.set_field("deal", resolve_deal)
query.set_field("deals", resolve_deals)
query.set_field("investor", resolve_investor)
query.set_field("investors", resolve_investors)

mutation = ObjectType("Mutation")
mutation.set_field("login", resolve_login)
mutation.set_field("logout", resolve_logout)

schema = make_executable_schema(type_defs, [datetime_scalar], query, mutation)
