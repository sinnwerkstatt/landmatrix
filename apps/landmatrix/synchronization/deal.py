import json
import re

from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point
from geojson_rewind import rewind

from apps.landmatrix.models import Deal
from apps.landmatrix.models import (
    HistoricalActivity,
    HistoricalInvestorActivityInvolvement,
    Crop,
    Animal,
    Mineral,
)
from apps.landmatrix.models.country import Country
from apps.landmatrix.models.deal import DealWorkflowInfo, DealVersion
from apps.landmatrix.synchronization.helpers import MetaActivity, calculate_new_stati
from apps.landmatrix.synchronization.helpers import (
    _extras_to_json,
    _extras_to_list,
    set_current,
    _lease_logic,
    _jobs_merge,
)
from apps.landmatrix.synchronization.helpers import _to_nullbool, date_year_field

User = get_user_model()


def _parse_general(deal, attrs):
    deal.country_id = (
        int(attrs.get("target_country"))
        if attrs.get("target_country")
        else attrs.get("target_country")
    )
    deal.intended_size = (
        float(attrs.get("intended_size")) if attrs.get("intended_size") else None
    )
    deal.contract_size = _extras_to_json(
        attrs, "contract_size", val1name="area", expected_type=float
    )
    deal.production_size = _extras_to_json(
        attrs, "production_size", val1name="area", expected_type=float
    )
    deal.land_area_comment = attrs.get("tg_land_area_comment") or ""

    INTENTION_MAP = {
        # Agriculture
        "Biofuels": "BIOFUELS",
        "Food crops": "FOOD_CROPS",
        "Fodder": "FODDER",
        "Livestock": "LIVESTOCK",
        "Non-food agricultural commodities": "NON_FOOD_AGRICULTURE",
        "Agriculture unspecified": "AGRICULTURE_UNSPECIFIED",
        "Agriculture": "AGRICULTURE_UNSPECIFIED",
        # Forestry
        "Timber plantation": "TIMBER_PLANTATION",
        "Forest logging / management": "FOREST_LOGGING",
        "For carbon sequestration/REDD": "CARBON",
        "Forestry unspecified": "FORESTRY_UNSPECIFIED",
        "Forestry": "FORESTRY_UNSPECIFIED",
        "For wood and fibre": "FORESTRY_UNSPECIFIED",
        "For wood and fiber": "FORESTRY_UNSPECIFIED",
        # Other
        "Mining": "MINING",
        "Oil / Gas extraction": "OIL_GAS_EXTRACTION",
        "Tourism": "TOURISM",
        "Industry": "INDUSTRY",
        "Conservation": "CONVERSATION",
        "Land speculation": "LAND_SPECULATION",
        "Renewable Energy": "RENEWABLE_ENERGY",
        "Other": "OTHER",
    }
    deal.intention_of_investment = _extras_to_json(
        attrs,
        "intention",
        val1name="choices",
        val2name="area",
        fieldmap=INTENTION_MAP,
        multi_value=True,
        expected_type2=float,
    )
    deal.intention_of_investment_comment = attrs.get("tg_intention_comment") or ""
    NATURE_OF_DEAL_MAP = {
        None: None,
        "Outright Purchase": "OUTRIGHT_PURCHASE",
        "Outright purchase": "OUTRIGHT_PURCHASE",
        "Compra Directa": "OUTRIGHT_PURCHASE",
        "Compra directa": "OUTRIGHT_PURCHASE",
        "Lease": "LEASE",
        "Arrendamiento": "LEASE",
        "Concession": "CONCESSION",
        "Concesión": "CONCESSION",
        "Exploitation permit / license / concession (for mineral resources)": "EXPLOITATION_PERMIT",
        "Permiso de explotación/licencia/concesión (para recursos minerales)": "EXPLOITATION_PERMIT",
        "Exploitation permit / license / concession": "EXPLOITATION_PERMIT",
        "Resource exploitation license / concession": "EXPLOITATION_PERMIT",
        "Pure contract farming": "PURE_CONTRACT_FARMING",
    }
    deal.nature_of_deal = _extras_to_list(attrs, "nature", NATURE_OF_DEAL_MAP)
    deal.nature_of_deal_comment = attrs.get("tg_nature_comment") or ""

    NEG_STATUS_MAP = {
        "Expression of interest": "EXPRESSION_OF_INTEREST",
        "Under negotiation": "UNDER_NEGOTIATION",
        "Memorandum of understanding": "MEMORANDUM_OF_UNDERSTANDING",
        "Oral agreement": "ORAL_AGREEMENT",
        "Contract signed": "CONTRACT_SIGNED",
        "Negotiations failed": "NEGOTIATIONS_FAILED",
        "Contract canceled": "CONTRACT_CANCELED",
        "Contract cancelled": "CONTRACT_CANCELED",
        "Contract expired": "CONTRACT_EXPIRED",
        "Change of ownership": "CHANGE_OF_OWNERSHIP",
        "---------": None,
        "": None,
    }
    deal.negotiation_status = _extras_to_json(
        attrs, "negotiation_status", val1name="choice", fieldmap=NEG_STATUS_MAP
    )
    deal.negotiation_status_comment = attrs.get("tg_negotiation_status_comment") or ""

    IMP_STATUS_MAP = {
        "Project not started": "PROJECT_NOT_STARTED",
        "Startup phase (no production)": "STARTUP_PHASE",
        "In operation (production)": "IN_OPERATION",
        "Project abandoned": "PROJECT_ABANDONED",
    }
    deal.implementation_status = _extras_to_json(
        attrs, "implementation_status", val1name="choice", fieldmap=IMP_STATUS_MAP
    )
    deal.implementation_status_comment = (
        attrs.get("tg_implementation_status_comment") or ""
    )

    HA_AREA_MAP = {
        None: None,
        "per ha": "PER_HA",
        "par ha": "PER_HA",
        "for specified area": "PER_AREA",
        "por área específica": "PER_AREA",
    }
    deal.purchase_price = attrs.get("purchase_price")
    deal.purchase_price_currency_id = attrs.get("purchase_price_currency")
    deal.purchase_price_type = HA_AREA_MAP[attrs.get("purchase_price_type")]
    deal.purchase_price_area = attrs.get("purchase_price_area")
    deal.purchase_price_comment = (
        attrs.get("tg_purchase_price_comment")
        or attrs.get("purchase_price_comment")
        or ""
    )
    deal.annual_leasing_fee_comment = attrs.get("tg_leasing_fees_comment") or ""

    annual_leasing_fee = attrs.get("annual_leasing_fee")
    # NOTE Adding broken data to comment
    if annual_leasing_fee == "9 USD per year per ha":
        deal.annual_leasing_fee_comment += annual_leasing_fee
    else:
        deal.annual_leasing_fee = annual_leasing_fee
    annual_leasing_fee_currency = attrs.get("annual_leasing_fee_currency")
    if annual_leasing_fee_currency == "Uruguay Peso en Unidades Indexadas":
        annual_leasing_fee_currency = 154
    deal.annual_leasing_fee_currency_id = annual_leasing_fee_currency
    deal.annual_leasing_fee_type = HA_AREA_MAP[attrs.get("annual_leasing_fee_type")]
    deal.annual_leasing_fee_area = attrs.get("annual_leasing_fee_area")

    deal.contract_farming = _to_nullbool(attrs.get("contract_farming"))
    deal.on_the_lease_state = _to_nullbool(attrs.get("on_the_lease"))
    deal.off_the_lease_state = _to_nullbool(attrs.get("off_the_lease"))
    deal.on_the_lease = _lease_logic(attrs, "on")
    deal.off_the_lease = _lease_logic(attrs, "off")
    deal.contract_farming_comment = attrs.get("tg_contract_farming_comment") or ""


