from django.utils.translation import gettext as _

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


INTENTION_CHOICES = [
    # agriculture
    ("BIOFUELS", _("Biomass for biofuels")),
    ("BIOMASS_ENERGY_GENERATION", _("Biomass for energy generation")),
    ("FODDER", _("Fodder")),
    ("FOOD_CROPS", _("Food crops")),
    ("LIVESTOCK", _("Livestock")),
    ("NON_FOOD_AGRICULTURE", _("Non-food agricultural commodities")),
    ("AGRICULTURE_UNSPECIFIED", _("Agriculture unspecified")),
    # forest
    ("BIOMASS_ENERGY_PRODUCTION", _("Biomass for energy generation")),
    ("CARBON", _("For carbon sequestration/REDD")),
    ("FOREST_LOGGING", _("Forest logging / management for wood and fiber")),
    ("TIMBER_PLANTATION", _("Timber plantation for wood and fiber")),
    ("FORESTRY_UNSPECIFIED", _("Forestry unspecified")),
    # renewable
    ("SOLAR_PARK", _("Solar park")),
    ("WIND_FARM", _("Wind farm")),
    ("RENEWABLE_ENERGY", _("Renewable energy unspecified")),
    # other
    ("CONVERSATION", _("Conservation")),
    ("INDUSTRY", _("Industry")),
    ("LAND_SPECULATION", _("Land speculation")),
    ("MINING", _("Mining")),
    ("OIL_GAS_EXTRACTION", _("Oil / Gas extraction")),
    ("TOURISM", _("Tourism")),
    ("OTHER", _("Other")),
]
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

NEGOTIATION_STATUS_CHOICES = [
    ("EXPRESSION_OF_INTEREST", _("Intended (Expression of interest)")),
    ("UNDER_NEGOTIATION", _("Intended (Under negotiation)")),
    ("MEMORANDUM_OF_UNDERSTANDING", _("Intended (Memorandum of understanding)")),
    ("ORAL_AGREEMENT", _("Concluded (Oral Agreement)")),
    ("CONTRACT_SIGNED", _("Concluded (Contract signed)")),
    ("CHANGE_OF_OWNERSHIP", _("Concluded (Change of ownership)")),
    ("NEGOTIATIONS_FAILED", _("Failed (Negotiations failed)")),
    ("CONTRACT_CANCELED", _("Failed (Contract cancelled)")),
    ("CONTRACT_EXPIRED", _("Contract expired")),
]

NEGOTIATION_STATUS_CHOICES_GROUPED = [
    (
        "Intended",
        [
            ("EXPRESSION_OF_INTEREST", _("Intended (Expression of interest)")),
            ("UNDER_NEGOTIATION", _("Intended (Under negotiation)")),
            (
                "MEMORANDUM_OF_UNDERSTANDING",
                _("Intended (Memorandum of understanding)"),
            ),
        ],
    ),
    (
        "Concluded",
        [
            ("ORAL_AGREEMENT", _("Concluded (Oral Agreement)")),
            ("CONTRACT_SIGNED", _("Concluded (Contract signed)")),
            ("CHANGE_OF_OWNERSHIP", _("Concluded (Change of ownership)")),
        ],
    ),
    (
        "Failed",
        [
            ("NEGOTIATIONS_FAILED", _("Failed (Negotiations failed)")),
            ("CONTRACT_CANCELED", _("Failed (Contract cancelled)")),
        ],
    ),
    ("CONTRACT_EXPIRED", _("Contract expired")),
]

IMPLEMENTATION_STATUS_CHOICES = [
    ("PROJECT_NOT_STARTED", "Project not started"),
    ("STARTUP_PHASE", "Startup phase (no production)"),
    ("IN_OPERATION", "In operation (production)"),
    ("PROJECT_ABANDONED", "Project abandoned"),
]

