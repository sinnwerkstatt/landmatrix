from django.db import connection
from django.db.models import Q, QuerySet

from .involvement_sql import GRAPH_QUERY, UNIDIRECTIONAL_GRAPH_QUERY
from .models.new import InvestorHull, Involvement, DealHull


class InvolvementNetwork:
    def __init__(self):
        self.MAX_DEPTH = 30

    def get_network(
        self, investor_id, depth=1, show_ventures=True
    ) -> tuple[QuerySet[InvestorHull], QuerySet[Involvement], set[tuple], int]:
        depth = min(depth, self.MAX_DEPTH)

        min_depth = depth
        if show_ventures:
            with connection.cursor() as cursor:
                # depth-1 to fix off-by-one issue where "1" is giving two edges depth
                cursor.execute(GRAPH_QUERY, [depth - 1, investor_id])
                rows = cursor.fetchall()

            investor_ids = set()
            edges = set()
            for row in rows:
                # print(row)
                row_depth, row_investor_id, down_edges, up_edges = row
                investor_ids.add(row_investor_id)
                for down_edge in down_edges:
                    investor_ids.add(down_edge)
                    edges.add((row_investor_id, down_edge))
                for up_edge in up_edges:
                    investor_ids.add(up_edge)
                    edges.add((up_edge, row_investor_id))
                min_depth = min(min_depth, row_depth)
        else:
            with connection.cursor() as cursor:
                # depth-1 to fix off-by-one issue where "1" is giving two edges depth
                cursor.execute(UNIDIRECTIONAL_GRAPH_QUERY, [depth - 1, investor_id])
                rows = cursor.fetchall()
            investor_ids = set()
            edges = set()
            for row in rows:
                row_depth, row_investor_id, up_edges = row
                investor_ids.add(row_investor_id)
                for up_edge in up_edges:
                    investor_ids.add(up_edge)
                    edges.add((up_edge, row_investor_id))
                min_depth = min(min_depth, row_depth)
        # ic(depth, min_depth)
        all_involvements: QuerySet[Involvement] = Involvement.objects.filter(
            Q(parent_investor_id__in=investor_ids)
            | Q(child_investor_id__in=investor_ids)
        ).order_by("id")

        all_investors: QuerySet[InvestorHull] = (
            InvestorHull.objects.active().filter(id__in=investor_ids).order_by("id")
        )
        return all_investors, all_involvements, edges, min_depth

    def get_network_x(
        self, investor_id, depth=1, include_deals=False, show_ventures=True
    ) -> dict:
        all_investors, all_involvements, edges, min_depth = self.get_network(
            investor_id,
            depth=depth,
            show_ventures=show_ventures,
        )

        all_investor_ids = set(all_investors.values_list("id", flat=True))
        all_investors_values = all_investors.values(
            "id",
            "active_version_id",
            "active_version__name",
            "active_version__country_id",
            "active_version__homepage",
            "active_version__classification",
            "active_version__comment",
        )
        all_involvements_values = all_involvements.values(
            "id",
            "parent_investor_id",
            "child_investor_id",
            "role",
            "investment_type",
        )

        rich_nodes = []
        for node in all_investors_values:
            if node["id"] == investor_id:
                node["bgColor"] = "rgba(68,183,181,1)"
                node["rootNode"] = True
            else:
                node["bgColor"] = "rgba(143,214,212,1)"
            node["name"] = node["active_version__name"]
            rich_nodes += [{"data": node}]

        rich_edges = []
        for edge in edges:
            involvement = next(
                (
                    invo
                    for invo in all_involvements_values
                    if invo["parent_investor_id"] == edge[0]
                    and invo["child_investor_id"] == edge[1]
                )
            )
            if edge[0] not in all_investor_ids or edge[1] not in all_investor_ids:
                continue
            edge_color = (
                "rgba(234,128,121,1)"
                if involvement["role"] == "PARENT"
                else "rgba(133,146,238,1)"
            )
            rich_edges += [
                {
                    "data": {
                        "id": f"{edge[0]}_{edge[1]}",
                        "source": edge[0],
                        "target": edge[1],
                        "edge_color": edge_color,
                        "target_arrow_shape": "triangle",
                    }
                }
            ]

        if include_deals:
            deals = (
                DealHull.objects.normal()
                .filter(active_version__operating_company_id__in=all_investor_ids)
                .values(
                    "id",
                    "country_id",
                    "active_version__operating_company_id",
                    "active_version__intention_of_investment",
                    "active_version__implementation_status",
                    "active_version__negotiation_status",
                    "active_version__intended_size",
                    "active_version__contract_size",
                )
            )

            for deal in deals:
                rich_nodes += [
                    {
                        "data": {
                            "deal_id": deal["id"],
                            "id": f"D{deal['id']}",
                            "name": f"#{deal['id']}",
                            "country_id": deal["country_id"],
                            "intention_of_investment": deal[
                                "active_version__intention_of_investment"
                            ],
                            "implementation_status": deal[
                                "active_version__implementation_status"
                            ],
                            "negotiation_status": deal[
                                "active_version__negotiation_status"
                            ],
                            "intended_size": deal["active_version__intended_size"],
                            "contract_size": deal["active_version__contract_size"],
                            "bgColor": "rgba(252,148,30,1)",
                            "dealNode": True,
                        }
                    }
                ]
                rich_edges += [
                    {
                        "data": {
                            "id": f"{deal['active_version__operating_company_id']}_D{deal['id']}",
                            "source": deal["active_version__operating_company_id"],
                            "target": f"D{deal['id']}",
                            "edge_color": "rgba(252,148,30,1)",
                        }
                    }
                ]

        return {
            "elements": {"nodes": rich_nodes, "edges": rich_edges},
            "involvements": all_involvements_values,
            "more_exist": min_depth == 0,
            "full_depth": None if min_depth == 0 else (depth - min_depth + 1),
        }
