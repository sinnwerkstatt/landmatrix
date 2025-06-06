import { _ } from "svelte-i18n"
import { derived } from "svelte/store"

import type { components } from "$lib/openAPI"

export const dealChoices = derived(_, $_ => {
  return {
    intention_of_investment: [
      { value: "BIOFUELS", label: $_("Biomass for biofuels"), group: "AGRICULTURE" },
      {
        value: "BIOMASS_ENERGY_GENERATION",
        label: $_("Biomass for energy generation (agriculture)"),
        group: "AGRICULTURE",
      },
      { value: "FODDER", label: $_("Fodder"), group: "AGRICULTURE" },
      { value: "FOOD_CROPS", label: $_("Food crops"), group: "AGRICULTURE" },
      { value: "LIVESTOCK", label: $_("Livestock"), group: "AGRICULTURE" },
      {
        value: "NON_FOOD_AGRICULTURE",
        label: $_("Non-food agricultural commodities"),
        group: "AGRICULTURE",
      },
      {
        value: "AGRICULTURE_UNSPECIFIED",
        label: $_("Agriculture unspecified"),
        group: "AGRICULTURE",
      },
      {
        value: "BIOMASS_ENERGY_PRODUCTION",
        label: $_("Biomass for energy generation (forestry)"),
        group: "FORESTRY",
      },
      {
        value: "CARBON",
        label: $_("For carbon sequestration/REDD"),
        group: "FORESTRY",
      },
      {
        value: "FOREST_LOGGING",
        label: $_("Forest logging / management for wood and fiber"),
        group: "FORESTRY",
      },
      {
        value: "TIMBER_PLANTATION",
        label: $_("Timber plantation for wood and fiber"),
        group: "FORESTRY",
      },
      {
        value: "FORESTRY_UNSPECIFIED",
        label: $_("Forestry unspecified"),
        group: "FORESTRY",
      },
      { value: "SOLAR_PARK", label: $_("Solar park"), group: "RENEWABLE_ENERGY" },
      { value: "WIND_FARM", label: $_("Wind farm"), group: "RENEWABLE_ENERGY" },
      {
        value: "RENEWABLE_ENERGY",
        label: $_("Renewable energy unspecified"),
        group: "RENEWABLE_ENERGY",
      },
      { value: "CONVERSATION", label: $_("Conservation"), group: "OTHER" },
      { value: "INDUSTRY", label: $_("Industry"), group: "OTHER" },
      { value: "LAND_SPECULATION", label: $_("Land speculation"), group: "OTHER" },
      { value: "MINING", label: $_("Mining"), group: "OTHER" },
      {
        value: "OIL_GAS_EXTRACTION",
        label: $_("Oil / Gas extraction"),
        group: "OTHER",
      },
      { value: "TOURISM", label: $_("Tourism"), group: "OTHER" },
      { value: "OTHER", label: $_("Other"), group: "OTHER" },
    ],
    intention_of_investment_group: [
      { value: "AGRICULTURE", label: $_("Agriculture") },
      { value: "FORESTRY", label: $_("Forestry") },
      { value: "RENEWABLE_ENERGY", label: $_("Renewable energy power plants") },
      { value: "OTHER", label: $_("Other") },
    ],
    negotiation_status: [
      {
        value: "EXPRESSION_OF_INTEREST",
        label: $_("Intended (Expression of interest)"),
        group: "INTENDED",
      },
      {
        value: "UNDER_NEGOTIATION",
        label: $_("Intended (Under negotiation)"),
        group: "INTENDED",
      },
      {
        value: "MEMORANDUM_OF_UNDERSTANDING",
        label: $_("Intended (Memorandum of understanding)"),
        group: "INTENDED",
      },
      {
        value: "ORAL_AGREEMENT",
        label: $_("Concluded (Oral Agreement)"),
        group: "CONCLUDED",
      },
      {
        value: "CONTRACT_SIGNED",
        label: $_("Concluded (Contract signed)"),
        group: "CONCLUDED",
      },
      {
        value: "CHANGE_OF_OWNERSHIP",
        label: $_("Concluded (Change of ownership)"),
        group: "CONCLUDED",
      },
      {
        value: "NEGOTIATIONS_FAILED",
        label: $_("Failed (Negotiations failed)"),
        group: "FAILED",
      },
      {
        value: "CONTRACT_CANCELED",
        label: $_("Failed (Contract cancelled)"),
        group: "FAILED",
      },
      {
        value: "CONTRACT_EXPIRED",
        label: $_("Contract expired"),
        group: "CONTRACT_EXPIRED",
      },
    ],
    negotiation_status_group: [
      { value: "INTENDED", label: $_("Intended") },
      { value: "CONCLUDED", label: $_("Concluded") },
      { value: "FAILED", label: $_("Failed") },
      { value: "CONTRACT_EXPIRED", label: $_("Contract expired") },
    ],
    implementation_status: [
      { value: "PROJECT_NOT_STARTED", label: $_("Project not started") },
      { value: "STARTUP_PHASE", label: $_("Startup phase (no production)") },
      { value: "IN_OPERATION", label: $_("In operation (production)") },
      { value: "PROJECT_ABANDONED", label: $_("Project abandoned") },
    ],
    level_of_accuracy: [
      { value: "COUNTRY", label: $_("Country") },
      { value: "ADMINISTRATIVE_REGION", label: $_("Administrative region") },
      { value: "APPROXIMATE_LOCATION", label: $_("Approximate location") },
      { value: "EXACT_LOCATION", label: $_("Exact location") },
      { value: "COORDINATES", label: $_("Coordinates") },
    ],
    nature_of_deal: [
      { value: "OUTRIGHT_PURCHASE", label: $_("Outright purchase") },
      { value: "LEASE", label: $_("Lease") },
      { value: "CONCESSION", label: $_("Concession") },
      {
        value: "EXPLOITATION_PERMIT",
        label: $_("Exploitation permit / license / concession (for mineral resources)"),
      },
      { value: "PURE_CONTRACT_FARMING", label: $_("Pure contract farming") },
      { value: "OTHER", label: $_("Other") },
    ],
    recognition_status: [
      {
        value: "INDIGENOUS_RIGHTS_RECOGNIZED",
        label: $_(
          "Indigenous Peoples traditional or customary rights recognized by government",
        ),
      },
      {
        value: "INDIGENOUS_RIGHTS_NOT_RECOGNIZED",
        label: $_(
          "Indigenous Peoples traditional or customary rights not recognized by government",
        ),
      },
      {
        value: "COMMUNITY_RIGHTS_RECOGNIZED",
        label: $_("Community traditional or customary rights recognized by government"),
      },
      {
        value: "COMMUNITY_RIGHTS_NOT_RECOGNIZED",
        label: $_(
          "Community traditional or customary rights not recognized by government",
        ),
      },
    ],
    negative_impacts: [
      { value: "ENVIRONMENTAL_DEGRADATION", label: $_("Environmental degradation") },
      { value: "SOCIO_ECONOMIC", label: $_("Socio-economic") },
      { value: "CULTURAL_LOSS", label: $_("Cultural loss") },
      { value: "EVICTION", label: $_("Eviction") },
      { value: "DISPLACEMENT", label: $_("Displacement") },
      { value: "VIOLENCE", label: $_("Violence") },
      { value: "OTHER", label: $_("Other") },
    ],
    benefits: [
      { value: "HEALTH", label: $_("Health") },
      { value: "EDUCATION", label: $_("Education") },
      {
        value: "PRODUCTIVE_INFRASTRUCTURE",
        label: $_(
          "Productive infrastructure (e.g. irrigation, tractors, machinery...)",
        ),
      },
      { value: "ROADS", label: $_("Roads") },
      { value: "CAPACITY_BUILDING", label: $_("Capacity building") },
      { value: "FINANCIAL_SUPPORT", label: $_("Financial support") },
      {
        value: "COMMUNITY_SHARES",
        label: $_("Community shares in the investment project"),
      },
      { value: "OTHER", label: $_("Other") },
    ],
    former_land_owner: [
      { value: "STATE", label: $_("State") },
      { value: "PRIVATE_SMALLHOLDERS", label: $_("Private (smallholders)") },
      { value: "PRIVATE_LARGE_SCALE", label: $_("Private (large-scale farm)") },
      { value: "COMMUNITY", label: $_("Community") },
      { value: "INDIGENOUS_PEOPLE", label: $_("Indigenous people") },
      { value: "OTHER", label: $_("Other") },
    ],
    former_land_use: [
      {
        value: "COMMERCIAL_AGRICULTURE",
        label: $_("Commercial (large-scale) agriculture"),
      },
      { value: "SMALLHOLDER_AGRICULTURE", label: $_("Smallholder agriculture") },
      { value: "SHIFTING_CULTIVATION", label: $_("Shifting cultivation") },
      { value: "PASTORALISM", label: $_("Pastoralism") },
      { value: "HUNTING_GATHERING", label: $_("Hunting/Gathering") },
      { value: "FORESTRY", label: $_("Forestry") },
      { value: "CONSERVATION", label: $_("Conservation") },
      { value: "OTHER", label: $_("Other") },
    ],
    ha_area: [
      { value: "PER_HA", label: $_("per ha") },
      { value: "PER_AREA", label: $_("for specified area") },
    ],
    community_consultation: [
      { value: "NOT_CONSULTED", label: $_("Not consulted") },
      { value: "LIMITED_CONSULTATION", label: $_("Limited consultation") },
      { value: "FPIC", label: $_("Free, Prior and Informed Consent (FPIC)") },
      { value: "OTHER", label: $_("Other") },
    ],
    community_reaction: [
      { value: "CONSENT", label: $_("Consent") },
      { value: "MIXED_REACTION", label: $_("Mixed reaction") },
      { value: "REJECTION", label: $_("Rejection") },
    ],
    former_land_cover: [
      { value: "CROPLAND", label: $_("Cropland") },
      { value: "FOREST_LAND", label: $_("Forest land") },
      { value: "PASTURE", label: $_("Pasture") },
      { value: "RANGELAND", label: $_("Shrub land/Grassland (Rangeland)") },
      { value: "MARGINAL_LAND", label: $_("Marginal land") },
      { value: "WETLAND", label: $_("Wetland") },
      { value: "OTHER_LAND", label: $_("Other land (e.g. developed land)") },
    ],
    crops: [
      { value: "ACC", label: $_("Accacia"), produce: "NON_FOOD" },
      { value: "ALF", label: $_("Alfalfa"), produce: "NON_FOOD" },
      {
        value: "ALG",
        label: $_("Seaweed / Macroalgae(unspecified)"),
        produce: "NON_FOOD",
      },
      { value: "ALM", label: $_("Almond"), produce: "FOOD_CROP" },
      { value: "ALV", label: $_("Aloe Vera"), produce: "NON_FOOD" },
      { value: "APL", label: $_("Apple"), produce: "FOOD_CROP" },
      {
        value: "AQU",
        label: $_("Aquaculture (unspecified crops)"),
        produce: "FOOD_CROP",
      },
      { value: "BAM", label: $_("Bamboo"), produce: "NON_FOOD" },
      { value: "BAN", label: $_("Banana"), produce: "FOOD_CROP" },
      { value: "BEA", label: $_("Bean"), produce: "FOOD_CROP" },
      { value: "BOT", label: $_("Bottle Gourd"), produce: "FOOD_CROP" },
      { value: "BRL", label: $_("Barley"), produce: "FOOD_CROP" },
      { value: "BWT", label: $_("Buckwheat"), produce: "FOOD_CROP" },
      { value: "CAC", label: $_("Cacao"), produce: "FOOD_CROP" },
      { value: "CAS", label: $_("Cassava (Maniok)"), produce: "FOOD_CROP" },
      { value: "CAW", label: $_("Cashew"), produce: "FOOD_CROP" },
      { value: "CHA", label: $_("Chat") },
      { value: "CHE", label: $_("Cherries"), produce: "FOOD_CROP" },
      { value: "CNL", label: $_("Canola"), produce: "FLEX_CROP" },
      { value: "COC", label: $_("Coconut"), produce: "FOOD_CROP" },
      { value: "COF", label: $_("Coffee Plant"), produce: "FOOD_CROP" },
      { value: "COT", label: $_("Cotton"), produce: "NON_FOOD" },
      { value: "CRL", label: $_("Cereals (unspecified)"), produce: "FOOD_CROP" },
      { value: "CRN", label: $_("Corn (Maize)"), produce: "FOOD_CROP" },
      { value: "CRO", label: $_("Croton"), produce: "NON_FOOD" },
      { value: "CST", label: $_("Castor Oil Plant"), produce: "NON_FOOD" },
      { value: "CTR", label: $_("Citrus Fruits (unspecified)"), produce: "FOOD_CROP" },
      { value: "DIL", label: $_("Dill"), produce: "NON_FOOD" },
      { value: "EUC", label: $_("Eucalyptus"), produce: "NON_FOOD" },
      { value: "FLW", label: $_("Flowers (unspecified)"), produce: "NON_FOOD" },
      { value: "FNT", label: $_("Fig-Nut"), produce: "FOOD_CROP" },
      { value: "FOD", label: $_("Fodder Plants (unspecified)"), produce: "NON_FOOD" },
      { value: "FOO", label: $_("Food crops (unspecified)"), produce: "FOOD_CROP" },
      { value: "FRT", label: $_("Fruit (unspecified)"), produce: "FOOD_CROP" },
      { value: "GRA", label: $_("Grapes"), produce: "FOOD_CROP" },
      { value: "GRN", label: $_("Grains (unspecified)"), produce: "FOOD_CROP" },
      { value: "HRB", label: $_("Herbs (unspecified)") },
      { value: "JTR", label: $_("Jatropha"), produce: "NON_FOOD" },
      { value: "LNT", label: $_("Lentils"), produce: "FOOD_CROP" },
      { value: "MAN", label: $_("Mango"), produce: "FOOD_CROP" },
      { value: "MUS", label: $_("Mustard"), produce: "FOOD_CROP" },
      { value: "OAT", label: $_("Oats") },
      { value: "OIL", label: $_("Oil Seeds (unspecified)"), produce: "FLEX_CROP" },
      { value: "OLE", label: $_("Oleagionous plant"), produce: "FLEX_CROP" },
      { value: "OLV", label: $_("Olives"), produce: "FOOD_CROP" },
      { value: "ONI", label: $_("Onion"), produce: "FOOD_CROP" },
      { value: "OPL", label: $_("Oil Palm"), produce: "FLEX_CROP" },
      { value: "OTH", label: $_("Other crops") },
      { value: "PAL", label: $_("Palms"), produce: "FOOD_CROP" },
      { value: "PAP", label: $_("Papaya"), produce: "FOOD_CROP" },
      { value: "PAS", label: $_("Passion fruit"), produce: "FOOD_CROP" },
      { value: "PEA", label: $_("Peanut (groundnut)"), produce: "FOOD_CROP" },
      { value: "PEP", label: $_("Pepper"), produce: "FOOD_CROP" },
      { value: "PES", label: $_("Peas"), produce: "FOOD_CROP" },
      { value: "PIE", label: $_("Pine"), produce: "FOOD_CROP" },
      { value: "PIN", label: $_("Pineapple"), produce: "FOOD_CROP" },
      { value: "PLS", label: $_("Pulses (unspecified)"), produce: "FOOD_CROP" },
      { value: "POM", label: $_("Pomegranate"), produce: "FOOD_CROP" },
      { value: "PON", label: $_("Pongamia Pinnata"), produce: "NON_FOOD" },
      { value: "PTT", label: $_("Potatoes"), produce: "FOOD_CROP" },
      { value: "RAP", label: $_("Rapeseed"), produce: "FOOD_CROP" },
      { value: "RCH", label: $_("Rice (hybrid)"), produce: "FOOD_CROP" },
      { value: "RIC", label: $_("Rice"), produce: "FOOD_CROP" },
      { value: "ROS", label: $_("Roses"), produce: "NON_FOOD" },
      { value: "RUB", label: $_("Rubber tree"), produce: "NON_FOOD" },
      { value: "RYE", label: $_("Rye"), produce: "FOOD_CROP" },
      {
        value: "SEE",
        label: $_("Seeds Production (unspecified)"),
        produce: "FOOD_CROP",
      },
      { value: "SES", label: $_("Sesame"), produce: "FOOD_CROP" },
      { value: "SOR", label: $_("Sorghum"), produce: "FOOD_CROP" },
      { value: "SOY", label: $_("Soya Beans"), produce: "FLEX_CROP" },
      { value: "SPI", label: $_("Spices (unspecified)") },
      { value: "SSL", label: $_("Sisal"), produce: "NON_FOOD" },
      { value: "SUB", label: $_("Sugar beet"), produce: "FLEX_CROP" },
      { value: "SUC", label: $_("Sugar Cane"), produce: "FLEX_CROP" },
      { value: "SUG", label: $_("Sugar (unspecified)"), produce: "FLEX_CROP" },
      { value: "SUN", label: $_("Sun Flower"), produce: "FLEX_CROP" },
      { value: "SWP", label: $_("Sweet Potatoes"), produce: "FOOD_CROP" },
      { value: "TBC", label: $_("Tobacco"), produce: "NON_FOOD" },
      { value: "TEA", label: $_("Tea"), produce: "FOOD_CROP" },
      { value: "TEF", label: $_("Teff"), produce: "FOOD_CROP" },
      { value: "TEK", label: $_("Teak"), produce: "NON_FOOD" },
      { value: "TOM", label: $_("Tomatoes"), produce: "FOOD_CROP" },
      { value: "TRE", label: $_("Trees (unspecified)"), produce: "NON_FOOD" },
      { value: "VGT", label: $_("Vegetables (unspecified)"), produce: "FOOD_CROP" },
      { value: "VIN", label: $_("Vineyard"), produce: "FOOD_CROP" },
      { value: "WHT", label: $_("Wheat"), produce: "FOOD_CROP" },
      { value: "YAM", label: $_("Yam"), produce: "FOOD_CROP" },
    ],
    animals: [
      { value: "AQU", label: $_("Aquaculture (animals)") },
      { value: "BEE", label: $_("Beef Cattle") },
      { value: "CTL", label: $_("Cattle") },
      { value: "DCT", label: $_("Dairy Cattle") },
      { value: "FSH", label: $_("Fish") },
      { value: "GOT", label: $_("Goats") },
      { value: "OTH", label: $_("Other livestock") },
      { value: "PIG", label: $_("Pork") },
      { value: "POU", label: $_("Poultry") },
      { value: "SHP", label: $_("Sheep") },
      { value: "SHR", label: $_("Shrimp") },
    ],
    electricity_generation: [
      { value: "WIND", label: $_("On-shore wind turbines") },
      { value: "PHOTOVOLTAIC", label: $_("Solar (Photovoltaic)") },
      { value: "SOLAR_HEAT", label: $_("Solar (Thermal system)") },
    ],
    carbon_sequestration: [
      { value: "REFORESTATION", label: $_("Reforestation & afforestation") },
      { value: "AVOIDED_FOREST_CONVERSION", label: $_("Avoided forest conversion") },
      {
        value: "AVOIDED_GRASSLAND_CONVERSION",
        label: $_("Avoided grassland conversion"),
      },
      { value: "PEATLAND_RESTORATION", label: $_("Peatland restoration") },
      { value: "IMPROVED_FOREST_MANAGEMENT", label: $_("Improved forest management") },
      { value: "SUSTAINABLE_AGRICULTURE", label: $_("Sustainable agriculture") },
      {
        value: "SUSTAINABLE_GRASSLAND_MANAGEMENT",
        label: $_("Sustainable grassland management"),
      },
      { value: "RICE_EMISSION_REDUCTIONS", label: $_("Rice emission reductions") },
      { value: "SOLAR_PARK", label: $_("Solar park") },
      { value: "WIND_FARM", label: $_("Wind farm") },
      { value: "OTHER", label: $_("Other") },
    ],
    carbon_sequestration_certs: [
      { value: "REDD", label: $_("REDD+") },
      { value: "VCS", label: $_("Verified Carbon Standard (VCS)") },
      { value: "GOLD", label: $_("Gold Standard for the Global Goals (GOLD)") },
      { value: "CDM", label: $_("Clean Development Mechanism (CDM)") },
      { value: "CAR", label: $_("Climate Action Reserve (CAR)") },
      { value: "VIVO", label: $_("Plan Vivo") },
      { value: "OTHER", label: $_("Other") },
    ],
    minerals: [
      { value: "ALU", label: $_("Aluminum") },
      { value: "ASP", label: $_("Asphaltite") },
      { value: "ATC", label: $_("Anthracite") },
      { value: "BAR", label: $_("Barite") },
      { value: "BAS", label: $_("Basalt") },
      { value: "BAX", label: $_("Bauxite") },
      { value: "BEN", label: $_("Bentonite") },
      { value: "BUM", label: $_("Building materials") },
      { value: "CAR", label: $_("Carbon") },
      { value: "CHR", label: $_("Chromite") },
      { value: "CLA", label: $_("Clay") },
      { value: "COA", label: $_("Coal") },
      { value: "COB", label: $_("Cobalt") },
      { value: "COP", label: $_("Copper") },
      { value: "DIA", label: $_("Diamonds") },
      { value: "EME", label: $_("Emerald") },
      { value: "FLD", label: $_("Feldspar") },
      { value: "FLO", label: $_("Fluoride") },
      { value: "GAS", label: $_("Gas") },
      { value: "GLD", label: $_("Gold") },
      { value: "GRT", label: $_("Granite") },
      { value: "GRV", label: $_("Gravel") },
      { value: "HEA", label: $_("Heavy Mineral Sands") },
      { value: "ILM", label: $_("Ilmenite") },
      { value: "IRO", label: $_("Iron") },
      { value: "JAD", label: $_("Jade") },
      { value: "LED", label: $_("Lead") },
      { value: "LIM", label: $_("Limestone") },
      { value: "LIT", label: $_("Lithium") },
      { value: "MAG", label: $_("Magnetite") },
      { value: "MBD", label: $_("Molybdenum") },
      { value: "MGN", label: $_("Manganese") },
      { value: "MRB", label: $_("Marble") },
      { value: "NIK", label: $_("Nickel") },
      { value: "OTH", label: $_("Other minerals") },
      { value: "PET", label: $_("Petroleum") },
      { value: "PHP", label: $_("Phosphorous") },
      { value: "PLT", label: $_("Platinum") },
      { value: "PUM", label: $_("Hydrocarbons (e.g. crude oil)") },
      { value: "PYR", label: $_("Pyrolisis Plant") },
      { value: "RUT", label: $_("Rutile") },
      { value: "SAN", label: $_("Sand") },
      { value: "SIC", label: $_("Silica") },
      { value: "SIL", label: $_("Silver") },
      { value: "SLT", label: $_("Salt") },
      { value: "STO", label: $_("Stone") },
      { value: "TIN", label: $_("Tin") },
      { value: "TTM", label: $_("Titanium") },
      { value: "URM", label: $_("Uranium") },
      { value: "ZNC", label: $_("Zinc") },
    ],
    water_source: [
      { value: "GROUNDWATER", label: $_("Groundwater") },
      { value: "SURFACE_WATER", label: $_("Surface water") },
      { value: "RIVER", label: $_("River") },
      { value: "LAKE", label: $_("Lake") },
    ],
    not_public_reason: [
      { value: "CONFIDENTIAL", label: $_("Confidential flag") },
      { value: "NO_COUNTRY", label: $_("No country") },
      { value: "HIGH_INCOME_COUNTRY", label: $_("High-income country") },
      { value: "NO_DATASOURCES", label: $_("No datasources") },
      { value: "NO_OPERATING_COMPANY", label: $_("No operating company") },
      { value: "NO_KNOWN_INVESTOR", label: $_("No known investor") },
    ],
    actors: [
      {
        value: "GOVERNMENT_OR_STATE_INSTITUTIONS",
        label: $_(
          "Government / state institutions (government, ministries, departments, agencies etc.)",
        ),
      },
      {
        value: "TRADITIONAL_LAND_OWNERS_OR_COMMUNITIES",
        label: $_("Traditional land-owners / communities"),
      },
      {
        value: "TRADITIONAL_LOCAL_AUTHORITY",
        label: $_("Traditional local authority (e.g. Chiefdom council / Chiefs)"),
      },
      { value: "BROKER", label: $_("Broker") },
      { value: "INTERMEDIARY", label: $_("Intermediary") },
      { value: "OTHER", label: $_("Other") },
    ],
    produce_group: [
      { value: "CROPS", label: $_("Crops") },
      { value: "ANIMALS", label: $_("Livestock") },
      { value: "MINERAL_RESOURCES", label: $_("Mineral resources") },
    ],
  }
})