ACTOR_MAP = [
    (
        "GOVERNMENT_OR_STATE_INSTITUTIONS",
        _(
            "Government / state institutions (government, ministries, departments, agencies etc.)"
        ),
    ),
    (
        "TRADITIONAL_LAND_OWNERS_OR_COMMUNITIES",
        _("Traditional land-owners / communities"),
    ),
    (
        "TRADITIONAL_LOCAL_AUTHORITY",
        _("Traditional local authority (e.g. Chiefdom council / Chiefs)"),
    ),
    ("BROKER", _("Broker")),
    ("INTERMEDIARY", _("Intermediary")),
    ("OTHER", _("Other (please specify)")),
]

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

CROPS = {
    "ACC": {"name": _("Accacia"), "produce": "NON_FOOD"},
    "ALF": {"name": _("Alfalfa"), "produce": "NON_FOOD"},
    "ALG": {"name": _("Seaweed / Macroalgae(unspecified)"), "produce": "NON_FOOD"},
    "ALM": {"name": _("Almond"), "produce": "FOOD_CROP"},
    "ALV": {"name": _("Aloe Vera"), "produce": "NON_FOOD"},
    "APL": {"name": _("Apple"), "produce": "FOOD_CROP"},
    "AQU": {"name": _("Aquaculture (unspecified crops)"), "produce": "FOOD_CROP"},
    "BAM": {"name": _("Bamboo"), "produce": "NON_FOOD"},
    "BAN": {"name": _("Banana"), "produce": "FOOD_CROP"},
    "BEA": {"name": _("Bean"), "produce": "FOOD_CROP"},
    "BOT": {"name": _("Bottle Gourd"), "produce": "FOOD_CROP"},
    "BRL": {"name": _("Barley"), "produce": "FOOD_CROP"},
    "BWT": {"name": _("Buckwheat"), "produce": "FOOD_CROP"},
    "CAC": {"name": _("Cacao"), "produce": "FOOD_CROP"},
    "CAS": {"name": _("Cassava (Maniok)"), "produce": "FOOD_CROP"},
    "CAW": {"name": _("Cashew"), "produce": "FOOD_CROP"},
    "CHA": {"name": _("Chat")},
    "CHE": {"name": _("Cherries"), "produce": "FOOD_CROP"},
    "CNL": {"name": _("Canola"), "produce": "FLEX_CROP"},
    "COC": {"name": _("Coconut"), "produce": "FOOD_CROP"},
    "COF": {"name": _("Coffee Plant"), "produce": "FOOD_CROP"},
    "COT": {"name": _("Cotton"), "produce": "NON_FOOD"},
    "CRL": {"name": _("Cereals (unspecified)"), "produce": "FOOD_CROP"},
    "CRN": {"name": _("Corn (Maize)"), "produce": "FOOD_CROP"},
    "CRO": {"name": _("Croton"), "produce": "NON_FOOD"},
    "CST": {"name": _("Castor Oil Plant"), "produce": "NON_FOOD"},
    "CTR": {"name": _("Citrus Fruits (unspecified)"), "produce": "FOOD_CROP"},
    "DIL": {"name": _("Dill"), "produce": "NON_FOOD"},
    "EUC": {"name": _("Eucalyptus"), "produce": "NON_FOOD"},
    "FLW": {"name": _("Flowers (unspecified)"), "produce": "NON_FOOD"},
    "FNT": {"name": _("Fig-Nut"), "produce": "FOOD_CROP"},
    "FOD": {"name": _("Fodder Plants (unspecified)"), "produce": "NON_FOOD"},
    "FOO": {"name": _("Food crops (unspecified)"), "produce": "FOOD_CROP"},
    "FRT": {"name": _("Fruit (unspecified)"), "produce": "FOOD_CROP"},
    "GRA": {"name": _("Grapes"), "produce": "FOOD_CROP"},
    "GRN": {"name": _("Grains (unspecified)"), "produce": "FOOD_CROP"},
    "HRB": {"name": _("Herbs (unspecified)")},
    "JTR": {"name": _("Jatropha"), "produce": "NON_FOOD"},
    "LNT": {"name": _("Lentils"), "produce": "FOOD_CROP"},
    "MAN": {"name": _("Mango"), "produce": "FOOD_CROP"},
    "MUS": {"name": _("Mustard"), "produce": "FOOD_CROP"},
    "OAT": {"name": _("Oats")},
    "OIL": {"name": _("Oil Seeds (unspecified)"), "produce": "FLEX_CROP"},
    "OLE": {"name": _("Oleagionous plant"), "produce": "FLEX_CROP"},
    "OLV": {"name": _("Olives"), "produce": "FOOD_CROP"},
    "ONI": {"name": _("Onion"), "produce": "FOOD_CROP"},
    "OPL": {"name": _("Oil Palm"), "produce": "FLEX_CROP"},
    "OTH": {"name": _("Other crops (please specify)")},
    "PAL": {"name": _("Palms"), "produce": "FOOD_CROP"},
    "PAP": {"name": _("Papaya"), "produce": "FOOD_CROP"},
    "PAS": {"name": _("Passion fruit"), "produce": "FOOD_CROP"},
    "PEA": {"name": _("Peanut (groundnut)"), "produce": "FOOD_CROP"},
    "PEP": {"name": _("Pepper"), "produce": "FOOD_CROP"},
    "PES": {"name": _("Peas"), "produce": "FOOD_CROP"},
    "PIE": {"name": _("Pine"), "produce": "FOOD_CROP"},
    "PIN": {"name": _("Pineapple"), "produce": "FOOD_CROP"},
    "PLS": {"name": _("Pulses (unspecified)"), "produce": "FOOD_CROP"},
    "POM": {"name": _("Pomegranate"), "produce": "FOOD_CROP"},
    "PON": {"name": _("Pongamia Pinnata"), "produce": "NON_FOOD"},
    "PTT": {"name": _("Potatoes"), "produce": "FOOD_CROP"},
    "RAP": {"name": _("Rapeseed"), "produce": "FOOD_CROP"},
    "RCH": {"name": _("Rice (hybrid)"), "produce": "FOOD_CROP"},
    "RIC": {"name": _("Rice"), "produce": "FOOD_CROP"},
    "ROS": {"name": _("Roses"), "produce": "NON_FOOD"},
    "RUB": {"name": _("Rubber tree"), "produce": "NON_FOOD"},
    "RYE": {"name": _("Rye"), "produce": "FOOD_CROP"},
    "SEE": {"name": _("Seeds Production (unspecified)"), "produce": "FOOD_CROP"},
    "SES": {"name": _("Sesame"), "produce": "FOOD_CROP"},
    "SOR": {"name": _("Sorghum"), "produce": "FOOD_CROP"},
    "SOY": {"name": _("Soya Beans"), "produce": "FLEX_CROP"},
    "SPI": {"name": _("Spices (unspecified)")},
    "SSL": {"name": _("Sisal"), "produce": "NON_FOOD"},
    "SUB": {"name": _("Sugar beet"), "produce": "FLEX_CROP"},
    "SUC": {"name": _("Sugar Cane"), "produce": "FLEX_CROP"},
    "SUG": {"name": _("Sugar (unspecified)"), "produce": "FLEX_CROP"},
    "SUN": {"name": _("Sun Flower"), "produce": "FLEX_CROP"},
    "SWP": {"name": _("Sweet Potatoes"), "produce": "FOOD_CROP"},
    "TBC": {"name": _("Tobacco"), "produce": "NON_FOOD"},
    "TEA": {"name": _("Tea"), "produce": "FOOD_CROP"},
    "TEF": {"name": _("Teff"), "produce": "FOOD_CROP"},
    "TEK": {"name": _("Teak"), "produce": "NON_FOOD"},
    "TOM": {"name": _("Tomatoes"), "produce": "FOOD_CROP"},
    "TRE": {"name": _("Trees (unspecified)"), "produce": "NON_FOOD"},
    "VGT": {"name": _("Vegetables (unspecified)"), "produce": "FOOD_CROP"},
    "VIN": {"name": _("Vineyard"), "produce": "FOOD_CROP"},
    "WHT": {"name": _("Wheat"), "produce": "FOOD_CROP"},
    "YAM": {"name": _("Yam"), "produce": "FOOD_CROP"},
}

