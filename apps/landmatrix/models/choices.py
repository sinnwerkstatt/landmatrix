from django.utils.translation import gettext_lazy as _


INTENTION_OF_INVESTMENT_ITEMS = [
    {
        "value": "BIOFUELS",
        "label": _("Biomass for biofuels"),
        "group": _("Agriculture"),
    },
    {
        "value": "BIOMASS_ENERGY_GENERATION",
        "label": _("Biomass for energy generation"),
        "group": _("Agriculture"),
    },
    {"value": "FODDER", "label": _("Fodder"), "group": _("Agriculture")},
    {"value": "FOOD_CROPS", "label": _("Food crops"), "group": _("Agriculture")},
    {"value": "LIVESTOCK", "label": _("Livestock"), "group": _("Agriculture")},
    {
        "value": "NON_FOOD_AGRICULTURE",
        "label": _("Non-food agricultural commodities"),
        "group": _("Agriculture"),
    },
    {
        "value": "AGRICULTURE_UNSPECIFIED",
        "label": _("Agriculture unspecified"),
        "group": _("Agriculture"),
    },
    {
        "value": "BIOMASS_ENERGY_PRODUCTION",
        "label": _("Biomass for energy generation"),
        "group": _("Forestry"),
    },
    {
        "value": "CARBON",
        "label": _("For carbon sequestration/REDD"),
        "group": _("Forestry"),
    },
    {
        "value": "FOREST_LOGGING",
        "label": _("Forest logging / management for wood and fiber"),
        "group": _("Forestry"),
    },
    {
        "value": "TIMBER_PLANTATION",
        "label": _("Timber plantation for wood and fiber"),
        "group": _("Forestry"),
    },
    {
        "value": "FORESTRY_UNSPECIFIED",
        "label": _("Forestry unspecified"),
        "group": _("Forestry"),
    },
    {
        "value": "SOLAR_PARK",
        "label": _("Solar park"),
        "group": _("Renewable energy power plants"),
    },
    {
        "value": "WIND_FARM",
        "label": _("Wind farm"),
        "group": _("Renewable energy power plants"),
    },
    {
        "value": "RENEWABLE_ENERGY",
        "label": _("Renewable energy unspecified"),
        "group": _("Renewable energy power plants"),
    },
    {"value": "CONVERSATION", "label": _("Conservation"), "group": _("Other")},
    {"value": "INDUSTRY", "label": _("Industry"), "group": _("Other")},
    {"value": "LAND_SPECULATION", "label": _("Land speculation"), "group": _("Other")},
    {"value": "MINING", "label": _("Mining"), "group": _("Other")},
    {
        "value": "OIL_GAS_EXTRACTION",
        "label": _("Oil / Gas extraction"),
        "group": _("Other"),
    },
    {"value": "TOURISM", "label": _("Tourism"), "group": _("Other")},
    {"value": "OTHER", "label": _("Other"), "group": _("Other")},
]


INTENTION_CHOICES_GROUPED = [
    # agriculture
    (
        _("Agriculture"),
        [
            ("BIOFUELS", _("Biomass for biofuels")),
            ("BIOMASS_ENERGY_GENERATION", _("Biomass for energy generation")),
            ("FODDER", _("Fodder")),
            ("FOOD_CROPS", _("Food crops")),
            ("LIVESTOCK", _("Livestock")),
            ("NON_FOOD_AGRICULTURE", _("Non-food agricultural commodities")),
            ("AGRICULTURE_UNSPECIFIED", _("Agriculture unspecified")),
        ],
    ),
    # forest
    (
        _("Forestry"),
        [
            ("BIOMASS_ENERGY_PRODUCTION", _("Biomass for energy generation")),
            ("CARBON", _("For carbon sequestration/REDD")),
            ("FOREST_LOGGING", _("Forest logging / management for wood and fiber")),
            ("TIMBER_PLANTATION", _("Timber plantation for wood and fiber")),
            ("FORESTRY_UNSPECIFIED", _("Forestry unspecified")),
        ],
    ),
    # renewable
    (
        _("Renewable energy power plants"),
        (
            ("SOLAR_PARK", _("Solar park")),
            ("WIND_FARM", _("Wind farm")),
            ("RENEWABLE_ENERGY", _("Renewable energy unspecified")),
        ),
    ),
    # other
    (
        _("Other"),
        [
            ("CONVERSATION", _("Conservation")),
            ("INDUSTRY", _("Industry")),
            ("LAND_SPECULATION", _("Land speculation")),
            ("MINING", _("Mining")),
            ("OIL_GAS_EXTRACTION", _("Oil / Gas extraction")),
            ("TOURISM", _("Tourism")),
            ("OTHER", _("Other")),
        ],
    ),
]

