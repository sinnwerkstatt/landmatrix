from apps.greennewdeal.models import Deal
from apps.greennewdeal.models.country import Country
from apps.greennewdeal.synchronization.helpers import _extras_to_json, _extras_to_list
from apps.landmatrix.models import (
    HistoricalActivity,
    HistoricalInvestorActivityInvolvement,
)


def parse_general(deal, attrs):
    NATURE_OF_DEAL_MAP = {
        None: None,
        "Outright Purchase": 10,
        "Lease": 20,
        "Concession": 30,
        "Exploitation permit / license / concession (for mineral resources)": 40,
        "Exploitation permit / license / concession": 40,
        "Resource exploitation license / concession": 40,
        "Pure contract farming": 50,
    }
    HA_AREA_MAP = {None: None, "per ha": 10, "for specified area": 20}

    deal.target_country_id = attrs.get("target_country")
    if attrs.get("intended_size"):
        deal.intended_size = float(attrs.get("intended_size"))
    deal.contract_size = _extras_to_json(attrs, "contract_size", expected_type=float)
    deal.production_size = _extras_to_json(
        attrs, "production_size", expected_type=float
    )
    deal.land_area_comment = attrs.get("tg_land_area_comment") or ""

    deal.intention_of_investment = _extras_to_json(attrs, "intention", "size")
    deal.intention_of_investment_comment = attrs.get("tg_intention_comment") or ""

    deal.nature_of_deal = _extras_to_list(attrs, "nature", NATURE_OF_DEAL_MAP)
    deal.nature_of_deal_comment = attrs.get("tg_nature_comment") or ""

    NEG_STATUS_MAP = {
        "Expression of interest": 10,
        "Under negotiation": 11,
        "Memorandum of understanding": 12,
        "Oral agreement": 20,
        "Contract signed": 21,
        "Negotiations failed": 30,
        "Contract canceled": 31,
        "Contract cancelled": 31,
        "Contract expired": 32,
        "Change of ownership": 40,
    }
    deal.negotiation_status = _extras_to_json(
        attrs, "negotiation_status", fieldmap=NEG_STATUS_MAP
    )
    deal.negotiation_status_comment = attrs.get("tg_negotiation_status_comment") or ""

    IMP_STATUS_MAP = {
        "Project not started": 10,
        "Startup phase (no production)": 20,
        "In operation (production)": 30,
        "Project abandoned": 40,
    }
    deal.implementation_status = _extras_to_json(
        attrs, "implementation_status", fieldmap=IMP_STATUS_MAP
    )
    deal.implementation_status_comment = (
        attrs.get("tg_implementation_status_comment") or ""
    )

    deal.purchase_price = attrs.get("purchase_price")
    deal.purchase_price_currency_id = attrs.get("purchase_price_currency")
    deal.purchase_price_type = HA_AREA_MAP[attrs.get("purchase_price_type")]
    deal.purchase_price_area = attrs.get("purchase_price_area")
    deal.purchase_price_comment = attrs.get("tg_purchase_price_comment") or ""

    annual_leasing_fee = attrs.get("annual_leasing_fee")
    # FIXME Fixes for broken data
    if annual_leasing_fee == "9 USD per year per ha":
        annual_leasing_fee = 9
    deal.annual_leasing_fee = annual_leasing_fee
    annual_leasing_fee_currency = attrs.get("annual_leasing_fee_currency")
    if annual_leasing_fee_currency == "Uruguay Peso en Unidades Indexadas":
        annual_leasing_fee_currency = 154
    deal.annual_leasing_fee_currency_id = annual_leasing_fee_currency
    deal.annual_leasing_fee_type = HA_AREA_MAP[attrs.get("annual_leasing_fee_type")]
    deal.annual_leasing_fee_area = attrs.get("annual_leasing_fee_area")
    deal.annual_leasing_fees_comment = attrs.get("tg_leasing_fees_comment") or ""

    if attrs.get("contract_farming"):
        deal.contract_farming = attrs.get("contract_farming") == "Yes"
    deal.on_the_lease = attrs.get("on_the_lease") == "True"
    deal.on_the_lease_area = _extras_to_json(attrs, "on_the_lease_area")
    deal.on_the_lease_farmers = _extras_to_json(attrs, "on_the_lease_farmers")
    deal.on_the_lease_households = _extras_to_json(attrs, "on_the_lease_households")
    deal.off_the_lease = attrs.get("off_the_lease") == "True"
    deal.off_the_lease_area = _extras_to_json(attrs, "off_the_lease_area")
    deal.off_the_lease_farmers = _extras_to_json(attrs, "off_the_lease_farmers")
    deal.off_the_lease_households = _extras_to_json(attrs, "off_the_lease_households")
    deal.contract_farming_comment = attrs.get("tg_contract_farming_comment") or ""


