import json
import zipfile
from io import BytesIO

import unicodecsv as csv
from django.http import HttpResponse
from django.shortcuts import render
from openpyxl import Workbook
from openpyxl.utils.exceptions import IllegalCharacterError

from apps.graphql.tools import parse_filters
from apps.landmatrix.models import Deal, Investor, InvestorVentureInvolvement
from apps.landmatrix.utils import InvolvementNetwork
from apps.utils import qs_values_to_dict, arrayfield_choices_display

deal_headers = [
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
    "Operating company: Investor ID",
    "Operating company: Name",
    "Operating company: Country of registration/origin",
    "Operating company: Classification",
    "Operating company: Investor homepage",
    "Operating company: Opencorporates link",
    "Operating company: Comment",
]
deal_fields = [
    "id",
    "is_public",
    "transnational",
    "deal_size",
    "current_contract_size",
    "current_production_size",
    "current_negotiation_status",
    "current_implementation_status",
    "fully_updated_at",
    "top_investors",
    "operating_company__id",
    "operating_company__name",
    "operating_company__country__name",
    "operating_company__classification",
    "operating_company__homepage",
    "operating_company__opencorporates",
    "operating_company__comment",
]
current_negotiation_status_map = {
    "EXPRESSION_OF_INTEREST": "Intended (Expression of interest)",
    "UNDER_NEGOTIATION": "Intended (Under negotiation)",
    "MEMORANDUM_OF_UNDERSTANDING": "Intended (Memorandum of understanding)",
    "ORAL_AGREEMENT": "Concluded (Oral Agreement)",
    "CONTRACT_SIGNED": "Concluded (Contract signed)",
    "NEGOTIATIONS_FAILED": "Failed (Negotiations failed)",
    "CONTRACT_CANCELED": "Failed (Contract cancelled)",
    "CONTRACT_EXPIRED": "Contract expired",
    "CHANGE_OF_OWNERSHIP": "Change of ownership",
    None: "None",
}

current_implementation_status_map = {
    "PROJECT_NOT_STARTED": "Project not started",
    "STARTUP_PHASE": "Startup phase (no production)",
    "IN_OPERATION": "In operation (production)",
    "PROJECT_ABANDONED": "Project abandoned",
    None: "None",
}

deal_choices_fields = {
    # "current_negotiation_status": current_negotiation_status_map,
    # "current_implementation_status": current_implementation_status_map,
    "investor_classification": dict(Investor._meta.get_field("classification").choices),
}
deal_sub_fields = {
    "top_investors": [
        "top_investors__id",
        "top_investors__name",
        "top_investors__country__name",
    ]
}
deal_flattened_fields = []
for f in deal_fields:
    if f in deal_sub_fields:
        for sf in deal_sub_fields[f]:
            deal_flattened_fields.append(sf)
    else:
        deal_flattened_fields.append(f)

investor_headers = [
    "Investor ID",
    "Name",
    "Country of registration/origin",
    "Classification",
    "Investor homepage",
    "Opencorporates link",
    "Comment",
    "Action comment",
]
investor_fields = [
    "id",
    "name",
    "country__name",
    "classification",
    "homepage",
    "opencorporates",
    "comment",
]
investor_choices_fields = {
    "classification": dict(Investor._meta.get_field("classification").choices)
}

