import sys
from enum import Enum

from django.db.models import TextChoices
from django.utils.functional import Promise
from django.utils.translation import gettext_lazy as _

# https://stackoverflow.com/questions/68814891
if sys.version_info < (3, 11):
    from typing_extensions import NotRequired, Type, TypedDict
else:
    from typing import NotRequired, Type, TypedDict


# TypeDict Functional API works, but use class syntax for consistency
class ValueLabelItem(TypedDict):
    value: str
    # QUESTION: Use Promise or str here?
    label: Promise
    group: NotRequired[str]


# TODO: Write test
def serialize_enum(enum: Type[TextChoices]) -> list[ValueLabelItem]:
    # return [{"value": x.value, "label": x.label} for x in enum]
    return [{"value": x[0], "label": x[1]} for x in enum.choices]


# https://docs.djangoproject.com/en/5.0/ref/models/fields/#enumeration-types
class IntentionOfInvestmentGroupEnum(TextChoices):
    AGRICULTURE = "AGRICULTURE", _("Agriculture")
    FORESTRY = "FORESTRY", _("Forestry")
    RENEWABLE_ENERGY = "RENEWABLE_ENERGY", _("Renewable energy power plants")
    OTHER = "OTHER", _("Other")


INTENTION_OF_INVESTMENT_GROUP_ITEMS = serialize_enum(IntentionOfInvestmentGroupEnum)
# INTENTION_OF_INVESTMENT_GROUP_CHOICES = IntentionOfInvestmentGroupEnum.choices

INTENTION_OF_INVESTMENT_ITEMS: list[ValueLabelItem] = [
    {
        "value": "BIOFUELS",
        "label": _("Biomass for biofuels"),
        "group": IntentionOfInvestmentGroupEnum.AGRICULTURE,
    },
    {
        "value": "BIOMASS_ENERGY_GENERATION",
        "label": _("Biomass for energy generation (agriculture)"),
        "group": IntentionOfInvestmentGroupEnum.AGRICULTURE,
    },
    {
        "value": "FODDER",
        "label": _("Fodder"),
        "group": IntentionOfInvestmentGroupEnum.AGRICULTURE,
    },
    {
        "value": "FOOD_CROPS",
        "label": _("Food crops"),
        "group": IntentionOfInvestmentGroupEnum.AGRICULTURE,
    },
    {
        "value": "LIVESTOCK",
        "label": _("Livestock"),
        "group": IntentionOfInvestmentGroupEnum.AGRICULTURE,
    },
    {
        "value": "NON_FOOD_AGRICULTURE",
        "label": _("Non-food agricultural commodities"),
        "group": IntentionOfInvestmentGroupEnum.AGRICULTURE,
    },
    {
        "value": "AGRICULTURE_UNSPECIFIED",
        "label": _("Agriculture unspecified"),
        "group": IntentionOfInvestmentGroupEnum.AGRICULTURE,
    },
    {
        "value": "BIOMASS_ENERGY_PRODUCTION",
        "label": _("Biomass for energy generation (forestry)"),
        "group": IntentionOfInvestmentGroupEnum.FORESTRY,
    },
    {
        "value": "CARBON",
        "label": _("For carbon sequestration/REDD"),
        "group": IntentionOfInvestmentGroupEnum.FORESTRY,
    },
    {
        "value": "FOREST_LOGGING",
        "label": _("Forest logging / management for wood and fiber"),
        "group": IntentionOfInvestmentGroupEnum.FORESTRY,
    },
    {
        "value": "TIMBER_PLANTATION",
        "label": _("Timber plantation for wood and fiber"),
        "group": IntentionOfInvestmentGroupEnum.FORESTRY,
    },
    {
        "value": "FORESTRY_UNSPECIFIED",
        "label": _("Forestry unspecified"),
        "group": IntentionOfInvestmentGroupEnum.FORESTRY,
    },
    {
        "value": "SOLAR_PARK",
        "label": _("Solar park"),
        "group": IntentionOfInvestmentGroupEnum.RENEWABLE_ENERGY,
    },
    {
        "value": "WIND_FARM",
        "label": _("Wind farm"),
        "group": IntentionOfInvestmentGroupEnum.RENEWABLE_ENERGY,
    },
    {
        "value": "RENEWABLE_ENERGY",
        "label": _("Renewable energy unspecified"),
        "group": IntentionOfInvestmentGroupEnum.RENEWABLE_ENERGY,
    },
    {
        "value": "CONVERSATION",
        "label": _("Conservation"),
        "group": IntentionOfInvestmentGroupEnum.OTHER,
    },
    {
        "value": "INDUSTRY",
        "label": _("Industry"),
        "group": IntentionOfInvestmentGroupEnum.OTHER,
    },
    {
        "value": "LAND_SPECULATION",
        "label": _("Land speculation"),
        "group": IntentionOfInvestmentGroupEnum.OTHER,
    },
    {
        "value": "MINING",
        "label": _("Mining"),
        "group": IntentionOfInvestmentGroupEnum.OTHER,
    },
    {
        "value": "OIL_GAS_EXTRACTION",
        "label": _("Oil / Gas extraction"),
        "group": IntentionOfInvestmentGroupEnum.OTHER,
    },
    {
        "value": "TOURISM",
        "label": _("Tourism"),
        "group": IntentionOfInvestmentGroupEnum.OTHER,
    },
    {
        "value": "OTHER",
        "label": _("Other"),
        "group": IntentionOfInvestmentGroupEnum.OTHER,
    },
]

