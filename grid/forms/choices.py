'''
TODO: these are used in many DB queries! Move those to models and build
choices from them.
'''
from django.utils.translation import ugettext_lazy as _


__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


negotiation_status_choices = (
    ('', _("---------")),
    ("Expression of interest", _("Intended (Expression of interest)")),
    ("Under negotiation", _("Intended (Under negotiation)")),
    ("Memorandum of understanding", _("Intended (Memorandum of understanding)")),
    ("Oral agreement", _("Concluded (Oral Agreement)")),
    ("Contract signed", _("Concluded (Contract signed)")),
    ("Negotiations failed", _("Failed (Negotiations failed)")),
    ("Contract canceled", _("Failed (Contract canceled)")),
    ("Contract expired", _("Failed (Contract expired)")),
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
        ("Agriculture unspecified", _("Unspecified")),
    )),
    ("Forestry", _("Forestry"), (
        ("For wood and fibre", _("For wood and fibre")),
        ("For carbon sequestration/REDD", _("For carbon sequestration/REDD")),
        ("Forestry unspecified", _("Unspecified")),
    )),
    ("Logging", _("Logging"), None),
    ("Resource extraction", _("Resource extraction (Oil, Gas, Minerals)"), None),
    ("Tourism", _("Tourism"), None),
    ("Industry", _("Industry"), None),
    ("Conservation", _("Conservation"), None),
    ("Land speculation", _("Land speculation"), None),
    ("Renewable Energy", _("Renewable Energy"), None),
    ("Other", _("Other (please specify)"), None),
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

operational_company_choices = (
    ('10', _("Private company")),
    ('20', _("Stock-exchange listed company")),
    ('30', _("Individual entrepreneur")),
    ('40', _("Investment fund")),
    ('50', _("Semi state-owned company")),
    ('60', _("State-/government (owned) company")),
    ('70', _("Other (please specify in comment field)")),
)

investor_choices = (
    ('110', _("Government")),
    ('120', _("Government institution")),
    ('130', _("Multilateral Development Bank (MDB)")),
    ('140', _("Bilateral Development Bank / Development Finance Institution")),
    ('150', _("Commercial Bank")),
    ('160', _("Investment Bank")),
    ('170', _("Investment Fund (all types incl. pension, hedge, mutual, private equity funds etc.)")),
    ('180', _("Insurance firm")),
    ('190', _("Private equity firm")),
    ('200', _("Asset management firm")),
    ('210', _("Non - Profit organization (e.g. Church, University etc.)")),
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
