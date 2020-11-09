import gc
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
from apps.utils import arrayfield_choices_display

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
    "Operating company: Action comment"
]

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

involvement_headers = [
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


class DataDownload:
    def __init__(self, request):
        self.request = request
        deal_id = self.request.GET.get("deal_id")
        filters = self.request.GET.get("filters")
        self.return_format = self.request.GET.get("format", "html")

        if deal_id:
            self._single_deal(deal_id)
        else:
            self._multiple_deals(filters)

    def _single_deal(self, deal_id):
        deal = Deal.objects.get(id=deal_id)
        self.deals = [deal.legacy_download_list_format()]
        (
            self.investors,
            self.involvements,
        ) = InvolvementNetwork().flat_view_for_download(deal.operating_company)
        self.filename = f"deal_{deal_id}"

    def _multiple_deals(self, filters):
        self.filters = []
        if filters:
            self.filters = json.loads(filters)

        deal_qs = Deal.objects.public()\
            .filter(parse_filters(self.filters))\
            .prefetch_related("top_investors")\
            .prefetch_related("top_investors__country")\
            .order_by("id")
        self.deals = [
            deal.legacy_download_list_format()
            for deal in queryset_iterator(deal_qs)
        ]

        investor_qs = Investor.objects.public()\
            .order_by("id")\
            .prefetch_related("country")
        self.investors = [
            [
                investor.id,
                investor.name,
                investor.country.name if investor.country else "",
                investor.get_classification_display(),
                investor.homepage,
                investor.opencorporates,
                investor.comment,
                "",  # TODO. get action comment here? really? :S
            ]
            for investor in queryset_iterator(investor_qs)
        ]

        involvement_qs = InvestorVentureInvolvement.objects.public()\
            .prefetch_related("investor")\
            .prefetch_related("venture")\
            .prefetch_related("loans_currency")
        self.involvements = [
            [
                involvement.venture_id,
                involvement.venture.name,
                involvement.investor_id,
                involvement.investor.name,
                involvement.get_role_display(),
                "|".join(
                    arrayfield_choices_display(
                        involvement.investment_type, involvement.INVESTMENT_TYPE_CHOICES
                    )
                ),
                involvement.percentage,
                involvement.loans_amount,
                involvement.loans_currency,
                involvement.loans_date,
                # involvement.get_parent_relation_display(),
                involvement.comment,
            ]
            for involvement in queryset_iterator(involvement_qs)
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


def queryset_iterator(queryset, chunksize=1000):
    '''''
    https://www.djangosnippets.org/snippets/1949/

    Iterate over a Django Queryset ordered by the primary key

    This method loads a maximum of chunksize (default: 1000) rows in it's
    memory at the same time while django normally would load all rows in it's
    memory. Using the iterator() method only causes it to not preload all the
    classes.

    Note that the implementation of the iterator does not support ordered query sets.
    '''
    pk = 0
    last_pk = queryset.order_by('-pk')[0].pk
    queryset = queryset.order_by('pk')
    while pk < last_pk:
        for row in queryset.filter(pk__gt=pk)[:chunksize]:
            pk = row.pk
            yield row
        gc.collect()
