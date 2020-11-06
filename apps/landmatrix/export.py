import json

from django.http import HttpResponse
from django.shortcuts import render
from openpyxl import Workbook
from openpyxl.utils.exceptions import IllegalCharacterError

from apps.graphql.tools import parse_filters
from apps.landmatrix.models import Deal, Investor, InvestorVentureInvolvement
from apps.landmatrix.utils import InvolvementNetwork

heads = [
    "Deal ID",
    "Is public",
    "Deal scope",
    "Deal size",
    "Current size under contract",
    "Current size in operation (production)",
    "Current negotiation status",
    "Current implementation status",
    "Fully updated",
    "Top parent companies",
]


class DataDownload:
    def __init__(self, request):
        self.request = request
        deal_id = self.request.GET.get("deal_id")
        filters = self.request.GET.get("filters")
        self.return_format = self.request.GET.get("format", "html")

        if deal_id:
            deal = Deal.objects.get(id=deal_id)
            try:
                public = deal.is_public_deal() and "Yes"
            except Deal.IsNotPublic:
                public = "No"
            top_investors = "|".join(
                [
                    "#".join(
                        [
                            ti.name.replace("#", "").replace("\n", "").strip(),
                            str(ti.id),
                            ti.country.name if ti.country else "",
                        ]
                    )
                    for ti in deal.top_investors.all()
                ]
            )
            self.deals = [
                [
                    deal.id,
                    public,
                    "transnational" if deal.transnational else "domestic",
                    deal.deal_size,
                    deal.current_contract_size or "0",
                    deal.current_production_size or "0",
                    deal.get_current_negotiation_status_display(),
                    deal.get_current_implementation_status_display(),
                    deal.fully_updated_at,
                    top_investors,
                ]
            ]

            (
                self.investors,
                self.involvements,
            ) = InvolvementNetwork().flat_view_for_download(deal.operating_company)

        else:
            self.filters = json.loads(filters)
            self.deals = (
                Deal.objects.public().filter(parse_filters(self.filters)).order_by("id")
            )
            self.investors = Investor.objects.all()
            self.involvements = InvestorVentureInvolvement.objects.all()

    def get_response(self):
        if self.return_format == "xlsx":
            return self.xlsx()
        return self.html()

    @property
    def deal_headers(self):
        return [
            "Deal ID",
            "Is public",
            "Deal scope",
            "Deal size",
            "Current size under contract",
            "Current size in operation (production)",
            "Current negotiation status",
            "Current implementation status",
            "Fully updated",
            "Top parent companies",
        ]

    @property
    def investor_headers(self):
        return [
            "Investor ID",
            "Name",
            "Country of registration/origin",
            "Classification",
            "Investor homepage",
            "Opencorporates link",
            "Comment",
            "Action comment",
        ]

    @property
    def involvement_headers(self):
        return [
            "Investor ID Downstream",
            "Investor Name Downstream",
            "Investor ID Upstream",
            "Investor Name Upstream",
            "Relation type",
            "Investment type",
            "Ownership share",
            "Loan amount",
            "Loan currency",
            "Loan date",
            "Comment",
        ]

    def html(self):
        ctx = {
            "deal_headers": self.deal_headers,
            "deals": self.deals,
            "investor_headers": self.investor_headers,
            "investors": self.investors,
            "involvement_headers": self.involvement_headers,
            "involvements": self.involvements,
        }
        return render(self.request, "landmatrix/export_table.html", ctx)

    def xlsx(self):
        response = HttpResponse(content_type="application/ms-excel")
        response["Content-Disposition"] = f"attachment; filename={'export.xlsx'}"
        wb = Workbook(write_only=True)

        # Deals tab
        ws_deals = wb.create_sheet(title="Deals")
        ws_deals.append(self.deal_headers)
        for item in self.deals:
            try:
                ws_deals.append(item)
            except IllegalCharacterError:  # pragma: no cover
                ws_deals.append(
                    [str(i).encode("unicode_escape").decode("utf-8") for i in item]
                )

        # Involvements tab
        ws_involvements = wb.create_sheet(title="Involvements")
        ws_involvements.append(self.involvement_headers)
        for item in self.involvements:
            ws_involvements.append(item)

        # Investors tab
        ws_investors = wb.create_sheet(title="Investors")
        ws_investors.append(self.investor_headers)
        for item in self.investors:
            ws_investors.append(item)

        wb.save(response)
        return response