def parse_employment(deal, attrs):
    deal.total_jobs_created = attrs.get("total_jobs_created") == "True"
    deal.total_jobs_planned = attrs.get("total_jobs_planned")
    deal.total_jobs_planned_employees = attrs.get("total_jobs_planned_employees")
    deal.total_jobs_planned_daily_workers = attrs.get(
        "total_jobs_planned_daily_workers"
    )
    deal.total_jobs_current = _extras_to_json(attrs, "total_jobs_current")
    deal.total_jobs_current_employees = _extras_to_json(
        attrs, "total_jobs_current_employees"
    )
    deal.total_jobs_current_daily_workers = _extras_to_json(
        attrs, "total_jobs_current_daily_workers"
    )
    deal.total_jobs_created_comment = (
        attrs.get("tg_total_number_of_jobs_created_comment") or ""
    )

    deal.foreign_jobs_created = attrs.get("foreign_jobs_created") == "True"
    deal.foreign_jobs_planned = attrs.get("foreign_jobs_planned")
    deal.foreign_jobs_planned_employees = attrs.get("foreign_jobs_planned_employees")
    deal.foreign_jobs_planned_daily_workers = attrs.get(
        "foreign_jobs_planned_daily_workers"
    )
    deal.foreign_jobs_current = _extras_to_json(attrs, "foreign_jobs_current")
    deal.foreign_jobs_current_employees = _extras_to_json(
        attrs, "foreign_jobs_current_employees"
    )
    deal.foreign_jobs_current_daily_workers = _extras_to_json(
        attrs, "foreign_jobs_current_daily_workers"
    )
    deal.foreign_jobs_created_comment = (
        attrs.get("tg_foreign_jobs_created_comment") or ""
    )

    deal.domestic_jobs_created = attrs.get("domestic_jobs_created") == "True"
    deal.domestic_jobs_planned = attrs.get("domestic_jobs_planned")
    deal.domestic_jobs_planned_employees = attrs.get("domestic_jobs_planned_employees")
    deal.domestic_jobs_planned_daily_workers = attrs.get(
        "domestic_jobs_planned_daily_workers"
    )
    deal.domestic_jobs_current = _extras_to_json(attrs, "domestic_jobs_current")
    deal.domestic_jobs_current_employees = _extras_to_json(
        attrs, "domestic_jobs_current_employees"
    )
    deal.domestic_jobs_current_daily_workers = _extras_to_json(
        attrs, "domestic_jobs_current_daily_workers"
    )
    deal.domestic_jobs_created_comment = (
        attrs.get("tg_domestic_jobs_created_comment") or ""
    )


def connect_investor_to_deal(deal: Deal, act_version: HistoricalActivity):
    involvements = HistoricalInvestorActivityInvolvement.objects.filter(
        fk_activity=act_version
    ).order_by("-id")
    if len(involvements) < 1:
        return
    deal.operating_company_id = involvements[0].fk_investor.investor_identifier


def parse_investor_info(deal, attrs):
    # deal.operating_company see above "_connect_investor_to_deal"
    deal.involved_actors = _extras_to_json(attrs, "actors", "role")
    deal.project_name = attrs.get("project_name") or ""
    deal.investment_chain_comment = (
        attrs.get("tg_operational_stakeholder_comment") or ""
    )