def _parse_employment(deal, attrs):
    deal.total_jobs_created = _to_nullbool(attrs.get("total_jobs_created"))
    deal.total_jobs_planned = attrs.get("total_jobs_planned")
    deal.total_jobs_planned_employees = attrs.get("total_jobs_planned_employees")
    deal.total_jobs_planned_daily_workers = attrs.get(
        "total_jobs_planned_daily_workers"
    )
    deal.total_jobs_current = _jobs_merge(attrs, "total")
    deal.total_jobs_created_comment = (
        attrs.get("tg_total_number_of_jobs_created_comment") or ""
    )

    deal.foreign_jobs_created = _to_nullbool(attrs.get("foreign_jobs_created"))
    deal.foreign_jobs_planned = attrs.get("foreign_jobs_planned")
    deal.foreign_jobs_planned_employees = attrs.get("foreign_jobs_planned_employees")
    deal.foreign_jobs_planned_daily_workers = attrs.get(
        "foreign_jobs_planned_daily_workers"
    )
    deal.foreign_jobs_current = _jobs_merge(attrs, "foreign")
    deal.foreign_jobs_created_comment = (
        attrs.get("tg_foreign_jobs_created_comment") or ""
    )

    deal.domestic_jobs_created = _to_nullbool(attrs.get("domestic_jobs_created"))
    deal.domestic_jobs_planned = attrs.get("domestic_jobs_planned")
    deal.domestic_jobs_planned_employees = attrs.get("domestic_jobs_planned_employees")
    deal.domestic_jobs_planned_daily_workers = attrs.get(
        "domestic_jobs_planned_daily_workers"
    )
    deal.domestic_jobs_current = _jobs_merge(attrs, "domestic")
    deal.domestic_jobs_created_comment = (
        attrs.get("tg_domestic_jobs_created_comment") or ""
    )


def _connect_investor_to_deal(deal: Deal, act_version: HistoricalActivity):
    involvements = HistoricalInvestorActivityInvolvement.objects.filter(
        fk_activity=act_version
    ).order_by("-id")
    if len(involvements) < 1:
        return
    deal.operating_company_id = involvements[0].fk_investor.investor_identifier


actors_map = {
    "Government / State institutions": "GOVERNMENT_OR_STATE_INSTITUTIONS",
    "Government / State institutions (government, ministries, departments, agencies etc.)": "GOVERNMENT_OR_STATE_INSTITUTIONS",
    "Traditional land-owners / communities": "TRADITIONAL_LAND_OWNERS_OR_COMMUNITIES",
    "Traditional local authority (e.g. Chiefdom council / Chiefs)": "TRADITIONAL_LOCAL_AUTHORITY",
    "Traditional local authority": "TRADITIONAL_LOCAL_AUTHORITY",
    "Broker": "BROKER",
    "Intermediary": "INTERMEDIARY",
    "Other (please specify)": "OTHER",
    "Other": "OTHER",
}