export const datasourceChoices = derived(_, $_ => {
  return {
    type: [
      { value: "MEDIA_REPORT", label: $_("Media report") },
      {
        value: "RESEARCH_PAPER_OR_POLICY_REPORT",
        label: $_("Research Paper / Policy Report"),
      },
      { value: "GOVERNMENT_SOURCES", label: $_("Government sources") },
      { value: "COMPANY_SOURCES", label: $_("Company sources") },
      { value: "CONTRACT", label: $_("Contract") },
      {
        value: "CONTRACT_FARMING_AGREEMENT",
        label: $_("Contract (contract farming agreement)"),
      },
      { value: "PERSONAL_INFORMATION", label: $_("Personal information") },
      { value: "CROWDSOURCING", label: $_("Crowdsourcing") },
      { value: "OTHER", label: $_("Other") },
    ],
  }
})
export const investorChoices = derived(_, $_ => {
  return {
    classification: [
      { value: "GOVERNMENT", label: $_("Government") },
      { value: "GOVERNMENT_INSTITUTION", label: $_("Government institution") },
      { value: "STATE_OWNED_COMPANY", label: $_("State-/government (owned) company") },
      { value: "SEMI_STATE_OWNED_COMPANY", label: $_("Semi state-owned company") },
      { value: "ASSET_MANAGEMENT_FIRM", label: $_("Asset management firm") },
      {
        value: "BILATERAL_DEVELOPMENT_BANK",
        label: $_("Bilateral Development Bank / Development Finance Institution"),
      },
      {
        value: "STOCK_EXCHANGE_LISTED_COMPANY",
        label: $_("Stock-exchange listed company"),
      },
      { value: "COMMERCIAL_BANK", label: $_("Commercial Bank") },
      { value: "INSURANCE_FIRM", label: $_("Insurance firm") },
      { value: "INVESTMENT_BANK", label: $_("Investment Bank") },
      { value: "INVESTMENT_FUND", label: $_("Investment fund") },
      {
        value: "MULTILATERAL_DEVELOPMENT_BANK",
        label: $_("Multilateral Development Bank (MDB)"),
      },
      { value: "PRIVATE_COMPANY", label: $_("Private company") },
      { value: "PRIVATE_EQUITY_FIRM", label: $_("Private equity firm") },
      { value: "INDIVIDUAL_ENTREPRENEUR", label: $_("Individual entrepreneur") },
      {
        value: "NON_PROFIT",
        label: $_("Non - Profit organization (e.g. Church, University etc.)"),
      },
      { value: "OTHER", label: $_("Other") },
    ],
  }
})