INTENTION_OF_INVESTMENT_CHOICES = [
    (x["value"], x["label"]) for x in INTENTION_OF_INVESTMENT_ITEMS
]

IntentionOfInvestmentEnum = Enum(
    "IntentionOfInvestmentEnum",
    {x["value"]: x["value"] for x in INTENTION_OF_INVESTMENT_ITEMS},
)


class NatureOfDealEnum(TextChoices):
    OUTRIGHT_PURCHASE = "OUTRIGHT_PURCHASE", _("Outright purchase")
    LEASE = "LEASE", _("Lease")
    CONCESSION = "CONCESSION", _("Concession")
    EXPLOITATION_PERMIT = "EXPLOITATION_PERMIT", _(
        "Exploitation permit / license / concession (for mineral resources)"
    )
    PURE_CONTRACT_FARMING = "PURE_CONTRACT_FARMING", _("Pure contract farming")
    OTHER = "OTHER", _("Other")


NATURE_OF_DEAL_ITEMS = serialize_enum(NatureOfDealEnum)
NATURE_OF_DEAL_CHOICES = NatureOfDealEnum.choices


class NegotiationStatusGroupEnum(TextChoices):
    INTENDED = "INTENDED", _("Intended")
    CONCLUDED = "CONCLUDED", _("Concluded")
    FAILED = "FAILED", _("Failed")
    CONTRACT_EXPIRED = "CONTRACT_EXPIRED", _("Contract expired")


NEGOTIATION_STATUS_GROUP_ITEMS = serialize_enum(NegotiationStatusGroupEnum)
# NEGOTIATION_STATUS_GROUP_CHOICES = NegotiationStatusGroupEnum.choices

NEGOTIATION_STATUS_ITEMS: list[ValueLabelItem] = [
    {
        "value": "EXPRESSION_OF_INTEREST",
        "label": _("Intended (Expression of interest)"),
        "group": NegotiationStatusGroupEnum.INTENDED,
    },
    {
        "value": "UNDER_NEGOTIATION",
        "label": _("Intended (Under negotiation)"),
        "group": NegotiationStatusGroupEnum.INTENDED,
    },
    {
        "value": "MEMORANDUM_OF_UNDERSTANDING",
        "label": _("Intended (Memorandum of understanding)"),
        "group": NegotiationStatusGroupEnum.INTENDED,
    },
    {
        "value": "ORAL_AGREEMENT",
        "label": _("Concluded (Oral Agreement)"),
        "group": NegotiationStatusGroupEnum.CONCLUDED,
    },
    {
        "value": "CONTRACT_SIGNED",
        "label": _("Concluded (Contract signed)"),
        "group": NegotiationStatusGroupEnum.CONCLUDED,
    },
    {
        "value": "CHANGE_OF_OWNERSHIP",
        "label": _("Concluded (Change of ownership)"),
        "group": NegotiationStatusGroupEnum.CONCLUDED,
    },
    {
        "value": "NEGOTIATIONS_FAILED",
        "label": _("Failed (Negotiations failed)"),
        "group": NegotiationStatusGroupEnum.FAILED,
    },
    {
        "value": "CONTRACT_CANCELED",
        "label": _("Failed (Contract cancelled)"),
        "group": NegotiationStatusGroupEnum.FAILED,
    },
    {
        "value": "CONTRACT_EXPIRED",
        "label": _("Contract expired"),
        "group": NegotiationStatusGroupEnum.CONTRACT_EXPIRED,
    },
]
NEGOTIATION_STATUS_CHOICES = [
    (x["value"], x["label"]) for x in NEGOTIATION_STATUS_ITEMS
]
NegotiationStatusEnum = Enum(
    "NegotiationStatusEnum", {x["value"]: x["value"] for x in NEGOTIATION_STATUS_ITEMS}
)


class ImplementationStatusEnum(TextChoices):
    PROJECT_NOT_STARTED = "PROJECT_NOT_STARTED", _("Project not started")
    STARTUP_PHASE = "STARTUP_PHASE", _("Startup phase (no production)")
    IN_OPERATION = "IN_OPERATION", _("In operation (production)")
    PROJECT_ABANDONED = "PROJECT_ABANDONED", _("Project abandoned")


IMPLEMENTATION_STATUS_CHOICES = ImplementationStatusEnum.choices
IMPLEMENTATION_STATUS_ITEMS = serialize_enum(ImplementationStatusEnum)


