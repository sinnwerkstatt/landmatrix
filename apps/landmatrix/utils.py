from apps.utils import arrayfield_choices_display

from .models.investor import Investor, InvestorVentureInvolvement
from django.db import connection
from django.db.models import Q, QuerySet

from .involvement_sql import GRAPH_QUERY, UNIDIRECTIONAL_GRAPH_QUERY
from .models.new import InvestorHull, Involvement, DealHull


class InvolvementNetwork:
    def __init__(self, include_ventures=False, max_depth=10):
        self.traveled_edges = []
        self.seen_investors = set()
        self.include_ventures = include_ventures
        self.max_depth = max_depth

    def get_network(self, investor_id, exclude=None, depth=1) -> list:
        if depth > self.max_depth:
            return []

        # find all involvements
        involvements = []
        qs: QuerySet[InvestorVentureInvolvement] = (
            InvestorVentureInvolvement.objects.active()
            .prefetch_related("investor")
            .prefetch_related("investor__deals")
            .prefetch_related("venture")
            .prefetch_related("venture__deals")
        )

        # traverse over the investors
        network_investor_involvements = qs.filter(venture_id=investor_id).exclude(
            investor_id=exclude
        )
        for inv in network_investor_involvements:
            if {investor_id, inv.investor_id} in self.traveled_edges:
                continue
            involvement = inv.to_dict()
            involvement["involvement_type"] = "INVESTOR"
            investor = inv.investor.to_dict()
            involvement["depth"] = depth
            involvement["investor"] = investor
            involvements += [involvement]
            self.traveled_edges += [{investor_id, inv.investor_id}]

        # traverse over the ventures
        if self.include_ventures:
            network_venture_involvements = qs.filter(investor_id=investor_id).exclude(
                venture_id=exclude
            )
            for inv in network_venture_involvements:
                if {investor_id, inv.venture_id} in self.traveled_edges:
                    continue
                involvement = inv.to_dict()
                involvement["involvement_type"] = "VENTURE"
                venture = inv.venture.to_dict()
                involvement["depth"] = depth
                involvement["investor"] = venture
                involvements += [involvement]
                self.traveled_edges += [{investor_id, inv.venture_id}]

        if depth < self.max_depth:
            for node in involvements:
                node["investor"]["involvements"] = self.get_network(
                    node["investor"]["id"], investor_id, depth + 1
                )

        return involvements

    # appreantly unneeded
    # def flat_view_for_download(self, investor):
    #     network = self.get_network(investor.id, exclude=None)
    #     inv1 = investor.to_dict()
    #     investors, involvements = self._yield_datasets(inv1, network)
    #     return [self._investor_dict_to_list(inv1)] + investors, involvements

    @staticmethod
    def _investor_dict_to_list(investor_dict):
        inv_country = investor_dict.get("country")
        inv_country_name = inv_country.get("name") if inv_country else ""
        # TODO: this duplicates row generation in export.py
        return [
            investor_dict["id"],
            investor_dict["name"],
            inv_country_name,
            str(
                dict(Investor.CLASSIFICATION_CHOICES).get(
                    investor_dict.get("classification", ""), ""
                )
            ),
            investor_dict.get("homepage", ""),
            investor_dict.get("opencorporates", ""),
            # investor_dict.get("datasources", ""),
            investor_dict.get("comment", ""),
            "",  # TODO. get action comment here? really? :S
        ]

    def _yield_datasets(self, tl_investor, involvements):
        ret_involvements = []
        ret_investors = []
        for involvement in involvements:
            investor_dict = involvement["investor"]
            x, y = self._yield_datasets(investor_dict, investor_dict["involvements"])

            ret_investors += [self._investor_dict_to_list(investor_dict)] + x
            investment_type = "|".join(
                arrayfield_choices_display(
                    involvement["investment_type"],
                    InvestorVentureInvolvement.INVESTMENT_TYPE_CHOICES,
                )
            )
            # TODO: this duplicates row generation in export.py
            ret_involvements += [
                [
                    involvement["id"],
                    tl_investor["id"],
                    tl_investor["name"],
                    involvement["investor"]["id"],
                    involvement["investor"]["name"],
                    str(
                        dict(InvestorVentureInvolvement.ROLE_CHOICES).get(
                            involvement["role"], ""
                        )
                    ),
                    investment_type,
                    involvement["percentage"],
                    involvement["loans_amount"],
                    involvement["loans_currency"],
                    involvement["loans_date"],
                    involvement["comment"],
                ]
            ] + y

        return ret_investors, ret_involvements


class InvolvementNetwork2:
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
        )

        all_investors: QuerySet[InvestorHull] = InvestorHull.objects.filter(
            id__in=investor_ids
        ).exclude(active_version=None)
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
            deals = DealHull.objects.filter(
                active_version__operating_company_id__in=all_investor_ids
            ).values("id", "country_id", "active_version__operating_company_id")

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
