import pathlib

from ariadne import ObjectType, load_schema_from_path, make_executable_schema
from ariadne_django.scalars import date_scalar


from .resolvers.deal import (
    resolve_add_deal_comment,
    resolve_change_deal_status,
    resolve_deal,
    resolve_deal_edit,
    resolve_deals,
)
from .resolvers.generics import (
    resolve_add_workflow_info_reply,
    resolve_resolve_workflow_info,
)
from .resolvers.investor import (
    resolve_add_investor_comment,
    resolve_change_investor_status,
    resolve_investor,
    resolve_investor_edit,
    resolve_investors,
    resolve_involvement_network,
)


schema_folder = str(pathlib.Path(__file__).parent.joinpath("schema"))
type_defs = load_schema_from_path(schema_folder)

query = ObjectType("Query")
query.set_field("deal", resolve_deal)
query.set_field("deals", resolve_deals)
query.set_field("investor", resolve_investor)
query.set_field("involvement_network", resolve_involvement_network)
query.set_field("investors", resolve_investors)
# query.set_field("involvements", resolve_involvements)

mutation = ObjectType("Mutation")
# deal
mutation.set_field("add_deal_comment", resolve_add_deal_comment)
mutation.set_field("change_deal_status", resolve_change_deal_status)
mutation.set_field("deal_edit", resolve_deal_edit)

# investor
mutation.set_field("add_investor_comment", resolve_add_investor_comment)
mutation.set_field("change_investor_status", resolve_change_investor_status)
mutation.set_field("investor_edit", resolve_investor_edit)


mutation.set_field("resolve_workflow_info", resolve_resolve_workflow_info)
mutation.set_field("add_workflow_info_reply", resolve_add_workflow_info_reply)

schema = make_executable_schema(
    type_defs,
    [date_scalar],
    query,
    mutation,
)
