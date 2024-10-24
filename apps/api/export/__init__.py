import zipfile
from io import BytesIO

import unicodecsv as csv
from django.http.response import HttpResponseBadRequest
from openpyxl import Workbook
from openpyxl.utils.exceptions import IllegalCharacterError

from django.contrib.postgres.expressions import ArraySubquery
from django.db.models import Case, OuterRef, QuerySet, When
from django.db.models.functions import JSONObject
from django.http import HttpResponse
from django.shortcuts import render

from apps.api.export import converter
from apps.api.quality_indicators.serializers import QueryParamsSerializer
from apps.landmatrix.involvement_network import InvolvementNetwork
from apps.landmatrix.models.top_investors import DealTopInvestors
from apps.landmatrix.models.deal import DealVersion, DealHull
from apps.landmatrix.models.investor import InvestorHull, Involvement
from apps.landmatrix.quality_indicators import DEAL_QIS
from apps.landmatrix.quality_indicators.deal import annotate_counts
from apps.landmatrix.utils import parse_filters

deal_headers = converter.deal_fields.values()
location_headers = [
    "ID",
    "Deal ID",
    "Spatial accuracy level",
    "Location",
    "Point",
    "Facility name",
    "Location description",
    "Comment on location",
]
contract_headers = [
    "ID",
    "Deal ID",
    "Contract number",
    "Contract date",
    "Contract expiration date",
    "Duration of the agreement",
    "Comment on contract",
]
datasource_headers = [
    "ID",
    "Deal ID",
    "Data source type",
    "URL",
    "File",
    "Publication title",
    "Date",
    "Name",
    "Organisation",
    "Email",
    "Phone",
    "Open Contracting ID",
    "Comment on data source",
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
investor_fields = [
    "id",
    "name",
    "country__name",
    "classification",
    "homepage",
    "opencorporates",
    "comment",
]

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
    "nid",
    "child_investor_id",
    "child_investor__active_version__name",
    "parent_investor_id",
    "parent_investor__active_version__name",
    "role",
    "investment_type",
    "percentage",
    "loans_amount",
    "loans_currency",
    "loans_date",
    "comment",
]


