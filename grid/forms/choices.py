from django.utils.translation import ugettext_lazy as _

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

negotiation_status_choices = (
    (0, _("---------")),
    (10, _("Intended (Expression of interest)")),
    (20, _("Intended (Under negotiation)")),
    (30, _("Concluded (Oral Agreement)")),
    (40, _("Concluded (Contract signed)")),
    (50, _("Failed (Negotiations failed)")),
    (60, _("Failed (Contract canceled)")),
    (70, _("Sold"))
)

implementation_status_choices = (
    (0, _("---------")),
    (10, _("Project not started")),
    (20, _("Startup phase (no production)")),
    (30, _("In operation (production)")),
    (40, _("Project abandoned")),
)

intention_choices = (
    (10, _("Agriculture"), (
        (11, _("Biofuels")),
        (12, _("Food crops")),
        (13, _("Livestock")),
        (14, _("Non-food agricultural commodities")),
        (15, _("Agriunspecified")),
    )),
    (20, _("Forestry"), (
        (21, _("For wood and fibre")),
        (22, _("For carbon sequestration/REDD")),
        (23, _("Forestunspecified")),
    )),
    (30, _("Mining"), None),
    (40, _("Tourism"), None),
    (60, _("Industry"), None),
    (70, _("Conservation"), None),
    (80, _("Renewable Energy"), None),
    (90, _("Other (please specify)"), None),
)

nature_choices = (
    (10, _("Outright Purchase")),
    (20, _("Lease / Concession")),
    (30, _("Exploitation license")),
)

price_type_choices = (
    (0, _("---------")),
    (10, _("per ha")),
    (20, _("for specified area")),
)


def int_choice_to_string(choices):
    return ((value, value) for (key, value) in choices)