def _parse_investor_info(deal, attrs):
    # deal.operating_company see above "_connect_investor_to_deal"
    involved_actors = _extras_to_json(attrs, "actors", val1name="name", val2name="role")
    if involved_actors:
        for involved_actor in involved_actors:
            if involved_actor.get("role"):
                involved_actor["role"] = actors_map[involved_actor["role"]]
    deal.involved_actors = involved_actors

    deal.project_name = attrs.get("project_name") or ""
    deal.investment_chain_comment = (
        attrs.get("tg_operational_stakeholder_comment") or ""
    )


def _parse_local_communities(deal, attrs):
    deal.name_of_community = (
        attrs.get("name_of_community").split("#")
        if attrs.get("name_of_community")
        else None
    )
    deal.name_of_indigenous_people = (
        attrs.get("name_of_indigenous_people").split("#")
        if attrs.get("name_of_indigenous_people")
        else None
    )
    deal.people_affected_comment = attrs.get("tg_affected_comment") or ""

    RECOGNITION_STATUS_MAP = {
        "Indigenous Peoples traditional or customary rights recognized by government": "INDIGENOUS_RIGHTS_RECOGNIZED",
        "Derechos consuetudinarios o tradicionales de Pueblos Indígenas reconocidos por el gobierno": "INDIGENOUS_RIGHTS_RECOGNIZED",
        "Indigenous Peoples traditional or customary rights not recognized by government": "INDIGENOUS_RIGHTS_NOT_RECOGNIZED",
        "Derechos consuetudinarios o tradicionales de Pueblos Indígenas no reconocidos por el gobierno": "INDIGENOUS_RIGHTS_NOT_RECOGNIZED",
        "Community traditional or customary rights recognized by government": "COMMUNITY_RIGHTS_RECOGNIZED",
        "Derechos consuetudinarios o tradicionales de comunidad reconocidos por el gobierno": "COMMUNITY_RIGHTS_RECOGNIZED",
        "Community traditional or customary rights not recognized by government": "COMMUNITY_RIGHTS_NOT_RECOGNIZED",
    }

    deal.recognition_status = _extras_to_list(
        attrs, "recognition_status", RECOGNITION_STATUS_MAP
    )
    deal.recognition_status_comment = attrs.get("tg_recognition_status_comment") or ""

    COMMUNITY_CONSULTATION_MAP = {
        None: None,
        "Not consulted": "NOT_CONSULTED",
        "Sin consultar": "NOT_CONSULTED",
        "Limited consultation": "LIMITED_CONSULTATION",
        "Consulta limitada": "LIMITED_CONSULTATION",
        "Free prior and informed consent": "FPIC",
        "Free, Prior and Informed Consent (FPIC)": "FPIC",
        "Certified Free, Prior and Informed Consent (FPIC)": "FPIC",
        "Certificación de Consentimiento Libre, Previo e Informado (CLPI)": "FPIC",
        "Consentimiento Libre, Previo e Informado (CLPI)": "FPIC",
        "Other": "OTHER",
        "Otro": "OTHER",
    }
    deal.community_consultation = COMMUNITY_CONSULTATION_MAP[
        attrs.get("community_consultation")
    ]
    deal.community_consultation_comment = (
        attrs.get("tg_community_consultation_comment") or ""
    )

    COMMUNITY_REACTION_MAP = {
        "Consent": "CONSENT",
        "Consentimiento  ": "CONSENT",
        "Consentimiento": "CONSENT",
        "Consentement": "CONSENT",
        "Mixed reaction": "MIXED_REACTION",
        "Reacción mixta": "MIXED_REACTION",
        "Rejection": "REJECTION",
        "Rechazo": "REJECTION",
    }
    deal.community_reaction = (
        COMMUNITY_REACTION_MAP[attrs.get("community_reaction")]
        if attrs.get("community_reaction")
        else None
    )
    deal.community_reaction_comment = attrs.get("tg_community_reaction_comment") or ""
    deal.land_conflicts = _to_nullbool(attrs.get("land_conflicts"))
    deal.land_conflicts_comment = attrs.get("tg_land_conflicts_comment") or ""
    deal.displacement_of_people = _to_nullbool(attrs.get("displacement_of_people"))
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

    NEGATIVE_IMPACTS_MAP = {
        "Environmental degradation": "ENVIRONMENTAL_DEGRADATION",
        "Degradación ambiental": "ENVIRONMENTAL_DEGRADATION",
        "Socio-economic": "SOCIO_ECONOMIC",
        "Socio-económico": "SOCIO_ECONOMIC",
        "Cultural loss": "CULTURAL_LOSS",
        "Pérdida cultural": "CULTURAL_LOSS",
        "Eviction": "EVICTION",
        "Desalojo": "EVICTION",
        "Displacement": "DISPLACEMENT",
        "Desplazamiento": "DISPLACEMENT",
        "Violence": "VIOLENCE",
        "Violencia": "VIOLENCE",
        "Other": "OTHER",
        "Otro": "OTHER",
    }
    deal.negative_impacts = _extras_to_list(
        attrs, "negative_impacts", NEGATIVE_IMPACTS_MAP
    )
    deal.negative_impacts_comment = attrs.get("tg_negative_impacts_comment") or ""
    deal.promised_compensation = attrs.get("promised_compensation") or ""
    deal.received_compensation = attrs.get("received_compensation") or ""

    BENEFITS_MAP = {
        "Health": "HEALTH",
        "Salud": "HEALTH",
        "Santé": "HEALTH",
        "Education": "EDUCATION",
        "Educación": "EDUCATION",
        "Productive infrastructure (e.g. irrigation, tractors, machinery...)": "PRODUCTIVE_INFRASTRUCTURE",
        "Infraestructura productiva (ej. irrigación, tractores, maquinaria…)": "PRODUCTIVE_INFRASTRUCTURE",
        "Infrastructure de production (ex.\xa0: irrigation, tracteurs, machines, ...)": "PRODUCTIVE_INFRASTRUCTURE",
        "Productive infrastructure": "PRODUCTIVE_INFRASTRUCTURE",
        "Roads": "ROADS",
        "Carreteras": "ROADS",
        "Capacity Building": "CAPACITY_BUILDING",
        "Renforcement des capacités": "CAPACITY_BUILDING",
        "Desarrollo de Capacidades": "CAPACITY_BUILDING",
        "Financial Support": "FINANCIAL_SUPPORT",
        "Apoyo Económico": "FINANCIAL_SUPPORT",
        "Community shares in the investment project": "COMMUNITY_SHARES",
        "Participaciones de la comunidad en el proyecto de inversión": "COMMUNITY_SHARES",
        "Other": "OTHER",
        "Otro": "OTHER",
    }
    deal.promised_benefits = _extras_to_list(attrs, "promised_benefits", BENEFITS_MAP)
    deal.promised_benefits_comment = attrs.get("tg_promised_benefits_comment") or ""
    deal.materialized_benefits = _extras_to_list(
        attrs, "materialized_benefits", BENEFITS_MAP
    )
    deal.materialized_benefits_comment = (
        attrs.get("tg_materialized_benefits_comment") or ""
    )
    deal.presence_of_organizations = attrs.get("presence_of_organizations") or ""


