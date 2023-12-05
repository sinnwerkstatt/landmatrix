import json
import zipfile
from datetime import datetime
from io import BytesIO

import unicodecsv as csv
from openpyxl import Workbook
from openpyxl.utils.exceptions import IllegalCharacterError

from django.http import HttpResponse
from django.shortcuts import render

from apps.graphql.tools import parse_filters

# noinspection PyProtectedMember
from apps.landmatrix.models import choices
from apps.landmatrix.models.country import Country
from apps.landmatrix.models.currency import Currency
from apps.landmatrix.models.deal import Deal
from apps.landmatrix.models.investor import Investor, InvestorVentureInvolvement
from apps.landmatrix.utils import InvolvementNetwork
from apps.utils import arrayfield_choices_display, qs_values_to_dict

deal_fields = {
    "id": "Deal ID",
    "is_public": "Is public",
    "transnational": "Deal scope",
    "deal_size": "Deal size",
    "country": "Target country",
    "current_contract_size": "Current size under contract",
    "current_production_size": "Current size in operation (production)",
    "current_negotiation_status": "Current negotiation status",
    "current_implementation_status": "Current implementation status",
    "fully_updated_at": "Fully updated",
    "top_investors": "Top parent companies",
    "intended_size": "Intended size (in ha)",
    "contract_size": "Size under contract (leased or purchased area, in ha)",
    "production_size": "Size in operation (production, in ha)",
    "land_area_comment": "Comment on land area",
    "intention_of_investment": "Intention of investment",
    "intention_of_investment_comment": "Comment on intention of investment",
    "nature_of_deal": "Nature of the deal",
    "nature_of_deal_comment": "Comment on nature of the deal",
    "negotiation_status": "Negotiation status",
    "negotiation_status_comment": "Comment on negotiation status",
    "implementation_status": "Implementation status",
    "implementation_status_comment": "Comment on implementation status",
    "purchase_price": "Purchase price",
    "purchase_price_currency": "Purchase price currency",
    "purchase_price_type": "Purchase price area type",
    "purchase_price_area": "Purchase price area",
    "purchase_price_comment": "Comment on purchase price",
    "annual_leasing_fee": "Annual leasing fee",
    "annual_leasing_fee_currency": "Annual leasing fee currency",
    "annual_leasing_fee_type": "Annual leasing fee type",
    "annual_leasing_fee_area": "Annual leasing fee area",
    "annual_leasing_fee_comment": "Comment on leasing fees",
    "contract_farming": "Contract farming",
    "on_the_lease_state": "On leased / purchased",
    "on_the_lease": "On leased area/farmers/households",
    "off_the_lease_state": "Not on leased / purchased (out-grower)",
    "off_the_lease": "Not on leased area/farmers/households (out-grower)",
    "contract_farming_comment": "Comment on contract farming",
    "total_jobs_created": "Jobs created (total)",
    "total_jobs_planned": "Planned number of jobs (total)",
    "total_jobs_planned_employees": "Planned employees (total)",
    "total_jobs_planned_daily_workers": "Planned daily/seasonal workers (total)",
    "total_jobs_current": "Current total number of jobs/employees/ daily/seasonal workers",
    "total_jobs_created_comment": "Comment on jobs created (total)",
    "foreign_jobs_created": "Jobs created (foreign)",
    "foreign_jobs_planned": "Planned number of jobs (foreign)",
    "foreign_jobs_planned_employees": "Planned employees (foreign)",
    "foreign_jobs_planned_daily_workers": "Planned daily/seasonal workers (foreign)",
    "foreign_jobs_current": "Current foreign number of jobs/employees/ daily/seasonal workers",
    "foreign_jobs_created_comment": "Comment on jobs created (foreign)",
    "domestic_jobs_created": "Jobs created (domestic)",
    "domestic_jobs_planned": "Planned number of jobs (domestic)",
    "domestic_jobs_planned_employees": "Planned employees (domestic)",
    "domestic_jobs_planned_daily_workers": "Planned daily/seasonal workers (domestic)",
    "domestic_jobs_current": "Current domestic number of jobs/employees/ daily/seasonal workers",
    "domestic_jobs_created_comment": "Comment on jobs created (domestic)",
    "involved_actors": "Actors involved in the negotiation / admission process",
    "project_name": "Name of investment project",
    "investment_chain_comment": "Comment on investment chain",
    "operating_company__id": "Operating company: Investor ID",
    "operating_company__name": "Operating company: Name",
    "operating_company__country__name": "Operating company: Country of registration/origin",
    "operating_company__classification": "Operating company: Classification",
    "operating_company__homepage": "Operating company: Investor homepage",
    "operating_company__opencorporates": "Operating company: Opencorporates link",
    "operating_company__comment": "Operating company: Comment",
    "name_of_community": "Name of community",
    "name_of_indigenous_people": "Name of indigenous people",
    "people_affected_comment": "Comment on communities / indigenous peoples affected",
    "recognition_status": "Recognition status of community land tenure",
    "recognition_status_comment": "Comment on recognitions status of community land tenure",
    "community_consultation": "Community consultation",
    "community_consultation_comment": "Comment on consultation of local community",
    "community_reaction": "Community reaction",
    "community_reaction_comment": "Comment on community reaction",
    "land_conflicts": "Presence of land conflicts",
    "land_conflicts_comment": "Comment on presence of land conflicts",
    "displacement_of_people": "Displacement of people",
    "displaced_people": "Number of people actually displaced",
    "displaced_households": "Number of households actually displaced",
    "displaced_people_from_community_land": "Number of people displaced out of their community land",
    "displaced_people_within_community_land": "Number of people displaced staying on community land",
    "displaced_households_from_fields": 'Number of households displaced "only" from their agricultural fields',
    "displaced_people_on_completion": "Number of people facing displacement once project is fully implemented",
    "displacement_of_people_comment": "Comment on displacement of people",
    "negative_impacts": "Negative impacts for local communities",
    "negative_impacts_comment": "Comment on negative impacts for local communities",
    "promised_compensation": "Promised compensation (e.g. for damages or resettlements)",
    "received_compensation": "Received compensation (e.g. for damages or resettlements)",
    "promised_benefits": "Promised benefits for local communities",
    "promised_benefits_comment": "Comment on promised benefits for local communities",
    "materialized_benefits": "Materialized benefits for local communities",
    "materialized_benefits_comment": "Comment on materialized benefits for local communities",
    "presence_of_organizations": "Presence of organizations and actions taken (e.g. farmer organizations, NGOs, etc.)",
    "former_land_owner": "Former land owner",
    "former_land_owner_comment": "Comment on former land owner",
    "former_land_use": "Former land use",
    "former_land_use_comment": "Comment on former land use",
    "former_land_cover": "Former land cover",
    "former_land_cover_comment": "Comment on former land cover",
    "crops": "Crops area/yield/export",
    "crops_comment": "Comment on crops",
    "animals": "Livestock area/yield/export",
    "animals_comment": "Comment on livestock",
    "mineral_resources": "Mineral resources area/yield/export",
    "mineral_resources_comment": "Comment on mineral resources",
    "contract_farming_crops": "Contract farming crops",
    "contract_farming_crops_comment": "Comment on contract farming crops",
    "contract_farming_animals": "Contract farming livestock",
    "contract_farming_animals_comment": "Comment on contract farming livestock",
    "electricity_generation": "Electricity generation",
    "electricity_generation_comment": "Comment on electricity generation",
    "carbon_sequestration": "Carbon sequestration",
    "carbon_sequestration_comment": "Comment on carbon sequestration",
    "has_domestic_use": "Has domestic use",
    "domestic_use": "Domestic use",
    "has_export": "Has export",
    "export": "Export",
    "export_country1": "Country 1",
    "export_country1_ratio": "Country 1 ratio",
    "export_country2": "Country 2",
    "export_country2_ratio": "Country 2 ratio",
    "export_country3": "Country 3",
    "export_country3_ratio": "Country 3 ratio",
    "use_of_produce_comment": "Comment on use of produce",
    "in_country_processing": "In country processing of produce",
    "in_country_processing_comment": "Comment on in country processing of produce",
    "in_country_processing_facilities": "Processing facilities / production infrastructure of the project (e.g. oil mill, ethanol distillery, biomass power plant etc.)",
    "in_country_end_products": "In-country end products of the project",
    "water_extraction_envisaged": "Water extraction envisaged",
    "water_extraction_envisaged_comment": "Comment on water extraction envisaged",
    "source_of_water_extraction": "Source of water extraction",
    "source_of_water_extraction_comment": "Comment on source of water extraction",
    "how_much_do_investors_pay_comment": "Comment on how much do investors pay for water",
    "water_extraction_amount": "Water extraction amount",
    "water_extraction_amount_comment": "Comment on how much water is extracted",
    "use_of_irrigation_infrastructure": "Use of irrigation infrastructure",
    "use_of_irrigation_infrastructure_comment": "Comment on use of irrigation infrastructure",
    "water_footprint": "Water footprint of the investment project",
    "gender_related_information": "Comment on gender-related info",
    "overall_comment": "Overall comment",
    "confidential": "Not public",
    "confidential_comment": "Comment on not public",
}
location_fields = {
    "id": "ID",
    "deal_id": "Deal ID",
    "level_of_accuracy": "Spatial accuracy level",
    "name": "Location",
    "point": "Point",
    "facility_name": "Facility name",
    "description": "Location description",
    "comment": "Comment on location",
}
contract_fields = {
    "id": "ID",
    "deal_id": "Deal ID",
    "number": "Contract number",
    "date": "Contract date",
    "expiration_date": "Contract expiration date",
    "agreement_duration": "Duration of the agreement",
    "comment": "Comment on contract",
}
datasource_fields = {
    "id": "ID",
    "deal_id": "Deal ID",
    "type": "Data source type",
    "url": "URL",
    "file": "File",
    "publication_title": "Publication title",
    "date": "Date",
    "name": "Name",
    "company": "Organisation",
    "email": "Email",
    "phone": "Phone",
    "open_land_contracts_id": "Open Contracting ID",
    "comment": "Comment on data source",
}

