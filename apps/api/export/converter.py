from django.db import models
from django.db.models import Case, CharField, Func, QuerySet, Value, When
from django.db.models.functions import Concat

from apps.landmatrix.models import choices
from apps.landmatrix.models.country import Country
from apps.landmatrix.models.currency import Currency
from apps.landmatrix.models.fields import ChoiceArrayField, DecimalIntField
from apps.landmatrix.models.new import (
    Contract,
    DealDataSource,
    DealVersion,
    InvestorHull,
    Involvement,
    Location,
)

deal_fields = {
    "deal_id": "Deal ID",
    "is_public": "Is public",
    "transnational": "Deal scope",
    "deal_size": "Deal size",
    "deal__country": "Target country",
    "current_contract_size": "Current size under contract",
    "current_production_size": "Current size in operation (production)",
    "current_negotiation_status": "Current negotiation status",
    "current_implementation_status": "Current implementation status",
    "deal__fully_updated_at": "Fully updated",
    "top_investors": "Top parent companies",
    "intended_size": "Intended size (in ha)",  # TODO LATER 100% Compat hacks
    "contract_size": "Size under contract (leased or purchased area, in ha)",
    "production_size": "Size in operation (production, in ha)",
    "land_area_comment": "Comment on land area",
    "intention_of_investment": "Intention of investment",
    "intention_of_investment_comment": "Comment on intention of investment",
    "carbon_offset_project": "Carbon offset project",
    "carbon_offset_project_comment": "Comment on carbon offset project",
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
    "operating_company__active_version__investor_id": "Operating company: Investor ID",
    "operating_company__active_version__name": "Operating company: Name",
    "operating_company__active_version__country__name": "Operating company: Country of registration/origin",
    "operating_company__active_version__classification": "Operating company: Classification",
    "operating_company__active_version__homepage": "Operating company: Investor homepage",
    "operating_company__active_version__opencorporates": "Operating company: Opencorporates link",
    "operating_company__active_version__comment": "Operating company: Comment",
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
    "carbon_sequestration": "Carbon sequestration/offsetting",
    "carbon_sequestration_comment": "Comment on carbon sequestration/offsetting",
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
    "deal__confidential": "Not public",
    "deal__confidential_comment": "Comment on not public",
}