class HaAreasEnum(TextChoices):
    PER_HA = "PER_HA", _("per ha")
    PER_AREA = "PER_AREA", _("for specified area")


HA_AREA_ITEMS = serialize_enum(HaAreasEnum)
HA_AREA_CHOICES = HaAreasEnum.choices


class RecognitionStatusEnum(TextChoices):
    INDIGENOUS_RIGHTS_RECOGNIZED = "INDIGENOUS_RIGHTS_RECOGNIZED", _(
        "Indigenous Peoples traditional or customary rights recognized by government"
    )
    INDIGENOUS_RIGHTS_NOT_RECOGNIZED = "INDIGENOUS_RIGHTS_NOT_RECOGNIZED", _(
        "Indigenous Peoples traditional or customary rights not recognized by government"
    )
    COMMUNITY_RIGHTS_RECOGNIZED = "COMMUNITY_RIGHTS_RECOGNIZED", _(
        "Community traditional or customary rights recognized by government"
    )
    COMMUNITY_RIGHTS_NOT_RECOGNIZED = "COMMUNITY_RIGHTS_NOT_RECOGNIZED", _(
        "Community traditional or customary rights not recognized by government"
    )


RECOGNITION_STATUS_ITEMS = serialize_enum(RecognitionStatusEnum)
RECOGNITION_STATUS_CHOICES = RecognitionStatusEnum.choices


class CommunityConsultationEnum(TextChoices):
    NOT_CONSULTED = "NOT_CONSULTED", _("Not consulted")
    LIMITED_CONSULTATION = "LIMITED_CONSULTATION", _("Limited consultation")
    FPIC = "FPIC", _("Free, Prior and Informed Consent (FPIC)")
    OTHER = "OTHER", _("Other")


COMMUNITY_CONSULTATION_ITEMS = serialize_enum(CommunityConsultationEnum)
COMMUNITY_CONSULTATION_CHOICES = CommunityConsultationEnum.choices


class CommunityReactionEnum(TextChoices):
    CONSENT = "CONSENT", _("Consent")
    MIXED_REACTION = "MIXED_REACTION", _("Mixed reaction")
    REJECTION = "REJECTION", _("Rejection")


COMMUNITY_REACTION_ITEMS = serialize_enum(CommunityReactionEnum)
COMMUNITY_REACTION_CHOICES = CommunityReactionEnum.choices


class NegativeImpactEnum(TextChoices):
    ENVIRONMENTAL_DEGRADATION = "ENVIRONMENTAL_DEGRADATION", _(
        "Environmental degradation"
    )
    SOCIO_ECONOMIC = "SOCIO_ECONOMIC", _("Socio-economic")
    CULTURAL_LOSS = "CULTURAL_LOSS", _("Cultural loss")
    EVICTION = "EVICTION", _("Eviction")
    DISPLACEMENT = "DISPLACEMENT", _("Displacement")
    VIOLENCE = "VIOLENCE", _("Violence")
    OTHER = "OTHER", _("Other")


NEGATIVE_IMPACTS_ITEMS = serialize_enum(NegativeImpactEnum)
NEGATIVE_IMPACTS_CHOICES = NegativeImpactEnum.choices


class BenefitsEnum(TextChoices):
    HEALTH = "HEALTH", _("Health")
    EDUCATION = "EDUCATION", _("Education")
    PRODUCTIVE_INFRASTRUCTURE = "PRODUCTIVE_INFRASTRUCTURE", _(
        "Productive infrastructure (e.g. irrigation, tractors, machinery...)"
    )
    ROADS = "ROADS", _("Roads")
    CAPACITY_BUILDING = "CAPACITY_BUILDING", _("Capacity building")
    FINANCIAL_SUPPORT = "FINANCIAL_SUPPORT", _("Financial support")
    COMMUNITY_SHARES = "COMMUNITY_SHARES", _(
        "Community shares in the investment project"
    )
    OTHER = "OTHER", _("Other")


BENEFITS_ITEMS = serialize_enum(BenefitsEnum)
BENEFITS_CHOICES = BenefitsEnum.choices


class FormerLandOwnerEnum(TextChoices):
    STATE = "STATE", _("State")
    PRIVATE_SMALLHOLDERS = "PRIVATE_SMALLHOLDERS", _("Private (smallholders)")
    PRIVATE_LARGE_SCALE = "PRIVATE_LARGE_SCALE", _("Private (large-scale farm)")
    COMMUNITY = "COMMUNITY", _("Community")
    INDIGENOUS_PEOPLE = "INDIGENOUS_PEOPLE", _("Indigenous people")
    OTHER = "OTHER", _("Other")


FORMER_LAND_OWNER_ITEMS = serialize_enum(FormerLandOwnerEnum)
FORMER_LAND_OWNER_CHOICES = FormerLandOwnerEnum.choices