CROPS_CHOICES = [(k, v["name"]) for k, v in CROPS.items()]

ANIMALS = {
    "AQU": {"name": _("Aquaculture (animals)")},
    "BEE": {"name": _("Beef Cattle")},
    "CTL": {"name": _("Cattle")},
    "DCT": {"name": _("Dairy Cattle")},
    "FSH": {"name": _("Fish")},
    "GOT": {"name": _("Goats")},
    "OTH": {"name": _("Other livestock (please specify)")},
    "PIG": {"name": _("Pork")},
    "POU": {"name": _("Poultry")},
    "SHP": {"name": _("Sheep")},
    "SHR": {"name": _("Shrimp")},
}
ANIMALS_CHOICES = [(k, v["name"]) for k, v in ANIMALS.items()]

ELECTRICITY_GENERATION_OPTIONS = [
    {"value": "WIND", "label": _("On-shore wind turbines")},
    {"value": "PHOTOVOLTAIC", "label": _("Solar (Photovoltaic)")},
    {"value": "SOLAR_HEAT", "label": _("Solar (Thermal system)")},
]
ELECTRICITY_GENERATIONS_CHOICES = [
    (x["value"], x["label"]) for x in ELECTRICITY_GENERATION_OPTIONS
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

MINERALS = {
    "ALU": {"name": _("Aluminum")},
    "ASP": {"name": _("Asphaltite")},
    "ATC": {"name": _("Anthracite")},
    "BAR": {"name": _("Barite")},
    "BAS": {"name": _("Basalt")},
    "BAX": {"name": _("Bauxite")},
    "BEN": {"name": _("Bentonite")},
    "BUM": {"name": _("Building materials")},
    "CAR": {"name": _("Carbon")},
    "CHR": {"name": _("Chromite")},
    "CLA": {"name": _("Clay")},
    "COA": {"name": _("Coal")},
    "COB": {"name": _("Cobalt")},
    "COP": {"name": _("Copper")},
    "DIA": {"name": _("Diamonds")},
    "EME": {"name": _("Emerald")},
    "FLD": {"name": _("Feldspar")},
    "FLO": {"name": _("Fluoride")},
    "GAS": {"name": _("Gas")},
    "GLD": {"name": _("Gold")},
    "GRT": {"name": _("Granite")},
    "GRV": {"name": _("Gravel")},
    "HEA": {"name": _("Heavy Mineral Sands")},
    "ILM": {"name": _("Ilmenite")},
    "IRO": {"name": _("Iron")},
    "JAD": {"name": _("Jade")},
    "LED": {"name": _("Lead")},
    "LIM": {"name": _("Limestone")},
    "LIT": {"name": _("Lithium")},
    "MAG": {"name": _("Magnetite")},
    "MBD": {"name": _("Molybdenum")},
    "MGN": {"name": _("Manganese")},
    "MRB": {"name": _("Marble")},
    "NIK": {"name": _("Nickel")},
    "OTH": {"name": _("Other minerals (please specify)")},
    "PET": {"name": _("Petroleum")},
    "PHP": {"name": _("Phosphorous")},
    "PLT": {"name": _("Platinum")},
    "PUM": {"name": _("Hydrocarbons (e.g. crude oil)")},
    "PYR": {"name": _("Pyrolisis Plant")},
    "RUT": {"name": _("Rutile")},
    "SAN": {"name": _("Sand")},
    "SIC": {"name": _("Silica")},
    "SIL": {"name": _("Silver")},
    "SLT": {"name": _("Salt")},
    "STO": {"name": _("Stone")},
    "TIN": {"name": _("Tin")},
    "TTM": {"name": _("Titanium")},
    "URM": {"name": _("Uranium")},
    "ZNC": {"name": _("Zinc")},
}
MINERALS_CHOICES = [(k, v["name"]) for k, v in MINERALS.items()]

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