# TODO: @Kurt why i18n choices and not just use the db values?
_negotiation_status_choices = dict(choices.NEGOTIATION_STATUS_CHOICES) | {None: "None"}
_implementation_status_choices = dict(choices.IMPLEMENTATION_STATUS_CHOICES) | {
    None: "None"
}
_intention_of_investment_choices = dict(choices.INTENTION_OF_INVESTMENT_CHOICES) | {
    None: "None"
}
_classification_choices = dict(choices.INVESTOR_CLASSIFICATION_CHOICES)
_produce_choices = {
    "crops": dict(choices.CROPS_CHOICES),
    "contract_farming_crops": dict(choices.CROPS_CHOICES),
    "animals": dict(choices.ANIMALS_CHOICES),
    "contract_farming_animals": dict(choices.ANIMALS_CHOICES),
    "mineral_resources": dict(choices.MINERALS_CHOICES),
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


_mchoices = Choices()


def __flatten_date_current_value(data, field, fieldname) -> None:
    if not data.get(field):
        data[field] = ""
        return
    data[field] = "|".join(
        [
            "#".join(
                [
                    x["date"] or "",
                    "current" if x.get("current") else "",
                    (
                        x[fieldname]
                        if isinstance(x[fieldname], str)
                        else str(round(x[fieldname], 2))
                    ),
                ]
            )
            for x in data[field]
            if x.get(fieldname) is not None
        ]
    )


def __flatten_array_choices(data, field, choics) -> None:
    if not data.get(field):
        data[field] = ""
        return

    matches = []
    for x in data[field]:
        if choice := choics.get(x):
            matches += [str(choice)]
    data[field] = "|".join(matches)


def __bool_cast(data, field) -> None:
    if data.get(field) is None:
        return
    data[field] = "Yes" if data[field] else "No"


def deal_download_format(data: dict):
    for field in DealVersion._meta.get_fields(include_parents=False):
        if field.name not in data.keys():
            continue
        if isinstance(field, models.BooleanField):
            __bool_cast(data, field.name)
        elif isinstance(field, DecimalIntField):
            if data.get(field.name) is not None:
                data[field.name] = f"{data[field.name]:.2f}"
            else:
                data[field.name] = ""

        elif isinstance(field, models.CharField):
            if field.choices and data.get(field.name):
                data[field.name] = str(dict(field.choices).get(data[field.name]))
        elif isinstance(field, ChoiceArrayField):
            __flatten_array_choices(data, field.name, dict(field.base_field.choices))
        # else:
        #     ic(field)
        #     "nevermind"

    # special cases
    if "transnational" in data:
        data["transnational"] = "transnational" if data["transnational"] else "domestic"
    fully_updated_at = data["deal__fully_updated_at"]
    if fully_updated_at:
        data["deal__fully_updated_at"] = fully_updated_at.isoformat()
    __bool_cast(data, "deal__confidential")

    # flatten top investors
    data["top_investors"] = "|".join(
        [
            "#".join(
                [
                    ti["active_version"]
                    .get("name", "")
                    .replace("#", "")
                    .replace("\n", "")
                    .strip(),
                    str(ti["id"]),
                    ti["active_version"].get("country_name", "") or "",
                ]
            )
            for ti in sorted(data["top_investors"], key=lambda x: x["id"])
            if ti["id"]
        ]
    )

    # map operating company fields
    if oc := data["operating_company"]:
        data["operating_company__active_version__investor_id"] = oc["investor_id"]
        data["operating_company__active_version__name"] = oc["name"]

        data["operating_company__active_version__country__name"] = oc["country__name"]
        data["operating_company__active_version__classification"] = str(
            _classification_choices.get(oc["classification"], "")
        )

        data["operating_company__active_version__homepage"] = oc["homepage"]
        data["operating_company__active_version__opencorporates"] = oc["opencorporates"]
        data["operating_company__active_version__comment"] = oc["comment"]

    __flatten_date_current_value(data, "contract_size", "area")
    __flatten_date_current_value(data, "production_size", "area")

    data["intention_of_investment"] = "|".join(
        [
            "#".join(
                [
                    x["date"] or "",
                    "current" if x.get("current") else "",
                    str(x.get("area", "") or ""),
                    ", ".join(
                        str(_intention_of_investment_choices[y])
                        for y in x.get("choices", [])
                    ),
                ]
            )
            for x in data["intention_of_investment"]
            if x.get("choices") is not None
        ]
    )

    data["negotiation_status"] = "|".join(
        [
            "#".join(
                [
                    x["date"] or "",
                    "current" if x.get("current") else "",
                    str(_negotiation_status_choices[x.get("choice")]),
                ]
            )
            for x in data["negotiation_status"]
        ]
    )

    data["implementation_status"] = "|".join(
        [
            "#".join(
                [
                    x["date"] or "",
                    "current" if x.get("current") else "",
                    str(_implementation_status_choices[x.get("choice")]),
                ]
            )
            for x in data["implementation_status"]
        ]
    )

    if data.get("purchase_price_currency"):
        data["purchase_price_currency"] = _mchoices.get("currency")[
            data["purchase_price_currency"]
        ]

    if data.get("annual_leasing_fee_currency"):
        data["annual_leasing_fee_currency"] = _mchoices.get("currency")[
            data["annual_leasing_fee_currency"]
        ]

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

    if data.get("involved_actors"):
        data["involved_actors"] = "|".join(
            [
                "#".join(
                    [
                        x.get("name") or "",
                        (
                            str(dict(choices.ACTOR_CHOICES)[x["role"]])
                            if x.get("role")
                            else ""
                        ),
                    ]
                )
                for x in data["involved_actors"]
            ]
        )
    else:
        data["involved_actors"] = ""

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

    if data.get("name_of_community"):
        data["name_of_community"] = "".join(
            [f"{x}#" for x in data["name_of_community"]]
        )
    if data.get("name_of_indigenous_people"):
        data["name_of_indigenous_people"] = "".join(
            [f"{x}#" for x in data["name_of_indigenous_people"]]
        )

    for country in [
        "deal__country",
        "export_country1",
        "export_country2",
        "export_country3",
    ]:
        if data.get(country):
            data[country] = _mchoices.get("country")[data[country]]

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
                                    str(_produce_choices.get(produce_type).get(x, x))
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
                                    str(_produce_choices.get(produce_type).get(x, x))
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

    xx = [
        (
            ""
            if (field not in data or data[field] is None or data[field] == [])
            else data[field]
        )
        for field in deal_fields.keys()
    ]
    # ic(xx)
    return xx


def location_download_format(locations: QuerySet[Location]) -> list[list]:
    return [
        [
            x["nid"],
            x["dealversion__deal_id"],
            str(
                dict(choices.LOCATION_ACCURACY_CHOICES)[x["level_of_accuracy"]]
                if x["level_of_accuracy"]
                else ""
            ),
            x["name"],
            x["point_lat_lng"],
            x["facility_name"],
            x["description"],
            x["comment"],
        ]
        for x in locations.annotate(
            point_lat_lng=Case(
                When(point=None, then=Value("")),
                default=Concat(
                    Func("point", function="ST_Y"),
                    Value(","),
                    Func("point", function="ST_X"),
                    output_field=CharField(),
                ),
            )
        ).values(
            "nid",
            "dealversion__deal_id",
            "level_of_accuracy",
            "name",
            "point_lat_lng",
            "facility_name",
            "description",
            "comment",
        )
    ]


def contracts_download_format(contracts: QuerySet[Contract]):
    return [
        [
            x["nid"],
            x["dealversion__deal_id"],
            x["number"],
            x["date_or_empty"],
            x["expiration_date_or_empty"],
            x["agreement_duration"],
            x["comment"],
        ]
        for x in contracts.annotate(
            date_or_empty=Case(
                When(date=None, then=Value("")),
                default="date",
                output_field=CharField(),
            ),
            expiration_date_or_empty=Case(
                When(expiration_date=None, then=Value("")),
                default="expiration_date",
                output_field=CharField(),
            ),
        ).values(
            "nid",
            "dealversion__deal_id",
            "number",
            "date_or_empty",
            "expiration_date_or_empty",
            "agreement_duration",
            "comment",
        )
    ]


def datasource_download_format(datasources: QuerySet[DealDataSource]) -> list[list]:
    return [
        [
            x["nid"],
            x["dealversion__deal_id"],
            str(dict(choices.DATASOURCE_TYPE_CHOICES)[x["type"]] if x["type"] else ""),
            x["url"],
            x["public_file"],
            x["publication_title"],
            x["date_or_empty"],
            x["name"],
            x["company"],
            x["email"],
            x["phone"],
            x["open_land_contracts_id"],
            x["comment"],
        ]
        for x in datasources.annotate(
            date_or_empty=Case(
                When(date=None, then=Value("")),
                default="date",
                output_field=CharField(),
            )
        )
        .annotate(
            public_file=Case(
                When(file_not_public=False, then="file"),
                default=Value("-redacted-"),
                output_field=CharField(),
            )
        )
        .values(
            "nid",
            "dealversion__deal_id",
            "type",
            "url",
            "public_file",
            "publication_title",
            "date_or_empty",
            "name",
            "company",
            "email",
            "phone",
            "open_land_contracts_id",
            "comment",
        )
    ]


def investor_download_format(investors: QuerySet[InvestorHull]):
    ret = []
    for x in (
        investors.annotate(
            classification_or_empty=Case(
                When(active_version__classification=None, then=Value("")),
                default="active_version__classification",
                output_field=CharField(),
            )
        )
        .annotate(
            country_or_empty=Case(
                When(active_version__country__name=None, then=Value("")),
                default="active_version__country__name",
                output_field=CharField(),
            )
        )
        .values_list(
            "id",
            "active_version__name",
            "country_or_empty",
            "classification_or_empty",
            "active_version__homepage",
            "active_version__opencorporates",
            "active_version__comment",
        )
    ):
        x = list(x)
        x[3] = str(_classification_choices.get(x[3], ""))
        ret += [x]
    return ret


def involvement_download_format(involvements: QuerySet[Involvement]) -> list[list]:
    return [
        [
            x["id"],
            x["child_investor_id"],
            x["child_investor__active_version__name"],
            x["parent_investor_id"],
            x["parent_investor__active_version__name"],
            str(dict(choices.INVOLVEMENT_ROLE_CHOICES)[x["role"]] if x["role"] else ""),
            "|".join(
                [
                    str(dict(choices.INVESTMENT_TYPE_CHOICES)[y])
                    for y in x["investment_type"]
                    if y
                ]
            ),
            float(x["percentage"]) if x["percentage"] is not None else "",
            x["loans_amount"] if x["loans_amount"] is not None else "",
            x["loans_currency"] if x["loans_currency"] is not None else "",
            x["loans_date"] if x["loans_date"] is not None else "",
            x["comment"],
        ]
        for x in involvements.values(
            "id",
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
        )
    ]