def parse_local_communities(deal, attrs):
    COMMUNITY_CONSULTATION_MAP = {
        None: None,
        "Not consulted": 10,
        "Limited consultation": 20,
        "Free prior and informed consent": 30,
        "Free, Prior and Informed Consent (FPIC)": 30,
        "Certified Free, Prior and Informed Consent (FPIC)": 30,
        "Other": 50,
    }
    RECOGNITION_STATUS_MAP = {v: k for k, v in Deal.RECOGNITION_STATUS_CHOICES}
    COMMUNITY_REACTION_MAP = {v: k for k, v in Deal.COMMUNITY_REACTION_CHOICES}
    NEGATIVE_IMPACTS_MAP = {v: k for k, v in Deal.NEGATIVE_IMPACTS_CHOICES}
    BENEFITS_MAP = {
        "Health": 10,
        "Education": 20,
        "Productive infrastructure (e.g. irrigation, tractors, machinery...)": 30,
        "Productive infrastructure": 30,
        "Roads": 40,
        "Capacity Building": 50,
        "Financial Support": 60,
        "Community shares in the investment project": 70,
        "Other": 80,
    }

    if attrs.get("name_of_community"):
        deal.name_of_community = attrs.get("name_of_community").split("#")
    if attrs.get("name_of_indigenous_people"):
        deal.name_of_indigenous_people = attrs.get("name_of_indigenous_people").split(
            "#"
        )
    deal.people_affected_comment = attrs.get("tg_affected_comment") or ""
    deal.recognition_status = _extras_to_list(
        attrs, "recognition_status", RECOGNITION_STATUS_MAP
    )
    deal.recognition_status_comment = attrs.get("tg_recognition_status_comment") or ""
    deal.community_consultation = COMMUNITY_CONSULTATION_MAP[
        attrs.get("community_consultation")
    ]
    deal.community_consultation_comment = (
        attrs.get("tg_community_consultation_comment") or ""
    )
    if attrs.get("community_reaction"):
        deal.community_reaction = COMMUNITY_REACTION_MAP[
            attrs.get("community_reaction")
        ]
    deal.community_reaction_comment = attrs.get("tg_community_reaction_comment") or ""
    if attrs.get("land_conflicts"):
        deal.land_conflicts = attrs.get("land_conflicts") == "Yes"
    deal.land_conflicts_comment = attrs.get("tg_land_conflicts_comment") or ""
    if attrs.get("displacement_of_people"):
        deal.displacement_of_people = attrs.get("displacement_of_people") == "Yes"
    deal.displaced_people = attrs.get("number_of_displaced_people")
    deal.displaced_households = attrs.get("number_of_displaced_households")
    deal.displaced_people_from_community_land = attrs.get(
        "number_of_people_displaced_from_community_land"
    )
    deal.displaced_people_within_community_land = attrs.get(
        "displaced_people_within_community_land"
    )
    deal.displaced_households_from_fields = attrs.get(
        "number_of_households_displaced_from_fields"
    )
    deal.displaced_people_on_completion = attrs.get(
        "number_of_people_displaced_on_completion"
    )
    deal.displacement_of_people_comment = (
        attrs.get("tg_number_of_displaced_people_comment") or ""
    )

    deal.negative_impacts = _extras_to_list(
        attrs, "negative_impacts", NEGATIVE_IMPACTS_MAP
    )
    deal.negative_impacts_comment = attrs.get("tg_negative_impacts_comment") or ""
    deal.promised_compensation = attrs.get("promised_compensation") or ""
    deal.received_compensation = attrs.get("received_compensation") or ""

    deal.promised_benefits = _extras_to_list(attrs, "promised_benefits", BENEFITS_MAP)
    deal.promised_benefits_comment = attrs.get("tg_promised_benefits_comment") or ""
    deal.materialized_benefits = _extras_to_list(
        attrs, "materialized_benefits", BENEFITS_MAP
    )
    deal.materialized_benefits_comment = (
        attrs.get("tg_materialized_benefits_comment") or ""
    )
    deal.presence_of_organizations = attrs.get("presence_of_organizations") or ""