class FormerLandUseEnum(TextChoices):
    COMMERCIAL_AGRICULTURE = "COMMERCIAL_AGRICULTURE", _(
        "Commercial (large-scale) agriculture"
    )
    SMALLHOLDER_AGRICULTURE = "SMALLHOLDER_AGRICULTURE", _("Smallholder agriculture")
    SHIFTING_CULTIVATION = "SHIFTING_CULTIVATION", _("Shifting cultivation")
    PASTORALISM = "PASTORALISM", _("Pastoralism")
    HUNTING_GATHERING = "HUNTING_GATHERING", _("Hunting/Gathering")
    FORESTRY = "FORESTRY", _("Forestry")
    CONSERVATION = "CONSERVATION", _("Conservation")
    OTHER = "OTHER", _("Other")


FORMER_LAND_USE_ITEMS = serialize_enum(FormerLandUseEnum)
FORMER_LAND_USE_CHOICES = FormerLandUseEnum.choices


class FormerLandCoverEnum(TextChoices):
    CROPLAND = "CROPLAND", _("Cropland")
    FOREST_LAND = "FOREST_LAND", _("Forest land")
    PASTURE = "PASTURE", _("Pasture")
    RANGELAND = "RANGELAND", _("Shrub land/Grassland (Rangeland)")
    MARGINAL_LAND = "MARGINAL_LAND", _("Marginal land")
    WETLAND = "WETLAND", _("Wetland")
    OTHER_LAND = "OTHER_LAND", _("Other land (e.g. developed land)")


FORMER_LAND_COVER_ITEMS = serialize_enum(FormerLandCoverEnum)
FORMER_LAND_COVER_CHOICES = FormerLandCoverEnum.choices


class ProduceGroupEnum(TextChoices):
    CROPS = "CROPS", _("Crops")
    ANIMALS = "ANIMALS", _("Livestock")
    MINERAL_RESOURCES = "MINERAL_RESOURCES", _("Mineral resources")


PRODUCE_GROUP_ITEMS = serialize_enum(ProduceGroupEnum)
# PRODUCE_GROUP_CHOICES = ProduceGroupEnum.choices