negotiation_status_choices = {**dict(choices.NEGOTIATION_STATUS_CHOICES), None: "None"}
implementation_status_choices = {
    **dict(choices.IMPLEMENTATION_STATUS_CHOICES),
    None: "None",
}
intention_of_investment_choices = {**dict(choices.INTENTION_CHOICES), None: "None"}
produce_choices = {
    "crops": {k: v["name"] for k, v in choices.CROPS.items()},
    "contract_farming_crops": {k: v["name"] for k, v in choices.CROPS.items()},
    "animals": {k: v["name"] for k, v in choices.ANIMALS.items()},
    "contract_farming_animals": {k: v["name"] for k, v in choices.ANIMALS.items()},
    "mineral_resources": {k: v["name"] for k, v in choices.MINERALS.items()},
}


class Choices:
    """need to generate the choices on running, otherwise DB errors"""

    choices = {}

    def get(self, name):
        if not self.choices.get(name):
            if name == "currency":
                self.choices[name] = {
                    x.id: f"{x.name} ({x.symbol})" if x.symbol else x.name
                    for x in Currency.objects.all()
                }
            if name == "country":
                self.choices[name] = dict(Country.objects.values_list("id", "name"))
        return self.choices[name]


mchoices = Choices()

deal_fields_top_investor = []
for f in deal_fields.keys():
    if f == "top_investors":
        deal_fields_top_investor += [
            "top_investors__id",
            "top_investors__name",
            "top_investors__country__name",
        ]
    else:
        deal_fields_top_investor += [f]

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


