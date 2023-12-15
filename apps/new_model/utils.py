from django.db import connection
from django.db.models import Q

from .involvement_sql import GRAPH_QUERY


class InvolvementNetwork:
    def __init__(self, include_ventures=False):
        self.traveled_edges = []
        self.seen_investors = set()
        self.include_ventures = include_ventures
        self.MAX_DEPTH = 30

    def get_network(self, investor_id, depth, include_deals=False) -> dict:
        from .models import Involvement, InvestorHull, DealHull

        depth = min(depth, self.MAX_DEPTH)

        min_depth = depth
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
        # ic(depth, min_depth)
        all_involvements = Involvement.objects.filter(
            Q(parent_investor_id__in=investor_ids)
            | Q(child_investor_id__in=investor_ids)
        ).values(
            "id",
            "parent_investor_id",
            "child_investor_id",
            "role",
            "investment_type",
        )

        all_investors = (
            InvestorHull.objects.filter(id__in=investor_ids)
            .exclude(active_version=None)
            .values(
                "id",
                "active_version_id",
                "active_version__name",
                "active_version__country_id",
                "active_version__homepage",
                "active_version__classification",
                "active_version__comment",
            )
        )
        all_investor_ids = set(x["id"] for x in all_investors)

        rich_nodes = []
        for node in all_investors:
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
                    for invo in all_involvements
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
            deals = DealHull.objects.filter(
                active_version__operating_company__investor_id__in=[
                    x["id"] for x in all_investors
                ]
            ).values(
                "id", "country_id", "active_version__operating_company__investor_id"
            )

            for deal in deals:
                rich_nodes += [
                    {
                        "data": {
                            "deal_id": deal["id"],
                            "id": f"D{deal['id']}",
                            "name": f"#{deal['id']}",
                            "country_id": deal["country_id"],
                            "bgColor": "rgba(252,148,30,1)",
                            "dealNode": True,
                        }
                    }
                ]
                rich_edges += [
                    {
                        "data": {
                            "id": f"{deal['active_version__operating_company__investor_id']}_D{deal['id']}",
                            "source": deal[
                                "active_version__operating_company__investor_id"
                            ],
                            "target": f"D{deal['id']}",
                            "edge_color": "rgba(252,148,30,1)",
                        }
                    }
                ]

        return {
            "elements": {
                "nodes": rich_nodes,
                "edges": rich_edges,
            },
            "involvements": all_involvements,
            "more_exist": min_depth == 0,
            "full_depth": None if min_depth == 0 else (depth - min_depth + 1),
        }