def _parse_former_use(deal, attrs):
    FORMER_LAND_OWNER_MAP = {
        "State": "STATE",
        "Estado": "STATE",
        "Private (smallholders)": "PRIVATE_SMALLHOLDERS",
        "Privado (pequeños agricultures)": "PRIVATE_SMALLHOLDERS",
        "Private (large-scale farm)": "PRIVATE_LARGE_SCALE",
        "Privado  (agricultura a gran escala)": "PRIVATE_LARGE_SCALE",
        "Private (large-scale)": "PRIVATE_LARGE_SCALE",
        "Community": "COMMUNITY",
        "Comunidad": "COMMUNITY",
        "Communauté": "COMMUNITY",
        "Indigenous people": "INDIGENOUS_PEOPLE",
        "Other": "OTHER",
        "Otro": "OTHER",
    }
    deal.former_land_owner = _extras_to_list(attrs, "land_owner", FORMER_LAND_OWNER_MAP)
    deal.former_land_owner_comment = attrs.get("tg_land_owner_comment") or ""

    FORMER_LAND_USE_MAP = {
        "Commercial (large-scale) agriculture": "COMMERCIAL_AGRICULTURE",
        "Agricultura comercial (a gran escala)": "COMMERCIAL_AGRICULTURE",
        "Smallholder agriculture": "SMALLHOLDER_AGRICULTURE",
        "Agricultura minifundista": "SMALLHOLDER_AGRICULTURE",
        "Shifting cultivation": "SHIFTING_CULTIVATION",
        "Pastoralism": "PASTORALISM",
        "Pastoralismo": "PASTORALISM",
        "Hunting/Gathering": "HUNTING_GATHERING",
        "Caza/Recolección": "HUNTING_GATHERING",
        "Forestry": "FORESTRY",
        "Silvicultura": "FORESTRY",
        "Conservation": "CONSERVATION",
        "Conservación": "CONSERVATION",
        "Other": "OTHER",
        "Otro": "OTHER",
        "Autre": "OTHER",
    }
    deal.former_land_use = _extras_to_list(attrs, "land_use", FORMER_LAND_USE_MAP)
    deal.former_land_use_comment = attrs.get("tg_land_use_comment") or ""

    FORMER_LAND_COVER_MAP = {
        "Cropland": "CROPLAND",
        "Tierra de cultivo": "CROPLAND",
        "Forest land": "FOREST_LAND",
        "Bosques": "FOREST_LAND",
        "Pasture": "PASTURE",
        "Pastura": "PASTURE",
        "Shrub land/Grassland (Rangeland)": "RANGELAND",
        "Shrub land/Grassland": "RANGELAND",
        "Matorrales/Praderas (Pastizales)": "RANGELAND",
        "Marginal land": "MARGINAL_LAND",
        "Terres marginales": "MARGINAL_LAND",
        "Wetland": "WETLAND",
        "Other land (e.g. developed land – specify in comment field)": "OTHER_LAND",
        "Otras tierras (ej. terrenos urbanizados - especifíquese en el campo para comentarios)": "OTHER_LAND",
        "Other land": "OTHER_LAND",
    }
    deal.former_land_cover = _extras_to_list(attrs, "land_cover", FORMER_LAND_COVER_MAP)
    deal.former_land_cover_comment = attrs.get("tg_land_cover_comment") or ""


