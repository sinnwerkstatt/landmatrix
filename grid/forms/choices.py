from django.utils.translation import ugettext_lazy as _

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

negotiation_status_choices = (
    (_("---------"), _("---------")),
    (_("Expression of interest"), _("Expression of interest")),
    (_("Under negotiation"), _("Under negotiation")),
    (_("Memorandum of understanding"), _("Memorandum of understanding")),
    (_("Oral Agreement"), _("Oral Agreement")),
    (_("Contract signed"), _("Contract signed")),
    (_("Negotiations failed"), _("Negotiations failed")),
    (_("Contract canceled"), _("Contract canceled")),
    (_("Contract expired"), _("Contract expired")),
    (_("Change of ownership"), _("Change of ownership"))
)

implementation_status_choices = (
    (_("---------"), _("---------")),
    (_("Project not started"), _("Project not started")),
    (_("Startup phase (no production)"), _("Startup phase (no production)")),
    (_("In operation (production)"), _("In operation (production)")),
    (_("Project abandoned"), _("Project abandoned")),
)

intention_choices = (
    (_("Agriculture"), _("Agriculture"), (
        (_("Biofuels"), _("Biofuels")),
        (_("Food crops"), _("Food crops")),
        (_("Fodder"), _("Fodder")),
        (_("Livestock"), _("Livestock")),
        (_("Non-food agricultural commodities"), _("Non-food agricultural commodities")),
    )),
    (_("Forestry"), _("Forestry"), (
        (_("For wood and fibre"), _("For wood and fibre")),
        (_("For carbon sequestration/REDD"), _("For carbon sequestration/REDD")),
    )),
    (_("Logging"), _("Logging"), None),
    (_("Resource extraction (Oil, Gas, Minerals)"), _("Resource extraction (Oil, Gas, Minerals)"), None),
    (_("Tourism"), _("Tourism"), None),
    (_("Industry"), _("Industry"), None),
    (_("Conservation"), _("Conservation"), None),
    (_("Land speculation"), _("Land speculation"), None),
    (_("Renewable Energy"), _("Renewable Energy"), None),
    (_("Other (please specify)"), _("Other (please specify)"), None),
)

nature_choices = (
    (_("Outright Purchase"), _("Outright Purchase")),
    (_("Lease"), _("Lease")),
    (_("Resource exploitation license / concession"), _("Resource exploitation license / concession")),
    (_("Logging concession"), _("Logging concession")),
    (_("Pure contract farming"), _("Pure contract farming")),
)

price_type_choices = (
    (_("---------"), _("---------")),
    (_("per ha"), _("per ha")),
    (_("for specified area"), _("for specified area")),
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