INTENTION_CHOICES = [(x["value"], x["label"]) for x in INTENTION_OF_INVESTMENT_ITEMS]

NATURE_OF_DEAL_CHOICES = [
    ("OUTRIGHT_PURCHASE", _("Outright purchase")),
    ("LEASE", _("Lease")),
    ("CONCESSION", _("Concession")),
    (
        "EXPLOITATION_PERMIT",
        _("Exploitation permit / license / concession (for mineral resources)"),
    ),
    ("PURE_CONTRACT_FARMING", _("Pure contract farming")),
    ("OTHER", _("Other")),
]

NEGOTIATION_STATUS_ITEMS = [
    {
        "value": "EXPRESSION_OF_INTEREST",
        "label": _("Intended (Expression of interest)"),
        "group": _("Intended"),
    },
    {
        "value": "UNDER_NEGOTIATION",
        "label": _("Intended (Under negotiation)"),
        "group": _("Intended"),
    },
    {
        "value": "MEMORANDUM_OF_UNDERSTANDING",
        "label": _("Intended (Memorandum of understanding)"),
        "group": _("Intended"),
    },
    {
        "value": "ORAL_AGREEMENT",
        "label": _("Concluded (Oral Agreement)"),
        "group": _("Concluded"),
    },
    {
        "value": "CONTRACT_SIGNED",
        "label": _("Concluded (Contract signed)"),
        "group": _("Concluded"),
    },
    {
        "value": "CHANGE_OF_OWNERSHIP",
        "label": _("Concluded (Change of ownership)"),
        "group": _("Concluded"),
    },
    {
        "value": "NEGOTIATIONS_FAILED",
        "label": _("Failed (Negotiations failed)"),
        "group": _("Failed"),
    },
    {
        "value": "CONTRACT_CANCELED",
        "label": _("Failed (Contract cancelled)"),
        "group": _("Failed"),
    },
    {"value": "CONTRACT_EXPIRED", "label": _("Contract expired")},
]
NEGOTIATION_STATUS_CHOICES = [
    (x["value"], x["label"]) for x in NEGOTIATION_STATUS_ITEMS
]

IMPLEMENTATION_STATUS_ITEMS = [
    {"value": "PROJECT_NOT_STARTED", "label": _("Project not started")},
    {"value": "STARTUP_PHASE", "label": _("Startup phase (no production)")},
    {"value": "IN_OPERATION", "label": _("In operation (production)")},
    {"value": "PROJECT_ABANDONED", "label": _("Project abandoned")},
]
IMPLEMENTATION_STATUS_CHOICES = [
    (x["value"], x["label"]) for x in IMPLEMENTATION_STATUS_ITEMS
]

ACTOR_ITEMS = [
    {
        "value": "GOVERNMENT_OR_STATE_INSTITUTIONS",
        "label": _(
            "Government / state institutions (government, ministries, departments, agencies etc.)"
        ),
    },
    {
        "value": "TRADITIONAL_LAND_OWNERS_OR_COMMUNITIES",
        "label": _("Traditional land-owners / communities"),
    },
    {
        "value": "TRADITIONAL_LOCAL_AUTHORITY",
        "label": _("Traditional local authority (e.g. Chiefdom council / Chiefs)"),
    },
    {"value": "BROKER", "label": _("Broker")},
    {"value": "INTERMEDIARY", "label": _("Intermediary")},
    {"value": "OTHER", "label": _("Other (please specify)")},
]
ACTOR_MAP = [(x["value"], x["label"]) for x in ACTOR_ITEMS]