export const involvementChoices = derived(_, $_ => {
  return {
    role: [
      { value: "PARENT", label: $_("Parent company") },
      { value: "LENDER", label: $_("Tertiary investor/lender") },
    ],
    investment_type: [
      { value: "EQUITY", label: $_("Shares/Equity") },
      { value: "DEBT_FINANCING", label: $_("Debt financing") },
    ],
    parent_relation: [
      { value: "SUBSIDIARY", label: $_("Subsidiary of parent company") },
      { value: "LOCAL_BRANCH", label: $_("Local branch of parent company") },
      { value: "JOINT_VENTURE", label: $_("Joint venture of parent companies") },
    ],
  }
})

export const areaChoices = derived(_, $_ => {
  return {
    type: [
      { value: "production_area", label: $_("Production area") },
      { value: "contract_area", label: $_("Contract area") },
      { value: "intended_area", label: $_("Intended area") },
    ],
  }
})

export type ValueLabelEntry = components["schemas"]["ValueLabel"]
export const createGroupMap = <T extends Record<string, string>>(
  choices: ValueLabelEntry[],
): T =>
  choices.reduce(
    (acc, { value, group }) => ({
      ...acc,
      [value]: group as string,
    }),
    {} as T,
  )
export const createLabels = <T extends string>(
  choices: ValueLabelEntry[],
): { [key in T]: string } =>
  choices.reduce(
    (acc, { value, label }) => ({
      ...acc,
      [value]: label,
    }),
    {} as { [key in T]: string },
  )