involvement_headers = [
    "Involvement ID",
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
involvement_fields = [
    "id",
    "venture_id",
    "venture__name",
    "investor_id",
    "investor__name",
    "role",
    "investment_type",
    "percentage",
    "loans_amount",
    "loans_currency",
    "loans_date",
    "comment",
]
involvement_choices_fields = {
    "role": dict(InvestorVentureInvolvement._meta.get_field("role").choices),
}


class DataDownload:
    def __init__(self, request):
        self.request = request
        self.user = request.user
        deal_id = self.request.GET.get("deal_id")
        filters = self.request.GET.get("filters")
        self.return_format = self.request.GET.get("format", "html")

        if deal_id:
            self._single_deal(deal_id)
        else:
            self._multiple_deals(filters)

    def _single_deal(self, deal_id):
        qs = Deal.objects.filter(id=deal_id)
        deal = qs[0]
        self.deals = [
            self.deal_download_format(qs_dict)
            for qs_dict in qs_values_to_dict(
                qs, deal_flattened_fields, deal_sub_fields.keys()
            )
        ]
        self.investors = []
        self.involvements = []
        if deal.operating_company:
            (
                self.investors,
                self.involvements,
            ) = InvolvementNetwork().flat_view_for_download(deal.operating_company)
        self.filename = f"deal_{deal_id}"

    def _multiple_deals(self, filters):
        self.filters = []
        if filters:
            self.filters = json.loads(filters)

        qs = (
            Deal.objects.visible(self.user, subset="ACTIVE")
            .filter(parse_filters(self.filters))
            .order_by("id")
        )
        self.deals = [
            self.deal_download_format(qs_dict)
            for qs_dict in qs_values_to_dict(
                qs, deal_flattened_fields, deal_sub_fields.keys()
            )
        ]

        qs = Investor.objects.visible(self.user).order_by("id")
        self.investors = [
            self.investor_download_format(qs_dict)
            for qs_dict in qs_values_to_dict(qs, investor_fields, [])
        ]

        qs = InvestorVentureInvolvement.objects.visible(self.user).order_by("id")
        self.involvements = [
            self.involvement_download_format(qs_dict)
            for qs_dict in qs_values_to_dict(qs, involvement_fields, [])
        ]
        self.filename = "export"

    def get_response(self):
        if self.return_format == "xlsx":
            return self.xlsx()
        if self.return_format == "csv":
            return self.csv()
        return self.html()

    def html(self):
        ctx = {
            "deal_headers": deal_headers,
            "deals": self.deals,
            "investor_headers": investor_headers,
            "investors": self.investors,
            "involvement_headers": involvement_headers,
            "involvements": self.involvements,
        }
        return render(self.request, "landmatrix/export_table.html", ctx)

    def xlsx(self):
        response = HttpResponse(content_type="application/ms-excel")
        response["Content-Disposition"] = f'attachment; filename="{self.filename}.xlsx"'
        wb = Workbook(write_only=True)

        # Deals tab
        ws_deals = wb.create_sheet(title="Deals")
        ws_deals.append(deal_headers)
        for item in self.deals:
            try:
                ws_deals.append(item)
            except IllegalCharacterError:  # pragma: no cover
                ws_deals.append(
                    [str(i).encode("unicode_escape").decode("utf-8") for i in item]
                )

        # Involvements tab
        ws_involvements = wb.create_sheet(title="Involvements")
        ws_involvements.append(involvement_headers)
        for item in self.involvements:
            ws_involvements.append(item)

        # Investors tab
        ws_investors = wb.create_sheet(title="Investors")
        ws_investors.append(investor_headers)
        for item in self.investors:
            ws_investors.append(item)

        wb.save(response)
        return response

    @staticmethod
    def _csv_writer(data):
        # Deals CSV
        file = BytesIO()
        writer = csv.writer(file, delimiter=";")  # encoding='cp1252'
        for item in data:
            writer.writerow(item)
        file.seek(0)
        return file.getvalue()

    def csv(self):
        result = BytesIO()
        zip_file = zipfile.ZipFile(result, "w")

        # Deals CSV
        deals_data = [deal_headers] + self.deals
        zip_file.writestr("deals.csv", self._csv_writer(deals_data))

        # Involvements CSV
        involvements_data = [involvement_headers] + self.involvements
        zip_file.writestr("involvements.csv", self._csv_writer(involvements_data))

        # Investors CSV
        investors_data = [investor_headers] + self.investors
        zip_file.writestr("investors.csv", self._csv_writer(investors_data))

        zip_file.close()
        response = HttpResponse(
            result.getvalue(), content_type="application/x-zip-compressed"
        )
        response["Content-Disposition"] = f'attachment; filename="{self.filename}.zip"'
        return response

    @staticmethod
    def deal_download_format(data):
        data["is_public"] = "Yes" if data["is_public"] else "No"
        if "transnational" in data:
            data["transnational"] = (
                "transnational" if data["transnational"] else "domestic"
            )

        # flatten top investors
        data["top_investors"] = "|".join(
            [
                "#".join(
                    [
                        ti["name"].replace("#", "").replace("\n", "").strip(),
                        str(ti["id"]),
                        ti["country__name"] if "country__name" in ti else "",
                    ]
                )
                for ti in data["top_investors"]
            ]
        )
        # map operating company fields
        if "operating_company" in data:
            data["operating_company__id"] = data["operating_company"]["id"]
            data["operating_company__name"] = data["operating_company"]["name"]
            if "country" in data["operating_company"]:
                data["operating_company__country__name"] = data["operating_company"][
                    "country"
                ]["name"]
            if "classification" in data["operating_company"]:
                data["operating_company__classification"] = str(
                    deal_choices_fields["investor_classification"][
                        data["operating_company"]["classification"]
                    ]
                )
            data["operating_company__homepage"] = data["operating_company"]["homepage"]
            data["operating_company__opencorporates"] = data["operating_company"][
                "opencorporates"
            ]
            data["operating_company__comment"] = data["operating_company"]["comment"]

        data["deal_size"] = int(data.get("deal_size", 0))
        data["current_contract_size"] = int(data.get("current_contract_size", 0))
        data["current_production_size"] = int(data.get("current_production_size", 0))

        imp_stat = data.get("current_implementation_status")
        data["current_implementation_status"] = current_implementation_status_map.get(
            imp_stat, imp_stat
        )

        neg_stat = data.get("current_negotiation_status")
        data["current_negotiation_status"] = current_negotiation_status_map.get(
            neg_stat, neg_stat
        )

        fully_updated_at = data.get("fully_updated_at")
        if fully_updated_at:
            data["fully_updated_at"] = fully_updated_at.isoformat()

        row = []
        for field in deal_fields:
            if field not in data:
                # empty fields
                data[field] = ""
            elif field in deal_choices_fields:
                # fields with choices
                data[field] = str(deal_choices_fields[field][data[field]])
            row.append(data[field])
        return row

    @staticmethod
    def investor_download_format(data):
        if "country" in data:
            data["country__name"] = data["country"]["name"]

        row = []
        for field in investor_fields:
            if field not in data:
                # empty fields
                data[field] = ""
            elif field in investor_choices_fields:
                # fields with choices
                data[field] = str(investor_choices_fields[field][data[field]])
            row.append(data[field])
        return row

    @staticmethod
    def involvement_download_format(data):
        data["venture__name"] = data["venture"]["name"]
        data["investor__name"] = data["investor"]["name"]

        if "investment_type" in data:
            data["investment_type"] = "|".join(
                arrayfield_choices_display(
                    data["investment_type"],
                    InvestorVentureInvolvement._meta.get_field(
                        "investment_type"
                    ).choices,
                )
            )
        row = []
        for field in involvement_fields:
            if field not in data:
                # empty fields
                data[field] = ""
            elif field in involvement_choices_fields:
                # fields with choices
                data[field] = str(involvement_choices_fields[field][data[field]])
            row.append(data[field])
        return row
