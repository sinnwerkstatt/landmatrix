from apps.landmatrix.models import InvestorVentureInvolvement, Investor
from apps.utils import arrayfield_choices_display


class InvolvementNetwork:
    def __init__(self, include_ventures=False):
        self.seen_investors = set()
        self.include_ventures = include_ventures

    def get_network(self, investor_id, exclude=None, depth=10):
        if depth <= 0:
            return

        # find all involvements
        involvements = []
        qs = (
            InvestorVentureInvolvement.objects.filter(status__in=(2, 3))
            .filter(investor__status__in=(2, 3), venture__status__in=(2, 3))
            .prefetch_related("investor")
            .prefetch_related("investor__deals")
            .prefetch_related("venture")
            .prefetch_related("venture__deals")
        )

        # traverse over the investors
        network_investors = qs.filter(venture_id=investor_id).exclude(
            investor_id=exclude
        )
        for inv in network_investors:
            if inv.id in self.seen_investors:
                continue
            involvement = inv.to_dict()
            involvement["involvement_type"] = "INVESTOR"
            investor = inv.investor.to_dict()
            investor["involvements"] = self.get_network(
                inv.investor_id, investor_id, depth - 1
            )
            involvement["investor"] = investor
            involvements += [involvement]
            self.seen_investors.add(inv.id)

        # traverse over the ventures
        if self.include_ventures:
            network_ventures = qs.filter(investor_id=investor_id).exclude(
                venture_id=exclude
            )
            for inv in network_ventures:
                if inv.id in self.seen_investors:
                    continue
                involvement = inv.to_dict()
                involvement["involvement_type"] = "VENTURE"
                venture = inv.venture.to_dict()
                venture["involvements"] = self.get_network(
                    inv.venture_id, investor_id, depth - 1
                )
                involvement["investor"] = venture
                involvements += [involvement]
                self.seen_investors.add(inv.id)

        return involvements

    def flat_view_for_download(self, investor, exclude=None, depth=10):
        network = self.get_network(investor.id, exclude=exclude, depth=depth)
        inv1 = investor.to_dict()
        investors, involvements = self._yield_datasets(inv1, network)
        return [self._investor_dict_to_list(inv1)] + investors, involvements

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
                    InvestorVentureInvolvement._meta.get_field(
                        "investment_type"
                    ).choices,
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
                        dict(
                            InvestorVentureInvolvement._meta.get_field("role").choices
                        )[involvement["role"]]
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
