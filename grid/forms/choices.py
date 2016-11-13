'''
TODO: these are used in many DB queries! Move those to models and build
choices from them.
'''
from django.utils.translation import ugettext_lazy as _




intention_agriculture_choices = (
    ("Biofuels", _("Biofuels")),
    ("Food crops", _("Food crops")),
    ("Fodder", _("Fodder")),
    ("Livestock", _("Livestock")),
    ("Non-food agricultural commodities", _("Non-food agricultural commodities")),
    ("Agriculture unspecified", _("Agriculture unspecified")),
)

INTENTION_AGRICULTURE_MAP = dict(intention_agriculture_choices)

intention_forestry_choices = (
    ("For wood and fibre", _("For wood and fibre")),
    ("For carbon sequestration/REDD", _("For carbon sequestration/REDD")),
    ("Forestry unspecified", _("Forestry unspecified")),
)

INTENTION_FORESTRY_MAP = dict(intention_forestry_choices)

intention_other_choices = (
    ("Logging", _("Logging")),
    ("Resource extraction", _("Resource extraction (Oil, Gas, Minerals)")),
    ("Tourism", _("Tourism")),
    ("Industry", _("Industry")),
    ("Conservation", _("Conservation")),
    ("Land speculation", _("Land speculation")),
    ("Renewable Energy", _("Renewable Energy")),
    ("Other", _("Other (please specify)")),
)

intention_choices = intention_agriculture_choices + intention_forestry_choices + intention_other_choices

INTENTION_MAP = dict(intention_choices)

grouped_intention_choices = (
    ("Agriculture", intention_agriculture_choices),
    ("Forestry", intention_forestry_choices),
    ("Other", intention_other_choices),
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

actor_choices = (
    ('', _("---------")),
    ('Government / State institutions', _("Government / State institutions (government, ministries, departments, agencies etc.)")),
    ('Traditional land-owners / communities', _("Traditional land-owners / communities")),
    ('Traditional local authority', _("Traditional local authority (e.g. Chiefdom council / Chiefs)")),
    ('Broker', _("Broker")),
    ('Intermediary', _("Intermediary")),
    ('Other', _("Other (please specify)")),
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