def _deal_qs_to_values(qs: QuerySet[DealVersion]):
    return (
        qs.values(
            "deal_id",
            "is_public",
            "transnational",
            "deal_size",
            "current_contract_size",
            "current_production_size",
            "current_negotiation_status",
            "current_implementation_status",
            "intended_size",
            "contract_size",
            "production_size",
            "land_area_comment",
            "intention_of_investment",
            "intention_of_investment_comment",
            "carbon_offset_project",
            "carbon_offset_project_comment",
            "nature_of_deal",
            "nature_of_deal_comment",
            "negotiation_status",
            "negotiation_status_comment",
            "implementation_status",
            "implementation_status_comment",
            "purchase_price",
            "purchase_price_currency",
            "purchase_price_type",
            "purchase_price_area",
            "purchase_price_comment",
            "annual_leasing_fee",
            "annual_leasing_fee_currency",
            "annual_leasing_fee_type",
            "annual_leasing_fee_area",
            "annual_leasing_fee_comment",
            "contract_farming",
            "on_the_lease_state",
            "on_the_lease",
            "off_the_lease_state",
            "off_the_lease",
            "contract_farming_comment",
            "total_jobs_created",
            "total_jobs_planned",
            "total_jobs_planned_employees",
            "total_jobs_planned_daily_workers",
            "total_jobs_current",
            "total_jobs_created_comment",
            "foreign_jobs_created",
            "foreign_jobs_planned",
            "foreign_jobs_planned_employees",
            "foreign_jobs_planned_daily_workers",
            "foreign_jobs_current",
            "foreign_jobs_created_comment",
            "domestic_jobs_created",
            "domestic_jobs_planned",
            "domestic_jobs_planned_employees",
            "domestic_jobs_planned_daily_workers",
            "domestic_jobs_current",
            "domestic_jobs_created_comment",
            "involved_actors",
            "project_name",
            "investment_chain_comment",
            "name_of_community",
            "name_of_indigenous_people",
            "people_affected_comment",
            "recognition_status",
            "recognition_status_comment",
            "community_consultation",
            "community_consultation_comment",
            "community_reaction",
            "community_reaction_comment",
            "land_conflicts",
            "land_conflicts_comment",
            "displacement_of_people",
            "displaced_people",
            "displaced_households",
            "displaced_people_from_community_land",
            "displaced_people_within_community_land",
            "displaced_households_from_fields",
            "displaced_people_on_completion",
            "displacement_of_people_comment",
            "negative_impacts",
            "negative_impacts_comment",
            "promised_compensation",
            "received_compensation",
            "promised_benefits",
            "promised_benefits_comment",
            "materialized_benefits",
            "materialized_benefits_comment",
            "presence_of_organizations",
            "former_land_owner",
            "former_land_owner_comment",
            "former_land_use",
            "former_land_use_comment",
            "former_land_cover",
            "former_land_cover_comment",
            "crops",
            "crops_comment",
            "animals",
            "animals_comment",
            "mineral_resources",
            "mineral_resources_comment",
            "contract_farming_crops",
            "contract_farming_crops_comment",
            "contract_farming_animals",
            "contract_farming_animals_comment",
            "electricity_generation",
            "electricity_generation_comment",
            "carbon_sequestration",
            "carbon_sequestration_comment",
            "has_domestic_use",
            "domestic_use",
            "has_export",
            "export",
            "export_country1",
            "export_country1_ratio",
            "export_country2",
            "export_country2_ratio",
            "export_country3",
            "export_country3_ratio",
            "use_of_produce_comment",
            "in_country_processing",
            "in_country_processing_comment",
            "in_country_processing_facilities",
            "in_country_end_products",
            "water_extraction_envisaged",
            "water_extraction_envisaged_comment",
            "source_of_water_extraction",
            "source_of_water_extraction_comment",
            "how_much_do_investors_pay_comment",
            "water_extraction_amount",
            "water_extraction_amount_comment",
            "use_of_irrigation_infrastructure",
            "use_of_irrigation_infrastructure_comment",
            "water_footprint",
            "gender_related_information",
            "overall_comment",
            "deal__confidential",
            "deal__confidential_comment",
            "deal__country",
            "deal__fully_updated_at",
        )
        .annotate(
            operating_company=Case(
                When(operating_company__active_version_id=None, then=None),
                default=JSONObject(
                    investor_id="operating_company__active_version__investor_id",
                    name="operating_company__active_version__name",
                    country__name="operating_company__active_version__country__name",
                    classification="operating_company__active_version__classification",
                    homepage="operating_company__active_version__homepage",
                    opencorporates="operating_company__active_version__opencorporates",
                    comment="operating_company__active_version__comment",
                ),
            )
        )
        .annotate(
            top_investors=(
                ArraySubquery(
                    DealTopInvestors.objects.exclude(investorhull__active_version=None)
                    .filter(investorhull__deleted=False)
                    .filter(dealversion_id=OuterRef("id"))
                    .order_by("-id")
                    .annotate(
                        active_version=JSONObject(
                            name="investorhull__active_version__name",
                            country_name="investorhull__active_version__country__name",
                        )
                    )
                    .values(
                        json=JSONObject(
                            id="investorhull_id", active_version="active_version"
                        )
                    )
                )
            )
        )
    )