def parse_former_use(deal, attrs):
    FORMER_LAND_OWNER_MAP = {
        "State": 10,
        "Private (smallholders)": 20,
        "Private (large-scale farm)": 30,
        "Private (large-scale)": 30,
        "Community": 40,
        "Indigenous people": 50,
        "Other": 60,
    }
    FORMER_LAND_USE_MAP = {v: k for k, v in Deal.FORMER_LAND_USE_CHOICES}
    FORMER_LAND_COVER_MAP = {
        "Cropland": 10,
        "Forest land": 20,
        "Pasture": 30,
        "Shrub land/Grassland (Rangeland)": 40,
        "Shrub land/Grassland": 40,
        "Marginal land": 50,
        "Wetland": 60,
        "Other land (e.g. developed land – specify in comment field)": 70,
        "Other land": 70,
    }

    deal.former_land_owner = _extras_to_list(attrs, "land_owner", FORMER_LAND_OWNER_MAP)
    deal.former_land_owner_comment = attrs.get("tg_land_owner_comment") or ""
    deal.former_land_use = _extras_to_list(attrs, "land_use", FORMER_LAND_USE_MAP)
    deal.former_land_use_comment = attrs.get("tg_land_use_comment") or ""
    deal.former_land_cover = _extras_to_list(attrs, "land_cover", FORMER_LAND_COVER_MAP)
    deal.former_land_cover_comment = attrs.get("tg_land_cover_comment") or ""


def parse_produce_info(deal, attrs):
    deal.crops = _extras_to_json(attrs, "crops", "hectares")
    deal.crops_yield = _extras_to_json(attrs, "crops_yield", "tons")
    deal.crops_export = _extras_to_json(attrs, "crops_export", "percent")
    deal.crops_comment = attrs.get("tg_crops_comment") or ""
    deal.animals = _extras_to_json(attrs, "animals", "hectares")
    deal.animals_yield = _extras_to_json(attrs, "animals_yield", "tons")
    deal.animals_export = _extras_to_json(attrs, "animals_export", "percent")
    deal.animals_comment = attrs.get("tg_animals_comment") or ""
    deal.resources = _extras_to_json(attrs, "minerals", "hectares")
    deal.resources_yield = _extras_to_json(attrs, "minerals_yield", "tons")
    deal.resources_export = _extras_to_json(attrs, "export", "percent")
    deal.resources_comment = attrs.get("tg_minerals_comment") or ""

    deal.contract_farming_crops = _extras_to_json(
        attrs, "contract_farming_crops", "hectares"
    )
    deal.contract_farming_crops_comment = (
        attrs.get("tg_contract_farming_crops_comment") or ""
    )
    deal.contract_farming_animals = _extras_to_json(
        attrs, "contract_farming_animals", "hectares"
    )
    deal.contract_farming_animals_comment = (
        attrs.get("tg_contract_farming_animals_comment") or ""
    )

    deal.has_domestic_use = attrs.get("has_domestic_use") == "True"

    # FIXME Fixes for broken data
    domestic_use = attrs.get("domestic_use")
    broken_domestic_use = {"20%": 20, "over 70% of the production will be exported": 30}
    try:
        domestic_use = broken_domestic_use[domestic_use]
    except KeyError:
        pass
    deal.domestic_use = domestic_use

    deal.has_export = attrs.get("has_export") == "True"

    export_country1 = attrs.get("export_country1")
    export_country2 = attrs.get("export_country2")
    export_country3 = attrs.get("export_country3")

    # FIXME Fixes for broken data
    broken_countries = {
        "Democratic People's Republic of Korea": "Korea, Dem. People's Rep.",
        "Democratic Republic of the Congo": "Congo, Dem. Rep.",
        "Egypt": "Egypt, Arab Rep.",
        "Iran (Islamic Republic of)": "Iran, Islamic Rep.",
        "United Republic of Tanzania": "Tanzania",
        "Viet Nam": "Vietnam",
        "Yemen": "Yemen, Rep.",
    }

    try:
        export_country1 = broken_countries[export_country1]
    except KeyError:
        pass
    try:
        export_country2 = broken_countries[export_country2]
    except KeyError:
        pass
    try:
        export_country3 = broken_countries[export_country3]
    except KeyError:
        pass

    if export_country1:
        try:
            deal.export_country1 = Country.objects.get(name=export_country1)
        except Country.DoesNotExist:
            deal.export_country1 = Country.objects.get(id=export_country1)
    deal.export_country1_ratio = attrs.get("export_country1_ratio")
    if export_country2:
        try:
            deal.export_country2 = Country.objects.get(name=export_country2)
        except Country.DoesNotExist:
            deal.export_country2 = Country.objects.get(id=export_country2)
    deal.export_country2_ratio = attrs.get("export_country2_ratio")
    if export_country3:
        try:
            deal.export_country3 = Country.objects.get(name=export_country3)
        except Country.DoesNotExist:
            deal.export_country3 = Country.objects.get(id=export_country3)
    deal.export_country3_ratio = attrs.get("export_country3_ratio")
    deal.use_of_produce_comment = attrs.get("tg_use_of_produce_comment") or ""
    if attrs.get("in_country_processing"):
        deal.in_country_processing = attrs.get("in_country_processing") == "Yes"
    deal.in_country_processing_comment = (
        attrs.get("tg_in_country_processing_comment") or ""
    )
    deal.in_country_processing_facilities = (
        attrs.get("in_country_processing_facilities") or ""
    )
    deal.in_country_end_products = attrs.get("in_country_end_products") or ""