# FIXME: produce field not in use
CROPS_ITEMS: list[ValueLabelItem] = [
    {"value": "ACC", "label": _("Accacia"), "produce": "NON_FOOD"},
    {"value": "ALF", "label": _("Alfalfa"), "produce": "NON_FOOD"},
    {
        "value": "ALG",
        "label": _("Seaweed / Macroalgae(unspecified)"),
        "produce": "NON_FOOD",
    },
    {"value": "ALM", "label": _("Almond"), "produce": "FOOD_CROP"},
    {"value": "ALV", "label": _("Aloe Vera"), "produce": "NON_FOOD"},
    {"value": "APL", "label": _("Apple"), "produce": "FOOD_CROP"},
    {
        "value": "AQU",
        "label": _("Aquaculture (unspecified crops)"),
        "produce": "FOOD_CROP",
    },
    {"value": "BAM", "label": _("Bamboo"), "produce": "NON_FOOD"},
    {"value": "BAN", "label": _("Banana"), "produce": "FOOD_CROP"},
    {"value": "BEA", "label": _("Bean"), "produce": "FOOD_CROP"},
    {"value": "BOT", "label": _("Bottle Gourd"), "produce": "FOOD_CROP"},
    {"value": "BRL", "label": _("Barley"), "produce": "FOOD_CROP"},
    {"value": "BWT", "label": _("Buckwheat"), "produce": "FOOD_CROP"},
    {"value": "CAC", "label": _("Cacao"), "produce": "FOOD_CROP"},
    {"value": "CAS", "label": _("Cassava (Maniok)"), "produce": "FOOD_CROP"},
    {"value": "CAW", "label": _("Cashew"), "produce": "FOOD_CROP"},
    {"value": "CHA", "label": _("Chat")},
    {"value": "CHE", "label": _("Cherries"), "produce": "FOOD_CROP"},
    {"value": "CNL", "label": _("Canola"), "produce": "FLEX_CROP"},
    {"value": "COC", "label": _("Coconut"), "produce": "FOOD_CROP"},
    {"value": "COF", "label": _("Coffee Plant"), "produce": "FOOD_CROP"},
    {"value": "COT", "label": _("Cotton"), "produce": "NON_FOOD"},
    {"value": "CRL", "label": _("Cereals (unspecified)"), "produce": "FOOD_CROP"},
    {"value": "CRN", "label": _("Corn (Maize)"), "produce": "FOOD_CROP"},
    {"value": "CRO", "label": _("Croton"), "produce": "NON_FOOD"},
    {"value": "CST", "label": _("Castor Oil Plant"), "produce": "NON_FOOD"},
    {"value": "CTR", "label": _("Citrus Fruits (unspecified)"), "produce": "FOOD_CROP"},
    {"value": "DIL", "label": _("Dill"), "produce": "NON_FOOD"},
    {"value": "EUC", "label": _("Eucalyptus"), "produce": "NON_FOOD"},
    {"value": "FLW", "label": _("Flowers (unspecified)"), "produce": "NON_FOOD"},
    {"value": "FNT", "label": _("Fig-Nut"), "produce": "FOOD_CROP"},
    {"value": "FOD", "label": _("Fodder Plants (unspecified)"), "produce": "NON_FOOD"},
    {"value": "FOO", "label": _("Food crops (unspecified)"), "produce": "FOOD_CROP"},
    {"value": "FRT", "label": _("Fruit (unspecified)"), "produce": "FOOD_CROP"},
    {"value": "GRA", "label": _("Grapes"), "produce": "FOOD_CROP"},
    {"value": "GRN", "label": _("Grains (unspecified)"), "produce": "FOOD_CROP"},
    {"value": "HRB", "label": _("Herbs (unspecified)")},
    {"value": "JTR", "label": _("Jatropha"), "produce": "NON_FOOD"},
    {"value": "LNT", "label": _("Lentils"), "produce": "FOOD_CROP"},
    {"value": "MAN", "label": _("Mango"), "produce": "FOOD_CROP"},
    {"value": "MUS", "label": _("Mustard"), "produce": "FOOD_CROP"},
    {"value": "OAT", "label": _("Oats")},
    {"value": "OIL", "label": _("Oil Seeds (unspecified)"), "produce": "FLEX_CROP"},
    {"value": "OLE", "label": _("Oleagionous plant"), "produce": "FLEX_CROP"},
    {"value": "OLV", "label": _("Olives"), "produce": "FOOD_CROP"},
    {"value": "ONI", "label": _("Onion"), "produce": "FOOD_CROP"},
    {"value": "OPL", "label": _("Oil Palm"), "produce": "FLEX_CROP"},
    {"value": "OTH", "label": _("Other crops")},
    {"value": "PAL", "label": _("Palms"), "produce": "FOOD_CROP"},
    {"value": "PAP", "label": _("Papaya"), "produce": "FOOD_CROP"},
    {"value": "PAS", "label": _("Passion fruit"), "produce": "FOOD_CROP"},
    {"value": "PEA", "label": _("Peanut (groundnut)"), "produce": "FOOD_CROP"},
    {"value": "PEP", "label": _("Pepper"), "produce": "FOOD_CROP"},
    {"value": "PES", "label": _("Peas"), "produce": "FOOD_CROP"},
    {"value": "PIE", "label": _("Pine"), "produce": "FOOD_CROP"},
    {"value": "PIN", "label": _("Pineapple"), "produce": "FOOD_CROP"},
    {"value": "PLS", "label": _("Pulses (unspecified)"), "produce": "FOOD_CROP"},
    {"value": "POM", "label": _("Pomegranate"), "produce": "FOOD_CROP"},
    {"value": "PON", "label": _("Pongamia Pinnata"), "produce": "NON_FOOD"},
    {"value": "PTT", "label": _("Potatoes"), "produce": "FOOD_CROP"},
    {"value": "RAP", "label": _("Rapeseed"), "produce": "FOOD_CROP"},
    {"value": "RCH", "label": _("Rice (hybrid)"), "produce": "FOOD_CROP"},
    {"value": "RIC", "label": _("Rice"), "produce": "FOOD_CROP"},
    {"value": "ROS", "label": _("Roses"), "produce": "NON_FOOD"},
    {"value": "RUB", "label": _("Rubber tree"), "produce": "NON_FOOD"},
    {"value": "RYE", "label": _("Rye"), "produce": "FOOD_CROP"},
    {
        "value": "SEE",
        "label": _("Seeds Production (unspecified)"),
        "produce": "FOOD_CROP",
    },
    {"value": "SES", "label": _("Sesame"), "produce": "FOOD_CROP"},
    {"value": "SOR", "label": _("Sorghum"), "produce": "FOOD_CROP"},
    {"value": "SOY", "label": _("Soya Beans"), "produce": "FLEX_CROP"},
    {"value": "SPI", "label": _("Spices (unspecified)")},
    {"value": "SSL", "label": _("Sisal"), "produce": "NON_FOOD"},
    {"value": "SUB", "label": _("Sugar beet"), "produce": "FLEX_CROP"},
    {"value": "SUC", "label": _("Sugar Cane"), "produce": "FLEX_CROP"},
    {"value": "SUG", "label": _("Sugar (unspecified)"), "produce": "FLEX_CROP"},
    {"value": "SUN", "label": _("Sun Flower"), "produce": "FLEX_CROP"},
    {"value": "SWP", "label": _("Sweet Potatoes"), "produce": "FOOD_CROP"},
    {"value": "TBC", "label": _("Tobacco"), "produce": "NON_FOOD"},
    {"value": "TEA", "label": _("Tea"), "produce": "FOOD_CROP"},
    {"value": "TEF", "label": _("Teff"), "produce": "FOOD_CROP"},
    {"value": "TEK", "label": _("Teak"), "produce": "NON_FOOD"},
    {"value": "TOM", "label": _("Tomatoes"), "produce": "FOOD_CROP"},
    {"value": "TRE", "label": _("Trees (unspecified)"), "produce": "NON_FOOD"},
    {"value": "VGT", "label": _("Vegetables (unspecified)"), "produce": "FOOD_CROP"},
    {"value": "VIN", "label": _("Vineyard"), "produce": "FOOD_CROP"},
    {"value": "WHT", "label": _("Wheat"), "produce": "FOOD_CROP"},
    {"value": "YAM", "label": _("Yam"), "produce": "FOOD_CROP"},
]

