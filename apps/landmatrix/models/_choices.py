from django.utils.translation import gettext as _

INTENTION_CHOICES = [
    ("BIOFUELS", _("Biofuels")),
    ("FOOD_CROPS", _("Food crops")),
    ("FODDER", _("Fodder")),
    ("LIVESTOCK", _("Livestock")),
    ("NON_FOOD_AGRICULTURE", _("Non-food agricultural commodities")),
    ("AGRICULTURE_UNSPECIFIED", _("Agriculture unspecified")),
    ("TIMBER_PLANTATION", _("Timber plantation")),
    ("FOREST_LOGGING", _("Forest logging / management")),
    ("CARBON", _("For carbon sequestration/REDD")),
    ("FORESTRY_UNSPECIFIED", _("Forestry unspecified")),
    ("MINING", _("Mining")),
    ("OIL_GAS_EXTRACTION", _("Oil / Gas extraction")),
    ("TOURISM", _("Tourism")),
    ("INDUSTRY", _("Industry")),
    ("CONVERSATION", _("Conservation")),
    ("LAND_SPECULATION", _("Land speculation")),
    ("RENEWABLE_ENERGY", _("Renewable energy")),
    ("OTHER", _("Other")),
]

NEGOTIATION_STATUS_CHOICES = [
    ("EXPRESSION_OF_INTEREST", _("Intended (Expression of interest)")),
    ("UNDER_NEGOTIATION", _("Intended (Under negotiation)")),
    ("MEMORANDUM_OF_UNDERSTANDING", _("Intended (Memorandum of understanding)")),
    ("ORAL_AGREEMENT", _("Concluded (Oral Agreement)")),
    ("CONTRACT_SIGNED", _("Concluded (Contract signed)")),
    ("NEGOTIATIONS_FAILED", _("Failed (Negotiations failed)")),
    ("CONTRACT_CANCELED", _("Failed (Contract cancelled)")),
    ("CONTRACT_EXPIRED", _("Contract expired")),
    ("CHANGE_OF_OWNERSHIP", _("Change of ownership")),
]

IMPLEMENTATION_STATUS_CHOICES = (
    ("PROJECT_NOT_STARTED", "Project not started"),
    ("STARTUP_PHASE", "Startup phase (no production)"),
    ("IN_OPERATION", "In operation (production)"),
    ("PROJECT_ABANDONED", "Project abandoned"),
)

ACTOR_MAP = (
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
)