def parse_water(deal, attrs):
    WATER_SOURCE_MAP = {v: k for k, v in Deal.WATER_SOURCE_CHOICES}

    if attrs.get("water_extraction_envisaged"):
        deal.water_extraction_envisaged = (
            attrs.get("water_extraction_envisaged") == "Yes"
        )
    deal.water_extraction_envisaged_comment = (
        attrs.get("tg_water_extraction_envisaged_comment") or ""
    )
    deal.source_of_water_extraction = _extras_to_list(
        attrs, "source_of_water_extraction", WATER_SOURCE_MAP
    )
    deal.source_of_water_extraction_comment = (
        attrs.get("tg_source_of_water_extraction_comment") or ""
    )
    deal.how_much_do_investors_pay_comment = (
        attrs.get("tg_how_much_do_investors_pay_comment") or ""
    )

    # FIXME Fixes for broken data
    water_extraction_amount = attrs.get("water_extraction_amount")
    water_extraction_amount_comment = attrs.get("tg_water_extraction_amount_comment")
    broken_water_ex_amounts = {
        "150 billion litres": 150_000_000,  # billion / 1000 for m3 instead of litres
        "75m m3/year": 75_000_000,
        "1 cubic meter of water per second to process one ton of gold. In 15-25 years between 9.5 and 23 billion cubic meters of water can be captured": 31_540_000,
        "108bn gal/yr": 408_800_000,
        "3.07": 96_820,
        "23 549": 23_549,
    }
    try:
        water_extraction_amount = broken_water_ex_amounts[water_extraction_amount]
    except KeyError:
        pass
    if water_extraction_amount == "80% of annual flow":
        water_extraction_amount = None
        water_extraction_amount_comment = "80% of annual flow"
    deal.water_extraction_amount = water_extraction_amount
    deal.water_extraction_amount_comment = water_extraction_amount_comment or ""

    if attrs.get("use_of_irrigation_infrastructure"):
        deal.use_of_irrigation_infrastructure = (
            attrs.get("use_of_irrigation_infrastructure") == "Yes"
        )
    deal.use_of_irrigation_infrastructure_comment = (
        attrs.get("tg_use_of_irrigation_infrastructure_comment") or ""
    )
    deal.water_footprint = attrs.get("water_footprint") or ""


def parse_remaining(deal, attrs):
    YPN_MAP = {v: k for k, v in Deal.YPN_CHOICES}

    deal.gender_related_information = attrs.get("tg_gender_specific_info_comment") or ""
    if attrs.get("vggt_applied"):
        deal.vggt_applied = YPN_MAP[attrs.get("vggt_applied")]
    deal.vggt_applied_comment = attrs.get("tg_vggt_applied_comment") or ""
    if attrs.get("prai_applied"):
        deal.prai_applied = YPN_MAP[attrs.get("prai_applied")]
    deal.prai_applied_comment = attrs.get("tg_prai_applied_comment") or ""
    deal.overall_comment = attrs.get("tg_overall_comment") or ""

    deal.fully_updated = attrs.get("fully_updated") == "True"
    deal.private = attrs.get("not_public") == "True"
    PRIVATE_REASON_MAP = {
        None: None,
        "Temporary removal from PI after criticism": 10,
        "Research in progress": 20,
        "Land Observatory Import": 30,
    }
    deal.private_reason = PRIVATE_REASON_MAP[attrs.get("not_public_reason")]
    deal.private_comment = attrs.get("tg_not_public_comment") or ""