CROPS_CHOICES = [(x["value"], x["label"]) for x in CROPS_ITEMS]
CropsEnum = Enum("CropsEnum", {x["value"]: x["value"] for x in CROPS_ITEMS})


class AnimalsEnum(TextChoices):
    AQU = "AQU", _("Aquaculture (animals)")
    BEE = "BEE", _("Beef Cattle")
    CTL = "CTL", _("Cattle")
    DCT = "DCT", _("Dairy Cattle")
    FSH = "FSH", _("Fish")
    GOT = "GOT", _("Goats")
    OTH = "OTH", _("Other livestock")
    PIG = "PIG", _("Pork")
    POU = "POU", _("Poultry")
    SHP = "SHP", _("Sheep")
    SHR = "SHR", _("Shrimp")


ANIMALS_ITEMS = serialize_enum(AnimalsEnum)
ANIMALS_CHOICES = AnimalsEnum.choices


class MineralsEnum(TextChoices):
    ALU = "ALU", _("Aluminum")
    ASP = "ASP", _("Asphaltite")
    ATC = "ATC", _("Anthracite")
    BAR = "BAR", _("Barite")
    BAS = "BAS", _("Basalt")
    BAX = "BAX", _("Bauxite")
    BEN = "BEN", _("Bentonite")
    BUM = "BUM", _("Building materials")
    CAR = "CAR", _("Carbon")
    CHR = "CHR", _("Chromite")
    CLA = "CLA", _("Clay")
    COA = "COA", _("Coal")
    COB = "COB", _("Cobalt")
    COP = "COP", _("Copper")
    DIA = "DIA", _("Diamonds")
    EME = "EME", _("Emerald")
    FLD = "FLD", _("Feldspar")
    FLO = "FLO", _("Fluoride")
    GAS = "GAS", _("Gas")
    GLD = "GLD", _("Gold")
    GRT = "GRT", _("Granite")
    GRV = "GRV", _("Gravel")
    HEA = "HEA", _("Heavy Mineral Sands")
    ILM = "ILM", _("Ilmenite")
    IRO = "IRO", _("Iron")
    JAD = "JAD", _("Jade")
    LED = "LED", _("Lead")
    LIM = "LIM", _("Limestone")
    LIT = "LIT", _("Lithium")
    MAG = "MAG", _("Magnetite")
    MBD = "MBD", _("Molybdenum")
    MGN = "MGN", _("Manganese")
    MRB = "MRB", _("Marble")
    NIK = "NIK", _("Nickel")
    OTH = "OTH", _("Other minerals")
    PET = "PET", _("Petroleum")
    PHP = "PHP", _("Phosphorous")
    PLT = "PLT", _("Platinum")
    PUM = "PUM", _("Hydrocarbons (e.g. crude oil)")
    PYR = "PYR", _("Pyrolisis Plant")
    RUT = "RUT", _("Rutile")
    SAN = "SAN", _("Sand")
    SIC = "SIC", _("Silica")
    SIL = "SIL", _("Silver")
    SLT = "SLT", _("Salt")
    STO = "STO", _("Stone")
    TIN = "TIN", _("Tin")
    TTM = "TTM", _("Titanium")
    URM = "URM", _("Uranium")
    ZNC = "ZNC", _("Zinc")


MINERALS_ITEMS = serialize_enum(MineralsEnum)
MINERALS_CHOICES = MineralsEnum.choices


class ActorEnum(TextChoices):
    GOVERNMENT_OR_STATE_INSTITUTIONS = "GOVERNMENT_OR_STATE_INSTITUTIONS", _(
        "Government / state institutions (government, ministries, departments, agencies etc.)"
    )
    TRADITIONAL_LAND_OWNERS_OR_COMMUNITIES = (
        "TRADITIONAL_LAND_OWNERS_OR_COMMUNITIES",
        _("Traditional land-owners / communities"),
    )
    TRADITIONAL_LOCAL_AUTHORITY = "TRADITIONAL_LOCAL_AUTHORITY", _(
        "Traditional local authority (e.g. Chiefdom council / Chiefs)"
    )
    BROKER = "BROKER", _("Broker")
    INTERMEDIARY = "INTERMEDIARY", _("Intermediary")
    OTHER = "OTHER", _("Other")