def _merge_area_yield_export(attrs, name, fieldmap):
    areas = (
        _extras_to_json(
            attrs,
            name,
            val1name="choices",
            val2name="area",
            fieldmap=fieldmap,
            multi_value=True,
            expected_type2=float,
        )
        or []
    )
    yyields = (
        _extras_to_json(
            attrs,
            f"{name}_yield",
            val1name="choices",
            val2name="yield",
            fieldmap=fieldmap,
            multi_value=True,
            expected_type2=float,
        )
        or []
    )

    exports = (
        _extras_to_json(
            attrs,
            f"{name}_export",
            val1name="choices",
            val2name="export",
            fieldmap=fieldmap,
            multi_value=True,
            expected_type2=float,
        )
        or []
    )
    for yyield in yyields:
        if not yyield.get("choices"):
            continue
        abgehandelt = False
        for area in areas:
            is_subset = set(yyield["choices"]).issubset(area.get("choices"))
            if is_subset and yyield.get("date") == area.get("date"):
                abgehandelt = True
                if yyield.get("yield"):
                    area["yield"] = yyield["yield"]
        if not abgehandelt:
            areas += [yyield]
    for export in exports:
        if not export.get("choices"):
            continue
        abgehandelt = False
        for area in areas:
            is_subset = set(export["choices"]).issubset(area.get("choices"))
            if is_subset and export.get("date") == area.get("date"):
                abgehandelt = True
                if export.get("export"):
                    area["export"] = export["export"]
        if not abgehandelt:
            areas += [export]
    if areas:
        set_current(areas)
    return areas


def _parse_produce_info(deal, attrs):
    CROP_MAP = dict(
        [(str(x[0]), x[1]) for x in Crop.objects.all().values_list("id", "code")]
    )
    CROP_MAP["67"] = "67"
    CROP_MAP["35"] = "35"
    ANIMAL_MAP = dict(
        [(str(x[0]), x[1]) for x in Animal.objects.all().values_list("id", "code")]
    )
    ANIMAL_MAP["Aquaculture (animals)"] = "AQU"
    ANIMAL_MAP["1"] = "1"
    ANIMAL_MAP["5"] = "5"
    ANIMAL_MAP["6"] = "6"
    MINERAL_MAP = {str(x): str(x) for x in range(101)}
    MINERAL_MAP.update(
        dict(
            [(str(x[0]), x[1]) for x in Mineral.objects.all().values_list("id", "code")]
        )
    )
    deal.crops = _merge_area_yield_export(attrs, "crops", CROP_MAP)
    deal.crops_comment = attrs.get("tg_crops_comment") or ""
    deal.animals = _merge_area_yield_export(attrs, "animals", ANIMAL_MAP)
    deal.animals_comment = attrs.get("tg_animals_comment") or ""
    deal.mineral_resources = _merge_area_yield_export(attrs, "minerals", MINERAL_MAP)
    deal.mineral_resources_comment = attrs.get("tg_minerals_comment") or ""

    deal.contract_farming_crops = _extras_to_json(
        attrs,
        "contract_farming_crops",
        val1name="choices",
        val2name="area",
        fieldmap=CROP_MAP,
        multi_value=True,
        expected_type2=float,
    )

    deal.contract_farming_crops_comment = (
        attrs.get("tg_contract_farming_crops_comment") or ""
    )
    deal.contract_farming_animals = _extras_to_json(
        attrs,
        "contract_farming_animals",
        val1name="choices",
        val2name="area",
        fieldmap=ANIMAL_MAP,
        multi_value=True,
        expected_type2=float,
    )
    deal.contract_farming_animals_comment = (
        attrs.get("tg_contract_farming_animals_comment") or ""
    )

    deal.has_domestic_use = _to_nullbool(attrs.get("has_domestic_use"))

    # NOTE Fixes for broken data
    domestic_use = attrs.get("domestic_use")
    broken_domestic_use = {"20%": 20, "over 70% of the production will be exported": 30}
    try:
        domestic_use = broken_domestic_use[domestic_use]
    except KeyError:
        pass
    deal.domestic_use = domestic_use

    deal.has_export = _to_nullbool(attrs.get("has_export"))
    deal.export = attrs.get("export")

    export_country1 = attrs.get("export_country1")
    export_country2 = attrs.get("export_country2")
    export_country3 = attrs.get("export_country3")

    # NOTE Fixes for broken data
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
    else:
        deal.export_country1 = None
    deal.export_country1_ratio = attrs.get("export_country1_ratio")
    if export_country2:
        try:
            deal.export_country2 = Country.objects.get(name=export_country2)
        except Country.DoesNotExist:
            deal.export_country2 = Country.objects.get(id=export_country2)
    else:
        deal.export_country2 = None
    deal.export_country2_ratio = attrs.get("export_country2_ratio")
    if export_country3:
        try:
            deal.export_country3 = Country.objects.get(name=export_country3)
        except Country.DoesNotExist:
            deal.export_country3 = Country.objects.get(id=export_country3)
    else:
        deal.export_country3 = None
    deal.export_country3_ratio = attrs.get("export_country3_ratio")
    deal.use_of_produce_comment = attrs.get("tg_use_of_produce_comment") or ""
    deal.in_country_processing = _to_nullbool(attrs.get("in_country_processing"))
    deal.in_country_processing_comment = (
        attrs.get("tg_in_country_processing_comment") or ""
    )
    deal.in_country_processing_facilities = attrs.get("processing_facilities") or ""
    deal.in_country_end_products = attrs.get("in_country_end_products") or ""


