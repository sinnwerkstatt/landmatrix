from mapping.map_model import MapModel
import landmatrix.models
import old_editor.models
from mapping.aux_functions import get_first_stakeholder_tag_value, get_country_id_for_stakeholder, get_now



def get_name_for_stakeholder(stakeholder_id):
    investor_name = get_first_stakeholder_tag_value(stakeholder_id, 'investor_name')
    return '' if investor_name is None else investor_name


def get_classification_for_stakeholder(stakeholder_id):
    classification = get_first_stakeholder_tag_value(stakeholder_id, 'classification')
    return {
        'Private company': '10',
        'Stock-exchange listed company': '20',
        'Individual entrepreneur': '30',
        'Investment fund': '40',
        'Semi state-owned company': '50',
        'State-/government(owned)': '60',
        'State-/government(-owned)': '60',
        'Other (please specify in comment field)': '70'
    }.get(classification, None)


class MapStakeholderInvestor(MapModel):
    old_class = old_editor.models.Stakeholder
    new_class = landmatrix.models.Investor
    attributes = {
        'stakeholder_identifier': 'investor_identifier',
        'id': (
            'id',
            ('name', get_name_for_stakeholder),
            ('fk_country_id', get_country_id_for_stakeholder),
            ('classification', get_classification_for_stakeholder),
            ('timestamp', get_now)
        )
    }
    DEBUG = False