ACTOR_ITEMS = serialize_enum(ActorEnum)
ACTOR_CHOICES = ActorEnum.choices


class ElectricityGenerationEnum(TextChoices):
    WIND = "WIND", _("On-shore wind turbines")
    PHOTOVOLTAIC = "PHOTOVOLTAIC", _("Solar (Photovoltaic)")
    SOLAR_HEAT = "SOLAR_HEAT", _("Solar (Thermal system)")


ELECTRICITY_GENERATION_ITEMS = serialize_enum(ElectricityGenerationEnum)
# ELECTRICITY_GENERATIONS_CHOICES = ElectricityGenerationEnum.choices


class CarbonSequestrationEnum(TextChoices):
    REFORESTATION = "REFORESTATION", _("Reforestation & afforestation")
    AVOIDED_FOREST_CONVERSION = "AVOIDED_FOREST_CONVERSION", _(
        "Avoided forest conversion"
    )
    AVOIDED_GRASSLAND_CONVERSION = "AVOIDED_GRASSLAND_CONVERSION", _(
        "Avoided grassland conversion"
    )
    PEATLAND_RESTORATION = "PEATLAND_RESTORATION", _("Peatland restoration")
    IMPROVED_FOREST_MANAGEMENT = "IMPROVED_FOREST_MANAGEMENT", _(
        "Improved forest management"
    )
    SUSTAINABLE_AGRICULTURE = "SUSTAINABLE_AGRICULTURE", _("Sustainable agriculture")
    SUSTAINABLE_GRASSLAND_MANAGEMENT = "SUSTAINABLE_GRASSLAND_MANAGEMENT", _(
        "Sustainable grassland management"
    )
    RICE_EMISSION_REDUCTIONS = "RICE_EMISSION_REDUCTIONS", _("Rice emission reductions")
    SOLAR_PARK = "SOLAR_PARK", _("Solar park")
    WIND_FARM = "WIND_FARM", _("Wind farm")
    OTHER = "OTHER", _("Other")


CARBON_SEQUESTRATION_ITEMS = serialize_enum(CarbonSequestrationEnum)
# CARBON_SEQUESTRATION_CHOICES = CarbonSequestrationEnum.choices


class CarbonSequestrationCertEnum(TextChoices):
    REDD = "REDD", _("REDD+")
    VCS = "VCS", _("Verified Carbon Standard (VCS)")
    GOLD = "GOLD", _("Gold Standard for the Global Goals (GOLD)")
    CDM = "CDM", _("Clean Development Mechanism (CDM)")
    CAR = "CAR", _("Climate Action Reserve (CAR)")
    VIVO = "VIVO", _("Plan Vivo")
    OTHER = "OTHER", _("Other")


CARBON_SEQUESTRATION_CERT_ITEMS = serialize_enum(CarbonSequestrationCertEnum)
# CARBON_SEQUESTRATION_CERT_CHOICES = CarbonSequestrationCertEnum.choices


class WaterSourceEnum(TextChoices):
    GROUNDWATER = "GROUNDWATER", _("Groundwater")
    SURFACE_WATER = "SURFACE_WATER", _("Surface water")
    RIVER = "RIVER", _("River")
    LAKE = "LAKE", _("Lake")


WATER_SOURCE_ITEMS = serialize_enum(WaterSourceEnum)
WATER_SOURCE_CHOICES = WaterSourceEnum.choices


class NotPublicReasonEnum(TextChoices):
    CONFIDENTIAL = "CONFIDENTIAL", _("Confidential flag")
    NO_COUNTRY = "NO_COUNTRY", _("No country")
    HIGH_INCOME_COUNTRY = "HIGH_INCOME_COUNTRY", _("High-income country")
    NO_DATASOURCES = "NO_DATASOURCES", _("No datasources")
    NO_OPERATING_COMPANY = "NO_OPERATING_COMPANY", _("No operating company")
    NO_KNOWN_INVESTOR = "NO_KNOWN_INVESTOR", _("No known investor")


NOT_PUBLIC_REASON_ITEMS = serialize_enum(NotPublicReasonEnum)
NOT_PUBLIC_REASON_CHOICES = NotPublicReasonEnum.choices


class DatasourceTypeEnum(TextChoices):
    MEDIA_REPORT = "MEDIA_REPORT", _("Media report")
    RESEARCH_PAPER_OR_POLICY_REPORT = "RESEARCH_PAPER_OR_POLICY_REPORT", _(
        "Research Paper / Policy Report"
    )
    GOVERNMENT_SOURCES = "GOVERNMENT_SOURCES", _("Government sources")
    COMPANY_SOURCES = "COMPANY_SOURCES", _("Company sources")
    CONTRACT = "CONTRACT", _("Contract")
    CONTRACT_FARMING_AGREEMENT = "CONTRACT_FARMING_AGREEMENT", _(
        "Contract (contract farming agreement)"
    )
    PERSONAL_INFORMATION = "PERSONAL_INFORMATION", _("Personal information")
    CROWDSOURCING = "CROWDSOURCING", _("Crowdsourcing")
    OTHER = "OTHER", _("Other")


