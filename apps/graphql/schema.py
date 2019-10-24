import pathlib

from ariadne import ObjectType, load_schema_from_path, make_executable_schema

from apps.graphql.deal import resolve_deal, resolve_deals

schema_file = pathlib.Path(__file__).parent.joinpath("schema.graphql")
type_defs = load_schema_from_path(schema_file)

query = ObjectType("Query")

query.set_field("deal", resolve_deal)
query.set_field("deals", resolve_deals)
# query.set_field("userSector", resolve_user_sector)
# query.set_field("userSectors", resolve_user_sectors)
# query.set_field("userGroups", resolve_user_groups)
# query.set_field("userSubGroups", resolve_user_subgroups)
#
# query.set_field("technologies", resolve_technologies)
# query.set_field("listOptStrategies", resolve_list_opt_strategies)
# query.set_field("listSzenarios", resolve_list_scenarios)
#
# query.set_field("kpiSections", resolve_kpi_sections)
# query.set_field("recommendations", resolve_recommendations)
#
# query.set_field("energyCarriers", resolve_energy_carriers)

schema = make_executable_schema(type_defs, query)