def flatten_date_current_value(data, field, fieldname) -> None:
    if not data.get(field):
        data[field] = ""
        return
    data[field] = "|".join(
        [
            "#".join(
                [
                    str(x.get("date", "")),
                    "current" if x.get("current") else "",
                    x[fieldname]
                    if isinstance(x[fieldname], str)
                    else str(round(x[fieldname], 2)),
                ]
            )
            for x in data[field]
            if x.get(fieldname) is not None
        ]
    )


def flatten_array_choices(data, field, choics) -> None:
    if not data.get(field):
        data[field] = ""
        return

    matches = []
    for x in data[field]:
        if choice := choics.get(x):
            matches += [choice]
    data[field] = "|".join(matches)


def single_choice(data, field, choics) -> None:
    if not data.get(field):
        return
    data[field] = choics[data[field]]


def bool_cast(data, field) -> None:
    if data.get(field) is None:
        return
    data[field] = "Yes" if data[field] else "No"


class DataDownload:
    def __init__(self, request):
        self.request = request
        self.user = request.user
        deal_id = self.request.GET.get("deal_id")
        filters = self.request.GET.get("filters")
        self.subset = self.request.GET.get("subset", "PUBLIC")
        self.return_format = self.request.GET.get("format", "html")

        if deal_id:
            self._single_deal(deal_id)
        else:
            self._multiple_deals(filters)

    def _single_deal(self, deal_id):
        qs = Deal.objects.visible(self.user, self.subset).filter(id=deal_id)
        deal = qs[0]
        self.deals = [
            self.deal_download_format(qs_dict)
            for qs_dict in qs_values_to_dict(
                qs, deal_fields_top_investor, ["top_investors"]
            )
        ]

        [loc.update({"deal_id": deal_id}) for loc in deal.locations]
        self.locations = [self.location_download_format(x) for x in deal.locations]

        [d.update({"deal_id": deal_id}) for d in deal.contracts]
        self.contracts = [self.contracts_download_format(x) for x in deal.contracts]

        [d.update({"deal_id": deal_id}) for d in deal.datasources]
        self.datasources = [
            self.datasource_download_format(x) for x in deal.datasources
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
        qs = Deal.objects.visible(self.user, subset=self.subset).order_by("id")
        if filters:
            qs = qs.filter(parse_filters(json.loads(filters)))

        # deal_ids = qs.values_list("id", flat=True)

        self.deals = [
            self.deal_download_format(qs_dict)
            for qs_dict in qs_values_to_dict(
                qs, deal_fields_top_investor, ["top_investors"]
            )
        ]

        self.locations = []
        for d in qs:
            if d.locations:
                for loc in d.locations:
                    loc.update({"deal_id": d.id})
                    self.locations += [self.location_download_format(loc)]

        self.contracts = []
        for d in qs:
            if d.contracts:
                for con in d.contracts:
                    con.update({"deal_id": d.id})
                    self.contracts += [self.contracts_download_format(con)]

        self.datasources = []
        for d in qs:
            if d.datasources:
                for ds in d.datasources:
                    ds.update({"deal_id": d.id})
                    self.datasources += [self.datasource_download_format(ds)]

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
            "deal_headers": deal_fields.values(),
            "deals": self.deals,
            "location_headers": location_fields.values(),
            "locations": self.locations,
            "contract_headers": contract_fields.values(),
            "contracts": self.contracts,
            "datasource_headers": datasource_fields.values(),
            "datasources": self.datasources,
            "investor_headers": investor_headers,
            "investors": self.investors,
            "involvement_headers": involvement_headers,
            "involvements": self.involvements,
        }
        return render(self.request, "landmatrix/export_table.html", ctx)

    def xlsx(self):
        response = HttpResponse(
            headers={
                "Content-Type": "application/ms-excel",
                "Content-Disposition": f"attachment; filename={self.filename}.xlsx",
            }
        )
        wb = Workbook(write_only=True)
        # wb = Workbook()

        # Deals tab
        ws_deals = wb.create_sheet(title="Deals")
        ws_deals.append(list(deal_fields.values()))
        for item in self.deals:
            try:
                ws_deals.append(item)
            except IllegalCharacterError:  # pragma: no cover
                ws_deals.append(
                    [str(i).encode("unicode_escape").decode("utf-8") for i in item]
                )

        # # Locations tab
        ws = wb.create_sheet(title="Locations")
        ws.append(list(location_fields.values()))
        [ws.append(item) for item in self.locations]

        # # Contracts tab
        ws = wb.create_sheet(title="Contracts")
        ws.append(list(contract_fields.values()))
        [ws.append(item) for item in self.contracts]

        # # DataSources tab
        ws = wb.create_sheet(title="Data sources")
        ws.append(list(datasource_fields.values()))
        [ws.append(item) for item in self.datasources]

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
        deals_data = [list(deal_fields.values())] + self.deals
        zip_file.writestr("deals.csv", self._csv_writer(deals_data))

        # Locations CSV
        zip_file.writestr(
            "locations.csv",
            self._csv_writer([list(location_fields.values())] + self.locations),
        )
        # Contracts CSV
        zip_file.writestr(
            "contracts.csv",
            self._csv_writer([list(contract_fields.values())] + self.contracts),
        )
        # Datasources CSV
        zip_file.writestr(
            "datasources.csv",
            self._csv_writer([list(datasource_fields.values())] + self.datasources),
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

    @staticmethod
    def deal_download_format(data):
        bool_cast(data, "is_public")
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
                for ti in sorted(data["top_investors"], key=lambda x: x["id"])
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
                    dict(Investor.CLASSIFICATION_CHOICES).get(
                        data["operating_company"]["classification"], ""
                    )
                )

            data["operating_company__homepage"] = data["operating_company"]["homepage"]
            data["operating_company__opencorporates"] = data["operating_company"][
                "opencorporates"
            ]
            data["operating_company__comment"] = data["operating_company"]["comment"]

        data["deal_size"] = data.get("deal_size", 0.0)
        data["current_contract_size"] = data.get("current_contract_size", 0.0)
        data["current_production_size"] = data.get("current_production_size", 0.0)

        imp_stat = data.get("current_implementation_status")
        data["current_implementation_status"] = implementation_status_choices.get(
            imp_stat, imp_stat
        )

        neg_stat = data.get("current_negotiation_status")
        data["current_negotiation_status"] = negotiation_status_choices.get(
            neg_stat, neg_stat
        )

        fully_updated_at = data.get("fully_updated_at")
        if fully_updated_at:
            data["fully_updated_at"] = fully_updated_at.isoformat()

        flatten_date_current_value(data, "contract_size", "area")
        flatten_date_current_value(data, "production_size", "area")

        if data.get("intention_of_investment"):
            data["intention_of_investment"] = "|".join(
                [
                    "#".join(
                        [
                            str(x.get("date", "")),
                            "current" if x.get("current") else "",
                            str(x.get("area", "")),
                            ", ".join(
                                intention_of_investment_choices[y]
                                for y in x.get("choices", [])
                            ),
                        ]
                    )
                    for x in data["intention_of_investment"]
                    if x.get("choices") is not None
                ]
            )
        else:
            data["intention_of_investment"] = ""

        flatten_array_choices(
            data, "nature_of_deal", dict(choices.NATURE_OF_DEAL_CHOICES)
        )

        if data.get("negotiation_status"):
            data["negotiation_status"] = "|".join(
                [
                    "#".join(
                        [
                            str(x.get("date", "")),
                            "current" if x.get("current") else "",
                            negotiation_status_choices[x.get("choice")],
                        ]
                    )
                    for x in data["negotiation_status"]
                ]
            )
        else:
            data["negotiation_status"] = ""

        if data.get("implementation_status"):
            data["implementation_status"] = "|".join(
                [
                    "#".join(
                        [
                            str(x.get("date", "")),
                            "current" if x.get("current") else "",
                            implementation_status_choices[x.get("choice")],
                        ]
                    )
                    for x in data["implementation_status"]
                ]
            )
        else:
            data["implementation_status"] = ""

        if data.get("purchase_price"):
            data["purchase_price"] = int(data["purchase_price"])
        if data.get("purchase_price_currency"):
            data["purchase_price_currency"] = mchoices.get("currency")[
                data["purchase_price_currency"]
            ]
        if data.get("purchase_price_type"):
            data["purchase_price_type"] = dict(choices.HA_AREA_CHOICES)[
                data["purchase_price_type"]
            ]
        # if data.get("purchase_price_area"):
        #     data["purchase_price_area"] = data["purchase_price_area"]

        if data.get("annual_leasing_fee"):
            data["annual_leasing_fee"] = int(data["annual_leasing_fee"])
        if data.get("annual_leasing_fee_currency"):
            data["annual_leasing_fee_currency"] = mchoices.get("currency")[
                data["annual_leasing_fee_currency"]
            ]
        if data.get("annual_leasing_fee_type"):
            data["annual_leasing_fee_type"] = dict(choices.HA_AREA_CHOICES)[
                data["annual_leasing_fee_type"]
            ]
        # if data.get("annual_leasing_fee_area"):
        #     data["annual_leasing_fee_area"] = data["annual_leasing_fee_area"]

        bool_cast(data, "contract_farming")

        for xdings in [
            "total_jobs_current",
            "foreign_jobs_current",
            "domestic_jobs_current",
        ]:
            if data.get(xdings) is not None:
                data[xdings] = "|".join(
                    [
                        "#".join(
                            [
                                dat.get("date") or "",
                                "current" if dat.get("current") else "",
                                str(dat.get("jobs") or ""),
                                str(dat.get("employees") or ""),
                                str(dat.get("workers") or ""),
                            ]
                        )
                        for dat in data[xdings]
                    ]
                )

        flatten_array_choices(
            data, "recognition_status", dict(choices.RECOGNITION_STATUS_CHOICES)
        )
        single_choice(
            data,
            "community_consultation",
            dict(choices.COMMUNITY_CONSULTATION_CHOICES),
        )
        single_choice(
            data, "community_reaction", dict(choices.COMMUNITY_REACTION_CHOICES)
        )

        if data.get("involved_actors"):
            data["involved_actors"] = "|".join(
                [
                    "#".join(
                        [
                            x.get("name", "") or "",
                            dict(choices.ACTOR_MAP)[x["role"]] if x.get("role") else "",
                        ]
                    )
                    for x in data["involved_actors"]
                ]
            )
        else:
            data["involved_actors"] = ""

        bool_cast(data, "on_the_lease_state")
        bool_cast(data, "off_the_lease_state")

        for xdings in ["on_the_lease", "off_the_lease"]:
            if data.get(xdings) is not None:
                data[xdings] = "|".join(
                    [
                        "#".join(
                            [
                                dat.get("date") or "",
                                "current" if dat.get("current") else "",
                                str(dat.get("area") or ""),
                                str(dat.get("farmers") or ""),
                                str(dat.get("households") or ""),
                            ]
                        )
                        for dat in data[xdings]
                    ]
                )
        bool_cast(data, "total_jobs_created")
        bool_cast(data, "foreign_jobs_created")
        bool_cast(data, "domestic_jobs_created")

        if data.get("name_of_community"):
            data["name_of_community"] = "".join(
                [f"{x}#" for x in data["name_of_community"]]
            )
        if data.get("name_of_indigenous_people"):
            data["name_of_indigenous_people"] = "".join(
                [f"{x}#" for x in data["name_of_indigenous_people"]]
            )

        bool_cast(data, "land_conflicts")
        bool_cast(data, "displacement_of_people")

        flatten_array_choices(
            data, "negative_impacts", dict(choices.NEGATIVE_IMPACTS_CHOICES)
        )
        flatten_array_choices(data, "promised_benefits", dict(choices.BENEFITS_CHOICES))
        flatten_array_choices(
            data, "materialized_benefits", dict(choices.BENEFITS_CHOICES)
        )
        flatten_array_choices(
            data, "former_land_owner", dict(choices.FORMER_LAND_OWNER_CHOICES)
        )
        flatten_array_choices(
            data, "former_land_use", dict(choices.FORMER_LAND_USE_CHOICES)
        )
        flatten_array_choices(
            data, "former_land_cover", dict(choices.FORMER_LAND_COVER_CHOICES)
        )

        bool_cast(data, "has_domestic_use")
        bool_cast(data, "has_export")

        bool_cast(data, "in_country_processing")
        bool_cast(data, "water_extraction_envisaged")
        bool_cast(data, "use_of_irrigation_infrastructure")
        bool_cast(data, "fully_updated")
        bool_cast(data, "confidential")

        for country in [
            "country",
            "export_country1",
            "export_country2",
            "export_country3",
        ]:
            if data.get(country):
                data[country] = mchoices.get("country")[data[country]]

        # if (crops := data.get("crops")) is not None:
        #     data["crops_json"] = json.dumps(crops)

        for produce_type in ["crops", "animals", "mineral_resources"]:
            if data.get(produce_type) is not None:
                data[produce_type] = "|".join(
                    [
                        "#".join(
                            [
                                dat.get("date") or "",
                                "current" if dat.get("current") else "",
                                str(dat.get("area") or ""),
                                str(dat.get("yield") or ""),
                                str(dat.get("export") or ""),
                                ", ".join(
                                    [
                                        produce_choices.get(produce_type).get(x, x)
                                        for x in dat.get("choices", [])
                                    ]
                                ),
                            ]
                        )
                        for dat in data[produce_type]
                    ]
                )

        for produce_type in ["contract_farming_crops", "contract_farming_animals"]:
            if data.get(produce_type) is not None:
                data[produce_type] = "|".join(
                    [
                        "#".join(
                            [
                                dat.get("date") or "",
                                "current" if dat.get("current") else "",
                                str(dat.get("area", "")),
                                ", ".join(
                                    [
                                        produce_choices.get(produce_type).get(x, x)
                                        for x in dat.get("choices", [])
                                    ]
                                ),
                            ]
                        )
                        for dat in data[produce_type]
                    ]
                )

        if (eg := data.get("electricity_generation")) is not None:
            data["electricity_generation"] = "|".join(
                [
                    "#".join(
                        [
                            dat.get("date") or "",
                            "current" if dat.get("current") else "",
                            str(dat.get("area", "")),
                            ", ".join([str(x) for x in dat.get("choices", [])]),
                            str(dat.get("export", "")),
                            str(dat.get("windfarm_count", "")),
                            str(dat.get("current_capacity", "")),
                            str(dat.get("intended_capacity", "")),
                        ]
                    )
                    for dat in eg
                ]
            )

        if (cs := data.get("carbon_sequestration")) is not None:
            data["carbon_sequestration"] = "|".join(
                [
                    "#".join(
                        [
                            dat.get("date") or "",
                            "current" if dat.get("current") else "",
                            str(dat.get("area", "")),
                            ", ".join([str(x) for x in dat.get("choices", [])]),
                            str(dat.get("projected_lifetime_sequestration", "")),
                            str(dat.get("projected_annual_sequestration", "")),
                            str(dat.get("certification_standard", "")),
                            str(dat.get("certification_standard_name", "")),
                            str(dat.get("certification_standard_comment", "")),
                        ]
                    )
                    for dat in cs
                ]
            )

        flatten_array_choices(
            data, "source_of_water_extraction", dict(choices.WATER_SOURCE_CHOICES)
        )
        bool_cast(data, "use_of_irrigation_infrastructure")

        return [
            "" if field not in data else data[field] for field in deal_fields.keys()
        ]

    @staticmethod
    def location_download_format(data):
        if data.get("point"):
            data["point"] = f"{data['point']['lat']},{data['point']['lng']}"
        else:
            # See bug #601 -> point is {} or None
            data["point"] = ""
        if data.get("level_of_accuracy"):
            data["level_of_accuracy"] = choices.LOCATION_ACCURACY[
                data["level_of_accuracy"]
            ]
        return [
            "" if field not in data else data[field] for field in location_fields.keys()
        ]

    @staticmethod
    def contracts_download_format(data):
        if data.get("date"):
            try:
                data["date"] = datetime.strptime(
                    data.get("date", ""), "%Y-%m-%d"
                ).date()
            except ValueError:
                pass
        else:
            data["date"] = ""

        if data.get("expiration_date"):
            try:
                data["expiration_date"] = datetime.strptime(
                    data.get("expiration_date", ""), "%Y-%m-%d"
                ).date()
            except ValueError:
                pass
        else:
            data["expiration_date"] = ""

        return [
            "" if field not in data else data[field] for field in contract_fields.keys()
        ]

    @staticmethod
    def datasource_download_format(data):
        if data.get("type"):
            data["type"] = choices.DATASOURCE_TYPE_MAP[data["type"]]
        if data.get("date"):
            try:
                data["date"] = datetime.strptime(data.get("date"), "%Y-%m-%d").date()
            except ValueError:
                pass
        else:
            data["date"] = ""

        return [
            "" if field not in data else data[field]
            for field in datasource_fields.keys()
        ]

    @staticmethod
    def investor_download_format(data):
        if "country" in data:
            data["country__name"] = data["country"]["name"]

        row = []
        for field in investor_fields:
            if field not in data:
                # empty fields
                data[field] = ""
            elif field == "classification":
                data[field] = str(
                    dict(Investor.CLASSIFICATION_CHOICES).get(data[field], "")
                )

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
                    InvestorVentureInvolvement.INVESTMENT_TYPE_CHOICES,
                )
            )
        row = []
        for field in involvement_fields:
            if field not in data:
                # empty fields
                data[field] = ""
            elif field == "role":
                data[field] = str(
                    dict(InvestorVentureInvolvement.ROLE_CHOICES).get(data[field], "")
                )
            row.append(data[field])
        return row