class DataDownload:
    def __init__(self, request):
        self.request = request
        self.user = request.user
        deal_id = self.request.GET.get("deal_id")
        self.subset = self.request.GET.get("subset", "PUBLIC")
        self.return_format = self.request.GET.get("format", "html")

        if deal_id:
            self._single_deal(deal_id)
        else:
            self._multiple_deals()

    def _single_deal(self, deal_id):
        dealhull = DealHull.objects.visible(self.user, self.subset).get(id=deal_id)
        dealversions: QuerySet[DealVersion] = DealVersion.objects.filter(
            id=dealhull.active_version_id
        )

        version = dealversions[0]

        self.deals = [
            converter.deal_download_format(d) for d in _deal_qs_to_values(dealversions)
        ]

        self.locations = converter.location_download_format(version.locations.all())
        self.contracts = converter.contracts_download_format(version.contracts.all())
        self.datasources = converter.datasource_download_format(
            version.datasources.all()
        )

        self.investors = []
        self.involvements = []
        if version.operating_company_id:
            (
                all_investors,
                all_involvements,
                edges,
                min_depth,
            ) = InvolvementNetwork().get_network(
                version.operating_company_id,
                depth=1,
                show_ventures=False,
            )

            self.investors = converter.investor_download_format(all_investors)
            self.involvements = converter.involvement_download_format(all_involvements)

        self.filename = f"deal_{deal_id}"

    def _multiple_deals(self):
        dealhulls = DealHull.objects.visible(self.user, subset=self.subset).filter(
            parse_filters(self.request)
        )

        qs: QuerySet[DealVersion] = DealVersion.objects.filter(
            id__in=dealhulls.values_list("active_version_id", flat=True)
        ).order_by("deal_id")

        # Quality indicators
        if qi := self.request.GET.get("qi"):
            keys = [qi.key for qi in DEAL_QIS]

            try:
                qi_index = keys.index(qi)
            except ValueError:
                return HttpResponseBadRequest("Invalid qi")

            query = DEAL_QIS[qi_index].query()

            serializer = QueryParamsSerializer(data=self.request.GET)
            serializer.is_valid(raise_exception=True)

            if serializer.validated_data["inverse"]:
                query = ~query

            qs = qs.annotate(counts=annotate_counts()).filter(query)

        self.deals = [converter.deal_download_format(d) for d in _deal_qs_to_values(qs)]

        self.locations = []
        for d in qs:
            self.locations += converter.location_download_format(d.locations.all())

        self.contracts = []
        for d in qs:
            self.contracts += converter.contracts_download_format(d.contracts.all())

        self.datasources = []
        for d in qs:
            self.datasources += converter.datasource_download_format(
                d.datasources.all()
            )

        self.investors = converter.investor_download_format(
            InvestorHull.objects.visible(self.user).order_by("id")
        )

        involvements = Involvement.objects.visible(self.user).order_by("id")
        self.involvements = converter.involvement_download_format(involvements)

        self.filename = "export"

    def get_response(self):
        if self.return_format == "xlsx":
            return self._xlsx()
        if self.return_format == "csv":
            return self._csv()
        return self._html()

    def _html(self):
        ctx = {
            "deal_headers": deal_headers,
            "deals": self.deals,
            "location_headers": location_headers,
            "locations": self.locations,
            "contract_headers": contract_headers,
            "contracts": self.contracts,
            "datasource_headers": datasource_headers,
            "datasources": self.datasources,
            "investor_headers": investor_headers,
            "investors": self.investors,
            "involvement_headers": involvement_headers,
            "involvements": self.involvements,
        }
        return render(self.request, "landmatrix/export_table.html", ctx)

    def _xlsx(self):
        response = HttpResponse(
            headers={
                "Content-Type": "application/ms-excel",
                "Content-Disposition": f"attachment; filename={self.filename}.xlsx",
            }
        )

        tabs = [
            {
                "title": "Deals",
                "headers": list(deal_headers),
                "items": self.deals,
            },
            {
                "title": "Locations",
                "headers": location_headers,
                "items": self.locations,
            },
            {
                "title": "Contract",
                "headers": contract_headers,
                "items": self.contracts,
            },
            {
                "title": "Data sources",
                "headers": datasource_headers,
                "items": self.datasources,
            },
            {
                "title": "Involvements",
                "headers": involvement_headers,
                "items": self.involvements,
            },
            {
                "title": "Investors",
                "headers": investor_headers,
                "items": self.investors,
            },
        ]

        wb = Workbook(write_only=True)

        for tab in tabs:
            ws = wb.create_sheet(title=tab["title"])
            ws.append(tab["headers"])

            for item in tab["items"]:
                cleaned_item = [
                    str(i).encode("unicode_escape").decode("utf-8") for i in item
                ]
                # from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE
                # cleaned_item = [ILLEGAL_CHARACTERS_RE.sub(r"", str(i)) for i in item]
                try:
                    ws.append(cleaned_item)
                except IllegalCharacterError:
                    print("This should not happen.")
                    continue

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

    def _csv(self):
        result = BytesIO()
        zip_file = zipfile.ZipFile(result, "w")

        # Deals CSV
        deals_data = [list(deal_headers)] + self.deals
        zip_file.writestr("deals.csv", self._csv_writer(deals_data))

        # Locations CSV
        zip_file.writestr(
            "locations.csv",
            self._csv_writer([location_headers] + self.locations),
        )
        # Contracts CSV
        zip_file.writestr(
            "contracts.csv",
            self._csv_writer([contract_headers] + self.contracts),
        )
        # Datasources CSV
        zip_file.writestr(
            "datasources.csv",
            self._csv_writer([datasource_headers] + self.datasources),
        )

        # Involvements CSV
        involvements_data = [involvement_headers] + self.involvements
        zip_file.writestr("involvements.csv", self._csv_writer(involvements_data))

        # Investors CSV
        investors_data = [investor_headers] + self.investors
        zip_file.writestr("investors.csv", self._csv_writer(investors_data))

        zip_file.close()

        return HttpResponse(
            result.getvalue(),
            headers={
                "Content-Type": "application/x-zip-compressed",
                "Content-Disposition": f"attachment; filename={self.filename}.zip",
            },
        )
