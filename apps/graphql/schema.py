import pathlib

from ariadne import (
    ObjectType,
    ScalarType,
    load_schema_from_path,
    make_executable_schema,
)

from apps.graphql.deal import resolve_deal, resolve_deals
from apps.graphql.investor import resolve_investor, resolve_investors

schema_file = pathlib.Path(__file__).parent.joinpath("schema.graphql")
type_defs = load_schema_from_path(schema_file)

query = ObjectType("Query")

query.set_field("deal", resolve_deal)
query.set_field("deals", resolve_deals)

query.set_field("investor", resolve_investor)
query.set_field("investors", resolve_investors)

schema = make_executable_schema(type_defs, query)
