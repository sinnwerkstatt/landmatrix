"""
TODO: these are used in many DB queries! Move those to models and build
choices from them.
"""
from django.utils.translation import gettext_lazy as _

# Agriculture
INTENTION_BIOFUELS = "Biofuels"
INTENTION_FOOD_CROPS = "Food crops"
INTENTION_FODDER = "Fodder"
INTENTION_LIVESTOCK = "Livestock"
INTENTION_NON_FOOD_AGRI = "Non-food agricultural commodities"
INTENTION_AGRI_UNSPECIFIED = "Agriculture unspecified"
# Forestry
INTENTION_TIMBER_PLANTATION = "Timber plantation"
INTENTION_FOREST_LOGGING = "Forest logging / management"
INTENTION_CARBON = "For carbon sequestration/REDD"
INTENTION_FORESTRY_UNSPECIFIED = "Forestry unspecified"
# Other
INTENTION_MINING = "Mining"
INTENTION_OIL_GAS_EXTRACTION = "Oil / Gas extraction"
INTENTION_TOURISM = "Tourism"
INTENTION_INDUSTRY = "Industry"
INTENTION_CONVERSATION = "Conservation"
INTENTION_LAND_SPECULATION = "Land speculation"
INTENTION_RENEWABLE_ENERGY = "Renewable Energy"
INTENTION_OTHER = "Other"

intention_agriculture_choices = (
    (INTENTION_BIOFUELS, _("Biofuels")),
    (INTENTION_FOOD_CROPS, _("Food crops")),
    (INTENTION_FODDER, _("Fodder")),
    (INTENTION_LIVESTOCK, _("Livestock")),
    (INTENTION_NON_FOOD_AGRI, _("Non-food agricultural commodities")),
    (INTENTION_AGRI_UNSPECIFIED, _("Agriculture unspecified")),
)

INTENTION_AGRICULTURE_MAP = dict(intention_agriculture_choices)

intention_forestry_choices = (
    (INTENTION_TIMBER_PLANTATION, _("Timber plantation (for wood and fibre)")),
    (
        INTENTION_FOREST_LOGGING,
        _("Forest logging / management (for wood and fibre)"),
    ),  # new
    (INTENTION_CARBON, _("For carbon sequestration/REDD")),
    (INTENTION_FORESTRY_UNSPECIFIED, _("Forestry unspecified")),
)

INTENTION_FORESTRY_MAP = dict(intention_forestry_choices)

intention_other_choices = (
    (INTENTION_MINING, _("Mining")),
    (INTENTION_OIL_GAS_EXTRACTION, _("Oil / Gas extraction")),
    (INTENTION_TOURISM, _("Tourism")),
    (INTENTION_INDUSTRY, _("Industry")),
    (INTENTION_CONVERSATION, _("Conservation")),
    (INTENTION_LAND_SPECULATION, _("Land speculation")),
    (INTENTION_RENEWABLE_ENERGY, _("Renewable Energy")),
    (INTENTION_OTHER, _("Other (please specify)")),
)

intention_choices = (
    intention_agriculture_choices + intention_forestry_choices + intention_other_choices
)

INTENTION_MAP = dict(intention_choices)

grouped_intention_choices = (
    ("Agriculture", intention_agriculture_choices),
    ("Forestry", intention_forestry_choices),
    ("Other", intention_other_choices),
)

NATURE_OUTRIGHT_PURCHASE = "Outright purchase"
NATURE_LEASE = "Lease"
NATURE_CONCESSION = "Concession"
NATURE_EXPLOITATION_PERMIT = "Exploitation permit / license / concession"
NATURE_CONTRACT_FARMING = "Pure contract farming"
NATURE_OTHER = "Other"
nature_choices = (
    (NATURE_OUTRIGHT_PURCHASE, _("Outright purchase")),
    (NATURE_LEASE, _("Lease")),
    (NATURE_CONCESSION, _("Concession")),
    (
        NATURE_EXPLOITATION_PERMIT,
        _("Exploitation permit / license / concession (for mineral resources)"),
    ),
    (NATURE_CONTRACT_FARMING, _("Pure contract farming")),
    (NATURE_OTHER, _("Other")),
)

price_type_choices = (
    ("", _("---------")),
    ("per ha", _("per ha")),
    ("for specified area", _("for specified area")),
)

actor_choices = (
    ("", _("---------")),
    (
        "Government / State institutions",
        _(
            "Government / State institutions (government, ministries, departments, agencies etc.)"
        ),
    ),
    (
        "Traditional land-owners / communities",
        _("Traditional land-owners / communities"),
    ),
    (
        "Traditional local authority",
        _("Traditional local authority (e.g. Chiefdom council / Chiefs)"),
    ),
    ("Broker", _("Broker")),
    ("Intermediary", _("Intermediary")),
    ("Other", _("Other (please specify)")),
)
