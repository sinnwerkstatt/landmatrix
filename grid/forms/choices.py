from django.utils.translation import ugettext_lazy as _

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

negotiation_status_choices = (
    (0, _("---------")),
    (10, _("Expression of interest")),
    (20, _("Under negotiation")),
    (30, _("Memorandum of understanding")),
    (40, _("Oral Agreement")),
    (50, _("Contract signed")),
    (60, _("Negotiations failed")),
    (70, _("Contract canceled")),
    (80, _("Contract expired")),
    (90, _("Change of ownership"))
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
        (13, _("Fodder")),
        (14, _("Livestock")),
        (15, _("Non-food agricultural commodities")),
        # (16, _("Agriunspecified")),
    )),
    (20, _("Forestry"), (
        (21, _("For wood and fibre")),
        (22, _("For carbon sequestration/REDD")),
        # (23, _("Forestunspecified")),
    )),
    (30, _("Logging"), None),
    (40, _("Resource extraction (Oil, Gas, Minerals)"), None),
    (50, _("Tourism"), None),
    (60, _("Industry"), None),
    (70, _("Conservation"), None),
    (80, _("Land speculation"), None),
    (90, _("Renewable Energy"), None),
    (100, _("Other (please specify)"), None),
)

nature_choices = (
    (10, _("Outright Purchase")),
    (20, _("Lease")),
    (30, _("Resource exploitation license / concession")),
    (40, _("Logging concession")),
    (50, _("Pure contract farming")),
)

price_type_choices = (
    (0, _("---------")),
    (10, _("per ha")),
    (20, _("for specified area")),
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