RECOGNITION_STATUS_CHOICES = (
    (
        "INDIGENOUS_RIGHTS_RECOGNIZED",
        _(
            "Indigenous Peoples traditional or customary rights recognized by government"
        ),
    ),
    (
        "INDIGENOUS_RIGHTS_NOT_RECOGNIZED",
        _(
            "Indigenous Peoples traditional or customary rights not recognized by government"
        ),
    ),
    (
        "COMMUNITY_RIGHTS_RECOGNIZED",
        _("Community traditional or customary rights recognized by government"),
    ),
    (
        "COMMUNITY_RIGHTS_NOT_RECOGNIZED",
        _("Community traditional or customary rights not recognized by government"),
    ),
)

NEGATIVE_IMPACTS_CHOICES = (
    ("ENVIRONMENTAL_DEGRADATION", _("Environmental degradation")),
    ("SOCIO_ECONOMIC", _("Socio-economic")),
    ("CULTURAL_LOSS", _("Cultural loss")),
    ("EVICTION", _("Eviction")),
    ("DISPLACEMENT", _("Displacement")),
    ("VIOLENCE", _("Violence")),
    ("OTHER", _("Other")),
)

BENEFITS_CHOICES = (
    ("HEALTH", _("Health")),
    ("EDUCATION", _("Education")),
    (
        "PRODUCTIVE_INFRASTRUCTURE",
        _("Productive infrastructure (e.g. irrigation, tractors, machinery...)"),
    ),
    ("ROADS", _("Roads")),
    ("CAPACITY_BUILDING", _("Capacity building")),
    ("FINANCIAL_SUPPORT", _("Financial support")),
    ("COMMUNITY_SHARES", _("Community shares in the investment project")),
    ("OTHER", _("Other")),
)

FORMER_LAND_OWNER_CHOICES = (
    ("STATE", _("State")),
    ("PRIVATE_SMALLHOLDERS", _("Private (smallholders)")),
    ("PRIVATE_LARGE_SCALE", _("Private (large-scale farm)")),
    ("COMMUNITY", _("Community")),
    ("INDIGENOUS_PEOPLE", _("Indigenous people")),
    ("OTHER", _("Other")),
)

FORMER_LAND_USE_CHOICES = (
    ("COMMERCIAL_AGRICULTURE", _("Commercial (large-scale) agriculture")),
    ("SMALLHOLDER_AGRICULTURE", _("Smallholder agriculture")),
    ("SHIFTING_CULTIVATION", _("Shifting cultivation")),
    ("PASTORALISM", _("Pastoralism")),
    ("HUNTING_GATHERING", _("Hunting/Gathering")),
    ("FORESTRY", _("Forestry")),
    ("CONSERVATION", _("Conservation")),
    ("OTHER", _("Other")),
)

HA_AREA_CHOICES = (("PER_HA", _("per ha")), ("PER_AREA", _("for specified area")))

COMMUNITY_CONSULTATION_CHOICES = (
    ("NOT_CONSULTED", _("Not consulted")),
    ("LIMITED_CONSULTATION", _("Limited consultation")),
    ("FPIC", _("Free, Prior and Informed Consent (FPIC)")),
    ("OTHER", _("Other")),
)
COMMUNITY_REACTION_CHOICES = (
    ("CONSENT", _("Consent")),
    ("MIXED_REACTION", _("Mixed reaction")),
    ("REJECTION", _("Rejection")),
)

