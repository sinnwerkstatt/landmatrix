import re

from from_v1.mapping.map_model import MapModel
import landmatrix.models
import editor.models
from from_v1.migrate import V1

from from_v1.mapping.map_activity_tag_group import MapActivityTagGroup

from from_v1.mapping.map_activity import MapActivity
from from_v1.mapping.map_language import MapLanguage

from from_v1.mapping.aux_functions import year_to_date, replace_model_name_with_id, \
    replace_country_name_with_id, extract_value, is_number


def clean_coordinates(key, value):
    return key, value
#    if isinstance(value, str):
#        parts = attributes.split(', ')
#    else:
#        parts = attributes
#
#    changed = False
#    for index, part in enumerate(parts):
#        if part.startswith('"' + 'point_lon' + '"') or part.startswith('"' + 'point_lat' + '"'):
#            coordinate = extract_value(part)
#            if not is_number(coordinate):
#                changed = True
#                parts[index] = ''
#    if changed:
#        parts = [ part for part in parts if part ]
#        print(parts)
#
#    if isinstance(attributes, str):
#        return ', '.join(parts)
#    else:
#        return parts


def clean_level_of_accuracy(key, value):
    if value == 'Approximate level':
        value = 'Administrative region'
    elif value == 'Exact coordinates':
        value = 'Coordinates'
    return key, value


def clean_target_country(key, value):
    value = replace_country_name_with_id(value)
    return key, value


def clean_nature(key, value, old_values={}):
    if value == 'Lease / Concession':
        value = 'Lease'
    elif value == 'Exploitation license':
        if 'For wood and fibre' in old_values.get('intention', []):
            value = 'Concession'
        else:
            value = 'Exploitation permit / license / concession'
    return key, value


def clean_crops(key, value):
    from old_editor.models import Crop
    value = replace_model_name_with_id(Crop, value)
    key, value = replace_obsolete_crops(key, value)
    return key, value

def clean_animals(key, value):
    from old_editor.models import Animal
    #if value == ' Tilapia Fish':
    #    value = 'Fish'
    #elif value == 'Aquaculture':
    #    value = 'Aquaculture (animals)'
    value = replace_model_name_with_id(Animal, value)
    return key, value


def clean_minerals(key, value):
    from old_editor.models import Mineral
    # Diamond mining
    # Iron
    # Pyrolisis Plant
    # Petroleum
    value = replace_model_name_with_id(Mineral, value)
    return key, value


def replace_obsolete_crops(key, value):
    if value == 42:
        value = 7
    return key, value


def replace_obsolete_animals(key, value):
    ANIMALS_TO_REPLACE = {
        'Chicken': 'Poultry',
        'Cows': 'Dairy Cattle',
        'Mariculture': 'Aquaculture (animals)'
    }
    value = ANIMALS_TO_REPLACE.get(value, value)
    return key, value


def clean_land_use(key, value):
    LAND_USE_MAP = {
        'Pastoralists': 'Pastoralism',
    }
    value = LAND_USE_MAP.get(value, value)
    return key, value


def clean_promised_benefits(key, value):
    BENEFITS_MAP = {
        'Productive infrastructure (e.g. irrigation, tractors, machinery...)': 'Productive infrastructure',
    }
    value = BENEFITS_MAP.get(value, value)
    return key, value


def clean_intended_size(key, value):
    if ',' in value:
        return key, value.replace(',', '.')
    else:
        return key, value


def rename_changed_keys(key, value):
    RENAMED_KEYS = {
        'community_compensation': 'promised_compensation',
        'community_benefits': 'promised_benefits',
        'community_benefits_comment': 'promised_benefits_comment'
    }
    key = RENAMED_KEYS.get(key, key)
    return key, value


def rename_negotiation_status(key, value):
    RENAMED_STATUS = {
        'Intended (Expression of interest)': 'Expression of interest',
        'Intended (Under negotiation)': 'Under negotiation',
        'Concluded (Oral Agreement)': 'Oral agreement',
        'Concluded (Contract signed)': 'Contract signed',
        'Failed (Contract canceled)': 'Contract canceled',
        'Failed (Negotiations failed)': 'Negotiations failed',
    }
    value = RENAMED_STATUS.get(value, value)
    return key, value


def clean_intention(key, value, old_values={}):
    if value == 'Agriunspecified':
        value = 'Agriculture unspecified'
    elif value == 'Forestunspecified':
        value = 'Forestry unspecified'
    elif value == 'Other (please specify)':
        value = 'Other'
    elif value == 'For wood and fibre':
        if 'True' in old_values.get('not_public', []):
            value = 'Forest logging / management'
        elif len(old_values.get('nature', [])) == 0:
            value = 'Forestry unspecified'
        elif 'Outright Purchase' in old_values.get('nature', []):
            value = 'Timber plantation'
        elif 'Lease / Concession' in old_values.get('nature', []):
            value = 'Timber plantation'
        elif 'Exploitation license' in old_values.get('nature', []):
            value = 'Forest logging / management'
        else:
            value = None
    return key, value


def clean_attribute(key, value, old_values={}):
    key, value = rename_changed_keys(key, value)
    if value == '---------':
        value = None
    if key == 'crops':
        return clean_crops(key, value)
    elif key == 'animals':
        return clean_animals(key, value)
    elif key == 'minerals':
        return clean_minerals(key, value)
    elif key in ('point_lat', 'point_lon'):
        return clean_coordinates(key, value)
    elif key == 'target_country':
        return clean_target_country(key, value)
    elif key == 'animals':
        return replace_obsolete_animals(key, value)
    elif key == 'negotiation_status':
        return rename_negotiation_status(key, value)
    elif key == 'level_of_accuracy':
        return clean_level_of_accuracy(key, value)
    elif key == 'nature':
        return clean_nature(key, value, old_values=old_values)
    elif key == 'intention':
        return clean_intention(key, value, old_values=old_values)
    elif key == 'land_use':
        return clean_land_use(key, value)
    elif key == 'tg_negotiation_status_comment':
        return 'tg_contract_comment', value
    elif key == 'tg_primary_investor_comment':
        return 'tg_operational_stakeholder_comment', value
    elif key == 'tg_community_benefits_comment':
        return 'tg_promised_benefits_comment', value
    elif key == 'promised_benefits':
        return clean_promised_benefits(key, value)
    elif key == 'intended_size':
        return clean_intended_size(key, value)
    return key, value


def clean_group(group_name, key, value):
    if group_name == 'agreement_duration':
        return 'contract_01'
    if group_name == 'negotiation_status' and key != 'negotiation_status':
        return 'contract_01'
    match = re.match('(.*?)_(\d)', group_name)
    if match:
        return '%s_%02i' % (
            match.groups()[0],
            int(match.groups()[1]),
        )
    return group_name


if V1 == 'v1_pg':
    class MapActivityAttributeGroup(MapModel):
        old_class = editor.models.ActivityAttributeGroup
        new_class = landmatrix.models.ActivityAttributeGroup
#        attributes = {
#            'activity': 'fk_activity',
#            'language': 'fk_language',
#            'year': ('date', year_to_date),
#            'attributes': ('attributes', clean_crops_and_target_country)
#        }
        depends = [MapActivity, MapLanguage]
else:
    MapActivityAttributeGroup = MapActivityTagGroup