DATASOURCE_TYPE_ITEMS = serialize_enum(DatasourceTypeEnum)
DATASOURCE_TYPE_CHOICES = DatasourceTypeEnum.choices


class LocationAccuracyEnum(TextChoices):
    COUNTRY = "COUNTRY", _("Country")
    ADMINISTRATIVE_REGION = "ADMINISTRATIVE_REGION", _("Administrative region")
    APPROXIMATE_LOCATION = "APPROXIMATE_LOCATION", _("Approximate location")
    EXACT_LOCATION = "EXACT_LOCATION", _("Exact location")
    COORDINATES = "COORDINATES", _("Coordinates")


LOCATION_ACCURACY_ITEMS = serialize_enum(LocationAccuracyEnum)
LOCATION_ACCURACY_CHOICES = LocationAccuracyEnum.choices


class InvestorClassificationEnum(TextChoices):
    GOVERNMENT = "GOVERNMENT", _("Government")
    GOVERNMENT_INSTITUTION = "GOVERNMENT_INSTITUTION", _("Government institution")
    STATE_OWNED_COMPANY = "STATE_OWNED_COMPANY", _("State-/government (owned) company")
    SEMI_STATE_OWNED_COMPANY = "SEMI_STATE_OWNED_COMPANY", _("Semi state-owned company")
    ASSET_MANAGEMENT_FIRM = "ASSET_MANAGEMENT_FIRM", _("Asset management firm")
    BILATERAL_DEVELOPMENT_BANK = "BILATERAL_DEVELOPMENT_BANK", _(
        "Bilateral Development Bank / Development Finance Institution"
    )
    STOCK_EXCHANGE_LISTED_COMPANY = "STOCK_EXCHANGE_LISTED_COMPANY", _(
        "Stock-exchange listed company"
    )
    COMMERCIAL_BANK = "COMMERCIAL_BANK", _("Commercial Bank")
    INSURANCE_FIRM = "INSURANCE_FIRM", _("Insurance firm")
    INVESTMENT_BANK = "INVESTMENT_BANK", _("Investment Bank")
    INVESTMENT_FUND = "INVESTMENT_FUND", _("Investment fund")
    MULTILATERAL_DEVELOPMENT_BANK = "MULTILATERAL_DEVELOPMENT_BANK", _(
        "Multilateral Development Bank (MDB)"
    )
    PRIVATE_COMPANY = "PRIVATE_COMPANY", _("Private company")
    PRIVATE_EQUITY_FIRM = "PRIVATE_EQUITY_FIRM", _("Private equity firm")
    INDIVIDUAL_ENTREPRENEUR = "INDIVIDUAL_ENTREPRENEUR", _("Individual entrepreneur")
    NON_PROFIT = "NON_PROFIT", _(
        "Non - Profit organization (e.g. Church, University etc.)"
    )
    OTHER = "OTHER", _("Other")


INVESTOR_CLASSIFICATION_ITEMS = serialize_enum(InvestorClassificationEnum)
INVESTOR_CLASSIFICATION_CHOICES = InvestorClassificationEnum.choices


class InvestorTypeEnum(TextChoices):
    EQUITY = "EQUITY", _("Shares/Equity")
    DEBT_FINANCING = "DEBT_FINANCING", _("Debt financing")


INVESTMENT_TYPE_ITEMS = serialize_enum(InvestorTypeEnum)
INVESTMENT_TYPE_CHOICES = InvestorTypeEnum.choices


class InvolvementRoleEnum(TextChoices):
    PARENT = "PARENT", _("Parent company")
    LENDER = "LENDER", _("Tertiary investor/lender")


INVOLVEMENT_ROLE_ITEMS = serialize_enum(InvolvementRoleEnum)
INVOLVEMENT_ROLE_CHOICES = InvolvementRoleEnum.choices


# TODO: Sync with investors.py
class ParentRelationEnum(TextChoices):
    SUBSIDIARY = "SUBSIDIARY", _("Subsidiary of parent company")
    LOCAL_BRANCH = "LOCAL_BRANCH", _("Local branch of parent company")
    JOINT_VENTURE = "JOINT_VENTURE", _("Joint venture of parent companies")


PARENT_RELATION_ITEMS = serialize_enum(ParentRelationEnum)
PARENT_RELATION_CHOICES = ParentRelationEnum.choices


# FIXME: Use Uppercase characters for value
class AreaTypeEnum(TextChoices):
    production_area = "production_area", _("Production area")
    contract_area = "contract_area", _("Contract area")
    intended_area = "intended_area", _("Intended area")


AREA_TYPE_ITEMS = serialize_enum(AreaTypeEnum)
AREA_TYPE_CHOICES = AreaTypeEnum.choices