FORMER_LAND_COVER_CHOICES = (
    ("CROPLAND", _("Cropland")),
    ("FOREST_LAND", _("Forest land")),
    ("PASTURE", _("Pasture")),
    ("RANGELAND", _("Shrub land/Grassland (Rangeland)")),
    ("MARGINAL_LAND", _("Marginal land")),
    ("WETLAND", _("Wetland")),
    (
        "OTHER_LAND",
        _("Other land (e.g. developed land – specify in comment field)"),
    ),
)

CROPS_ITEMS = [
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
    {"value": "OTH", "label": _("Other crops (please specify)")},
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
CROPS = {
    x["value"]: {"name": x["label"], "produce": x.get("produce")} for x in CROPS_ITEMS
}
CROPS_CHOICES = [(x["value"], x["label"]) for x in CROPS_ITEMS]

ANIMALS_ITEMS = [
    {"value": "AQU", "label": _("Aquaculture (animals)")},
    {"value": "BEE", "label": _("Beef Cattle")},
    {"value": "CTL", "label": _("Cattle")},
    {"value": "DCT", "label": _("Dairy Cattle")},
    {"value": "FSH", "label": _("Fish")},
    {"value": "GOT", "label": _("Goats")},
    {"value": "OTH", "label": _("Other livestock (please specify)")},
    {"value": "PIG", "label": _("Pork")},
    {"value": "POU", "label": _("Poultry")},
    {"value": "SHP", "label": _("Sheep")},
    {"value": "SHR", "label": _("Shrimp")},
]
ANIMALS = {x["value"]: {"name": x["label"]} for x in ANIMALS_ITEMS}
ANIMALS_CHOICES = [(x["value"], x["label"]) for x in ANIMALS_ITEMS]

ELECTRICITY_GENERATION_ITEMS = [
    {"value": "WIND", "label": _("On-shore wind turbines")},
    {"value": "PHOTOVOLTAIC", "label": _("Solar (Photovoltaic)")},
    {"value": "SOLAR_HEAT", "label": _("Solar (Thermal system)")},
]
ELECTRICITY_GENERATIONS_CHOICES = [
    (x["value"], x["label"]) for x in ELECTRICITY_GENERATION_ITEMS
]

CARBON_SEQUESTRATION_ITEMS = [
    {"value": "REFORESTATION", "label": _("Reforestation & afforestation")},
    {"value": "AVOIDED_FOREST_CONVERSION", "label": _("Avoided forest conversion")},
    {
        "value": "AVOIDED_GRASSLAND_CONVERSION",
        "label": _("Avoided grassland conversion"),
    },
    {"value": "PEATLAND_RESTORATION", "label": _("Peatland restoration")},
    {"value": "IMPROVED_FOREST_MANAGEMENT", "label": _("Improved forest management")},
    {"value": "SUSTAINABLE_AGRICULTURE", "label": _("Sustainable agriculture")},
    {
        "value": "SUSTAINABLE_GRASSLAND_MANAGEMENT",
        "label": _("Sustainable grassland management"),
    },
    {"value": "RICE_EMISSION_REDUCTIONS", "label": _("Rice emission reductions")},
    {"value": "OTHER", "label": _("Other (please specify in a comment)")},
]
CARBON_SEQUESTRATION_CHOICES = [
    (x["value"], x["label"]) for x in CARBON_SEQUESTRATION_ITEMS
]

CARBON_SEQUESTRATION_CERT_ITEMS = [
    {"value": "REDD", "label": _("REDD+")},
    {"value": "VCS", "label": _("Verified Carbon Standard (VCS)")},
    {"value": "GOLD", "label": _("Gold Standard for the Global Goals (GOLD)")},
    {"value": "CDM", "label": _("Clean Development Mechanism (CDM)")},
    {"value": "CAR", "label": _("Climate Action Reserve (CAR)")},
    {"value": "VIVO", "label": _("Plan Vivo")},
    {"value": "OTHER", "label": _("Other (please specify in a comment)")},
]
CARBON_SEQUESTRATION_CERT_CHOICES = [
    (x["value"], x["label"]) for x in CARBON_SEQUESTRATION_CERT_ITEMS
]

MINERALS_ITEMS = [
    {"value": "ALU", "label": _("Aluminum")},
    {"value": "ASP", "label": _("Asphaltite")},
    {"value": "ATC", "label": _("Anthracite")},
    {"value": "BAR", "label": _("Barite")},
    {"value": "BAS", "label": _("Basalt")},
    {"value": "BAX", "label": _("Bauxite")},
    {"value": "BEN", "label": _("Bentonite")},
    {"value": "BUM", "label": _("Building materials")},
    {"value": "CAR", "label": _("Carbon")},
    {"value": "CHR", "label": _("Chromite")},
    {"value": "CLA", "label": _("Clay")},
    {"value": "COA", "label": _("Coal")},
    {"value": "COB", "label": _("Cobalt")},
    {"value": "COP", "label": _("Copper")},
    {"value": "DIA", "label": _("Diamonds")},
    {"value": "EME", "label": _("Emerald")},
    {"value": "FLD", "label": _("Feldspar")},
    {"value": "FLO", "label": _("Fluoride")},
    {"value": "GAS", "label": _("Gas")},
    {"value": "GLD", "label": _("Gold")},
    {"value": "GRT", "label": _("Granite")},
    {"value": "GRV", "label": _("Gravel")},
    {"value": "HEA", "label": _("Heavy Mineral Sands")},
    {"value": "ILM", "label": _("Ilmenite")},
    {"value": "IRO", "label": _("Iron")},
    {"value": "JAD", "label": _("Jade")},
    {"value": "LED", "label": _("Lead")},
    {"value": "LIM", "label": _("Limestone")},
    {"value": "LIT", "label": _("Lithium")},
    {"value": "MAG", "label": _("Magnetite")},
    {"value": "MBD", "label": _("Molybdenum")},
    {"value": "MGN", "label": _("Manganese")},
    {"value": "MRB", "label": _("Marble")},
    {"value": "NIK", "label": _("Nickel")},
    {"value": "OTH", "label": _("Other minerals (please specify)")},
    {"value": "PET", "label": _("Petroleum")},
    {"value": "PHP", "label": _("Phosphorous")},
    {"value": "PLT", "label": _("Platinum")},
    {"value": "PUM", "label": _("Hydrocarbons (e.g. crude oil)")},
    {"value": "PYR", "label": _("Pyrolisis Plant")},
    {"value": "RUT", "label": _("Rutile")},
    {"value": "SAN", "label": _("Sand")},
    {"value": "SIC", "label": _("Silica")},
    {"value": "SIL", "label": _("Silver")},
    {"value": "SLT", "label": _("Salt")},
    {"value": "STO", "label": _("Stone")},
    {"value": "TIN", "label": _("Tin")},
    {"value": "TTM", "label": _("Titanium")},
    {"value": "URM", "label": _("Uranium")},
    {"value": "ZNC", "label": _("Zinc")},
]
MINERALS = {x["value"]: {"name": x["label"]} for x in MINERALS_ITEMS}
MINERALS_CHOICES = [(x["value"], x["label"]) for x in MINERALS_ITEMS]

WATER_SOURCE_CHOICES = (
    ("GROUNDWATER", _("Groundwater")),
    ("SURFACE_WATER", _("Surface water")),
    ("RIVER", _("River")),
    ("LAKE", _("Lake")),
)

NOT_PUBLIC_REASON_CHOICES = (
    ("CONFIDENTIAL", _("Confidential flag")),
    ("NO_COUNTRY", _("No country")),
    ("HIGH_INCOME_COUNTRY", _("High-income country")),
    ("NO_DATASOURCES", _("No datasources")),
    ("NO_OPERATING_COMPANY", _("No operating company")),
    ("NO_KNOWN_INVESTOR", _("No known investor")),
)

DATASOURCE_TYPE_MAP = {
    "MEDIA_REPORT": _("Media report"),
    "RESEARCH_PAPER_OR_POLICY_REPORT": _("Research Paper / Policy Report"),
    "GOVERNMENT_SOURCES": _("Government sources"),
    "COMPANY_SOURCES": _("Company sources"),
    "CONTRACT": "Contract",
    "CONTRACT_FARMING_AGREEMENT": _("Contract (contract farming agreement)"),
    "PERSONAL_INFORMATION": _("Personal information"),
    "CROWDSOURCING": _("Crowdsourcing"),
    "OTHER": _("Other (Please specify in comment field)"),
}
DATASOURCE_TYPE_OPTIONS = [
    {"value": k, "label": v} for k, v in DATASOURCE_TYPE_MAP.items()
]
DATASOURCE_TYPE_CHOICES = ((k, v) for k, v in DATASOURCE_TYPE_MAP.items())


LOCATION_ACCURACY_ITEMS = [
    {"value": "COUNTRY", "label": _("Country")},
    {"value": "ADMINISTRATIVE_REGION", "label": _("Administrative region")},
    {"value": "APPROXIMATE_LOCATION", "label": _("Approximate location")},
    {"value": "EXACT_LOCATION", "label": _("Exact location")},
    {"value": "COORDINATES", "label": _("Coordinates")},
]

LOCATION_ACCURACY = {
    "COUNTRY": _("Country"),
    "ADMINISTRATIVE_REGION": _("Administrative region"),
    "APPROXIMATE_LOCATION": _("Approximate location"),
    "EXACT_LOCATION": _("Exact location"),
    "COORDINATES": _("Coordinates"),
}

LOCATION_ACCURACY_OPTIONS = [
    {"value": k, "label": v} for k, v in LOCATION_ACCURACY.items()
]

LEVEL_OF_ACCURACY_CHOICES = ((k, v) for k, v in LOCATION_ACCURACY.items())

INVESTOR_CLASSIFICATION_ITEMS = [
    {"value": "GOVERNMENT", "label": _("Government")},
    {"value": "GOVERNMENT_INSTITUTION", "label": _("Government institution")},
    {"value": "STATE_OWNED_COMPANY", "label": _("State-/government (owned) company")},
    {"value": "SEMI_STATE_OWNED_COMPANY", "label": _("Semi state-owned company")},
    {"value": "ASSET_MANAGEMENT_FIRM", "label": _("Asset management firm")},
    {
        "value": "BILATERAL_DEVELOPMENT_BANK",
        "label": _("Bilateral Development Bank / Development Finance Institution"),
    },
    {
        "value": "STOCK_EXCHANGE_LISTED_COMPANY",
        "label": _("Stock-exchange listed company"),
    },
    {"value": "COMMERCIAL_BANK", "label": _("Commercial Bank")},
    {"value": "INSURANCE_FIRM", "label": _("Insurance firm")},
    {"value": "INVESTMENT_BANK", "label": _("Investment Bank")},
    {"value": "INVESTMENT_FUND", "label": _("Investment fund")},
    {
        "value": "MULTILATERAL_DEVELOPMENT_BANK",
        "label": _("Multilateral Development Bank (MDB)"),
    },
    {"value": "PRIVATE_COMPANY", "label": _("Private company")},
    {"value": "PRIVATE_EQUITY_FIRM", "label": _("Private equity firm")},
    {"value": "INDIVIDUAL_ENTREPRENEUR", "label": _("Individual entrepreneur")},
    {
        "value": "NON_PROFIT",
        "label": _("Non - Profit organization (e.g. Church, University etc.)"),
    },
    {"value": "OTHER", "label": _("Other (please specify in comment field)")},
]
INVESTOR_CLASSIFICATION_CHOICES = [
    (x["value"], x["label"]) for x in INVESTOR_CLASSIFICATION_ITEMS
]

INVESTMENT_TYPE_ITEMS = [
    {"value": "EQUITY", "label": _("Shares/Equity")},
    {"value": "DEBT_FINANCING", "label": _("Debt financing")},
]