def _parse_water(deal, attrs):
    WATER_SOURCE_MAP = {
        "Groundwater": "GROUNDWATER",
        "Aguas subterráneas": "GROUNDWATER",
        "Surface water": "SURFACE_WATER",
        "Aguas superficiales": "SURFACE_WATER",
        "River": "RIVER",
        "Río": "RIVER",
        "Lake": "LAKE",
    }

    deal.water_extraction_envisaged = _to_nullbool(
        attrs.get("water_extraction_envisaged")
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

    # NOTE Fixes for broken data
    water_extraction_amount = attrs.get("water_extraction_amount")
    water_extraction_amount_comment = (
        attrs.get("tg_water_extraction_amount_comment") or ""
    )
    broken_water_ex_amounts = {
        "150 billion litres": 150_000_000,  # billion / 1000 for m3 instead of litres
        "75m m3/year": 75_000_000,
        "1 cubic meter of water per second to process one ton of gold. In 15-25 years between 9.5 and 23 billion cubic meters of water can be captured": 31_540_000,
        "108bn gal/yr": 408_800_000,
        "3.07": 96_820,
        "23 549": 23_549,
        "40Millions de m3/mois": 40_000_000 * 12,
    }
    try:
        water_extraction_amount = broken_water_ex_amounts[water_extraction_amount]
    except KeyError:
        pass

    try:
        deal.water_extraction_amount = (
            float(water_extraction_amount) if water_extraction_amount else None
        )
    except ValueError:
        deal.water_extraction_amount = None
        water_extraction_amount_comment += (
            f"\n\nwater_extraction_amount={water_extraction_amount}"
        )
    deal.water_extraction_amount_comment = water_extraction_amount_comment or ""

    deal.use_of_irrigation_infrastructure = _to_nullbool(
        attrs.get("use_of_irrigation_infrastructure")
    )
    deal.use_of_irrigation_infrastructure_comment = (
        attrs.get("tg_use_of_irrigation_infrastructure_comment") or ""
    )
    deal.water_footprint = attrs.get("water_footprint") or ""


def _parse_remaining(deal, attrs):
    YPN_MAP = {v: k for k, v in Deal.YPN_CHOICES}

    deal.gender_related_information = attrs.get("tg_gender_specific_info_comment") or ""
    deal.vggt_applied = (
        YPN_MAP[attrs.get("vggt_applied")] if attrs.get("vggt_applied") else None
    )
    deal.vggt_applied_comment = attrs.get("tg_vggt_applied_comment") or ""
    deal.prai_applied = (
        YPN_MAP[attrs.get("prai_applied")] if attrs.get("prai_applied") else None
    )
    deal.prai_applied_comment = attrs.get("tg_prai_applied_comment") or ""
    deal.overall_comment = attrs.get("tg_overall_comment") or ""

    # META!
    deal.confidential = attrs.get("not_public") == "True"
    CONFIDENTIAL_REASON_MAP = {
        None: None,
        "Temporary removal from PI after criticism": "TEMPORARY_REMOVAL",
        "Research in progress": "RESEARCH_IN_PROGRESS",
        "Investigación en marcha": "RESEARCH_IN_PROGRESS",
        "Land Observatory Import": "LAND_OBSERVATORY_IMPORT",
    }
    deal.confidential_reason = CONFIDENTIAL_REASON_MAP[attrs.get("not_public_reason")]
    deal.confidential_comment = attrs.get("tg_not_public_comment") or ""


def _create_locations(deal, groups):
    ACCURACY_MAP = {
        None: "",
        "Country": "COUNTRY",
        "País": "COUNTRY",
        "Administrative region": "ADMINISTRATIVE_REGION",
        "Región administrativa": "ADMINISTRATIVE_REGION",
        "Région administrative": "ADMINISTRATIVE_REGION",
        "Approximate location": "APPROXIMATE_LOCATION",
        "Ubicación aproximada": "APPROXIMATE_LOCATION",
        "Exact location": "EXACT_LOCATION",
        "Ubicación exacta": "EXACT_LOCATION",
        "Coordinates": "COORDINATES",
        "Coordenadas": "COORDINATES",
    }
    locations = []
    i = 0
    for group_id, attrs in sorted(groups.items()):
        i += 1
        location = {
            "id": i,
            "old_group_id": group_id,
            "name": attrs.get("location") or "",
            "description": attrs.get("location_description") or "",
            "comment": attrs.get("tg_location_comment") or "",
            "facility_name": attrs.get("facility_name") or "",
            "level_of_accuracy": ACCURACY_MAP[attrs.get("level_of_accuracy")],
        }

        # location.point

        plat = attrs.get("point_lat")
        plng = attrs.get("point_lon")
        if plng == "-3.0001328124999426666666cro":
            plng = "-3.00013281249994266"

        if plat and plng:
            try:
                point_lat = plat.replace(",", ".").replace(" ", "")
                point_lat = round(float(point_lat), 5)
            except ValueError:
                pass
            try:
                point_lon = plng.replace(",", ".").replace("°", "")
                point_lon = round(float(point_lon), 5)
            except ValueError:
                pass

            try:
                assert 90 >= point_lat >= -90
                assert 180 >= point_lon >= -180
                Point(point_lon, point_lat)
                location["point"] = {"lat": point_lat, "lng": point_lon}
            except:
                print(plat, plng)
                location["comment"] += (
                    f"\n\nWas unable to parse location.\n"
                    f"The values are: lat:{point_lat} lon:{point_lon}"
                )
                location["point"] = None
        else:
            location["point"] = None

        features = []
        contract_area = attrs.get("contract_area", "polygon")
        intended_area = attrs.get("intended_area", "polygon")
        production_area = attrs.get("production_area", "polygon")
        if contract_area:
            area_feature = {
                "type": "Feature",
                "geometry": (json.loads(contract_area.geojson)),
                "properties": {"type": "contract_area"},
            }
            features += [rewind(area_feature)]
        if intended_area:
            area_feature = {
                "type": "Feature",
                "geometry": (json.loads(intended_area.geojson)),
                "properties": {"type": "intended_area"},
            }
            features += [rewind(area_feature)]
        if production_area:
            area_feature = {
                "type": "Feature",
                "geometry": (json.loads(production_area.geojson)),
                "properties": {"type": "production_area"},
            }
            features += [rewind(area_feature)]

        location["areas"] = (
            {"type": "FeatureCollection", "features": features} if features else None
        )
        locations += [location]

    deal.locations = locations


def _create_contracts(deal, groups):
    # track former contracts, throw out the ones that still exist now, delete the rest
    # all_contracts = set(c.id for c in deal.contracts.all())
    contracts = []
    i = 0
    for group_id, attrs in sorted(groups.items()):
        i += 1
        contract = {
            "id": i,
            "old_group_id": group_id,
            "number": attrs.get("contract_number") or "",
            "comment": attrs.get("tg_contract_comment") or "",
        }
        cdate = attrs.get("contract_date")
        if cdate:
            if cdate == "2008-15-08":
                cdate = "2008-08-15"
            if cdate == "2011-19-05":
                cdate = "2011-05-19"
            if cdate == "2008-24-09":
                cdate = "2008-09-24"
            if cdate == "2007-15":
                cdate = "2007"
            if date_year_field(cdate):
                contract["date"] = cdate
            else:
                print(f"cdate = '{cdate}'")
                raise Exception("!!")
        else:
            contract["date"] = None
        expdate = attrs.get("contract_expiration_date")
        if expdate:
            if expdate == "2035-09-31":
                expdate = "2035-09-30"
            if expdate == "2057-15-08":
                expdate = "2057-08-15"
            if expdate == "2060-19-05":
                expdate = "2060-05-19"
            if expdate == "2057-24-09":
                expdate = "2057-09-24"
            if expdate == "2056-15":
                expdate = "2056"
            if date_year_field(expdate):
                contract["expiration_date"] = expdate
            else:
                print(f"expdate = '{expdate}'")
                raise Exception("!!")
        else:
            contract["expiration_date"] = None
        agreement_duration = attrs.get("agreement_duration")
        if agreement_duration == "99 years":
            agreement_duration = 99
        contract["agreement_duration"] = (
            int(agreement_duration) if agreement_duration else None
        )
        contracts += [contract]
    deal.contracts = contracts


def _create_data_sources(deal, groups):
    TYPE_MAP = {
        None: "",
        "Media report": "MEDIA_REPORT",
        "Informe de prensa": "MEDIA_REPORT",
        "Research Paper / Policy Report": "RESEARCH_PAPER_OR_POLICY_REPORT",
        "Articles scientifiques/rapports politiques": "RESEARCH_PAPER_OR_POLICY_REPORT",
        "Informe de Investigación/Informe de Políticas": "RESEARCH_PAPER_OR_POLICY_REPORT",
        "Government sources": "GOVERNMENT_SOURCES",
        "Gouvernements": "GOVERNMENT_SOURCES",
        "Fuentes gubernamentales": "GOVERNMENT_SOURCES",
        "Company sources": "COMPANY_SOURCES",
        "Entreprises": "COMPANY_SOURCES",
        "Fuentes empresariales": "COMPANY_SOURCES",
        "Contract": "CONTRACT",
        "Contract (contract farming agreement)": "CONTRACT_FARMING_AGREEMENT",
        "Personal information": "PERSONAL_INFORMATION",
        "Información personal": "PERSONAL_INFORMATION",
        "Crowdsourcing": "CROWDSOURCING",
        "Other (Please specify in comment field)": "OTHER",
        "Otro (por favor, especifique en el campo para comentarios)": "OTHER",
        "Other": "OTHER",
        "Otro": "OTHER",
    }
    i = 0
    datasources = []
    for group_id, attrs in sorted(groups.items()):
        i += 1
        url = attrs.get("url") or ""
        if url == "http%3A%2F%2Ffarmlandgrab.org%2F2510":
            # noinspection HttpUrlsUsage
            url = "http://farmlandgrab.org/2510"

        ds = {
            "id": i,
            "old_group_id": group_id,
            "type": TYPE_MAP[attrs.get("type")],
            "url": url,
            "file": f"uploads/{attrs.get('file')}" if attrs.get("file") else None,
            "file_not_public": attrs.get("file_not_public") == "True",
            "publication_title": attrs.get("publication_title") or "",
            "comment": attrs.get("tg_data_source_comment") or "",
            "name": attrs.get("name") or "",
            "company": attrs.get("company") or "",
            "email": attrs.get("email") or "",
            "phone": attrs.get("phone") or "",
            "includes_in_country_verified_information": _to_nullbool(
                attrs.get("includes_in_country_verified_information"),
            ),
            "open_land_contracts_id": attrs.get("open_land_contracts_id") or "",
        }

        ds_date = attrs.get("date")
        if ds_date:
            # NOTE Fixes for broken data
            if ":" in ds_date:
                ds_date = re.sub(
                    r"([0-9]{2}):([0-9]{2}):([0-9]{4})", r"\1.\2.\3", ds_date
                )
            broken_ds_dates = {
                "2019-18-02": "2019-02-18",
                "2014-29-09": "2014-09-29",
                "2017-02-29": "2017-02-28",
                "2018-11-31": "2018-11-30",
                "2019-28-05": "2019-05-28",
                "2019-04-31": "2019-04-30",
                "2018-17-04": "2018-04-17",
                "2020-15-11": "2020-11-15",
                "2017-17-01": "2017-01-17",
            }
            try:
                ds_date = broken_ds_dates[ds_date]
            except KeyError:
                pass

            if date_year_field(ds_date):
                ds["date"] = ds_date
            else:
                ds["comment"] += f"\n\nOld Date value: {ds_date}"
        else:
            ds["date"] = None
        datasources += [ds]
    deal.datasources = datasources


def histivity_to_deal(activity_pk: int = None, activity_identifier: int = None):
    if activity_pk and activity_identifier:
        raise AttributeError("just specify one")
    elif activity_pk:
        activity_versions = HistoricalActivity.objects.filter(pk=activity_pk)
        activity_identifier = activity_versions[0].activity_identifier
    elif activity_identifier:
        activity_versions = HistoricalActivity.objects.filter(
            activity_identifier=activity_identifier
        ).order_by("pk")
    else:
        raise AttributeError("specify activity_pk or activity_identifier")

    if not activity_versions:
        return

    for histivity in activity_versions:
        deal, created = Deal.objects.get_or_create(id=activity_identifier)

        meta_activity = MetaActivity(histivity)
        _create_locations(deal, meta_activity.loc_groups)
        _parse_general(deal, meta_activity.group_general)
        _create_contracts(deal, meta_activity.con_groups)
        _parse_employment(deal, meta_activity.group_employment)
        _connect_investor_to_deal(deal, histivity)
        _parse_investor_info(deal, meta_activity.group_investor_info)
        _create_data_sources(deal, meta_activity.ds_groups)
        _parse_local_communities(deal, meta_activity.group_local_communities)
        _parse_former_use(deal, meta_activity.group_former_use)
        _parse_produce_info(deal, meta_activity.group_produce_info)
        _parse_water(deal, meta_activity.group_water)
        _parse_remaining(deal, meta_activity.group_remaining)

        user = User.objects.filter(id=histivity.history_user_id).first()

        if created:
            deal.created_at = histivity.history_date
            deal.created_by = user
        deal.modified_at = histivity.history_date
        deal.modified_by = user
        deal.fully_updated = histivity.fully_updated
        if deal.fully_updated:
            deal.fully_updated_at = deal.modified_at

        new_status = histivity.fk_status_id

        do_save = deal.status == 1 or new_status in [2, 3, 4]

        old_draft_status = deal.draft_status
        deal.status, deal.draft_status = calculate_new_stati(deal, new_status)

        deal.recalculate_fields()

        deal_version = DealVersion.from_object(
            deal, created_at=histivity.history_date, created_by=user
        )
        deal.current_draft = deal_version

        if do_save:
            # save the actual model
            # if: there is not a current_model
            # or: there is a current model but it's a draft
            # or: the new status is Live, Updated or Deleted
            deal.save()
        else:
            Deal.objects.filter(pk=deal.pk).update(
                draft_status=deal.draft_status, current_draft=deal_version
            )

        assign_user = meta_activity.group_remaining.get("assign_to_user")
        assuser = User.objects.get(id=assign_user) if assign_user else None

        feedback_comment = (
            meta_activity.group_remaining.get("tg_feedback_comment") or ""
        )
        comment = f"{histivity.comment or ''}" + (
            f"\n\n{feedback_comment}" if feedback_comment else ""
        )

        DealWorkflowInfo.objects.create(
            from_user=user or User.objects.get(id=1),
            to_user=assuser,
            draft_status_before=old_draft_status,
            draft_status_after=deal.draft_status,
            timestamp=histivity.history_date,
            comment=comment,
            processed_by_receiver=True,
            deal=deal,
            deal_version=deal_version,
        )
