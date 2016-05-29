from django.utils.translation import ugettext_lazy as _

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

negotiation_status_choices = (
    ('', _("---------")),
    ("Expression of interest", _("Expression of interest")),
    ("Under negotiation", _("Under negotiation")),
    ("Memorandum of understanding", _("Memorandum of understanding")),
    ("Oral Agreement", _("Oral Agreement")),
    ("Contract signed", _("Contract signed")),
    ("Negotiations failed", _("Negotiations failed")),
    ("Contract canceled", _("Contract canceled")),
    ("Contract expired", _("Contract expired")),
    ("Change of ownership", _("Change of ownership"))
)

implementation_status_choices = (
    ('', _("---------")),
    ("Project not started", _("Project not started")),
    ("Startup phase (no production)", _("Startup phase (no production)")),
    ("In operation (production)", _("In operation (production)")),
    ("Project abandoned", _("Project abandoned")),
)

intention_choices = (
    ("Agriculture", _("Agriculture"), (
        ("Biofuels", _("Biofuels")),
        ("Food crops", _("Food crops")),
        ("Fodder", _("Fodder")),
        ("Livestock", _("Livestock")),
        ("Non-food agricultural commodities", _("Non-food agricultural commodities")),
        ("Unspecified", _("Unspecified")),
    )),
    ("Forestry", _("Forestry"), (
        ("For wood and fibre", _("For wood and fibre")),
        ("For carbon sequestration/REDD", _("For carbon sequestration/REDD")),
        ("Unspecified", _("Unspecified")),
    )),
    ("Logging", _("Logging"), None),
    ("Resource extraction (Oil, Gas, Minerals)", _("Resource extraction (Oil, Gas, Minerals)"), None),
    ("Tourism", _("Tourism"), None),
    ("Industry", _("Industry"), None),
    ("Conservation", _("Conservation"), None),
    ("Land speculation", _("Land speculation"), None),
    ("Renewable Energy", _("Renewable Energy"), None),
    ("Other (please specify)", _("Other (please specify)"), None),
)

nature_choices = (
    ("Outright Purchase", _("Outright Purchase")),
    ("Lease", _("Lease")),
    ("Resource exploitation license / concession", _("Resource exploitation license / concession")),
    ("Logging concession", _("Logging concession")),
    ("Pure contract farming", _("Pure contract farming")),
)

price_type_choices = (
    ('', _("---------")),
    ("per ha", _("per ha")),
    ("for specified area", _("for specified area")),
)


def int_choice_to_string(choices):
    if choices and len(choices[0]) == 3:
        for key, value, sub_choices in choices:
            if sub_choices:
                yield (value, value, int_choice_to_string(sub_choices))
            else:
                yield (value, value, None)
    elif choices and len(choices[0]) == 2:
        for key, value in choices:
            yield (value, value)


def get_choice_parent(selected_choice, choices):
    for parent_choice in int_choice_to_string(choices):
        if len(parent_choice) != 3:
            break
        child_choices = parent_choice[2]
        if child_choices:
            for child_choice in child_choices:
                if child_choice[0] == selected_choice:
                    return parent_choice[0]

    return None
