from mapping.map_model import MapModel
import landmatrix.models
import editor.models
from migrate import V1

from mapping.map_activity_tag_group import MapActivityTagGroup

from mapping.map_activity import MapActivity
from mapping.map_language import MapLanguage

from mapping.aux_functions import year_to_date, replace_model_name_with_id, \
    replace_country_name_with_id, extract_value, is_number

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


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

def clean_nature(key, value):
    if value == 'Lease / Concession':
        value = 'Lease'
    elif value == 'Exploitation license':
        value = 'Resource exploitation license / concession'
    return key, value

def clean_crops(key, value):
    from old_editor.models import Crop
    value = replace_model_name_with_id(Crop, value)
    key, value = replace_obsolete_crops(key, value)
    return key, value

def clean_animals(key, value):
    from old_editor.models import Animal
    value = replace_model_name_with_id(Animal, value)
    return key, value

def clean_minerals(key, value):
    from old_editor.models import Mineral
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

def clean_intention(key, value):
    if value == 'Agriunspecified':
        value = 'Agriculture unspecified'
    elif value == 'Forestunspecified':
        value = 'Forestry unspecified'
    elif value == 'Mining':
        value = 'Resource extraction'
    elif value == 'Other (please specify)':
        value = 'Other'
    return key, value

def clean_attribute(key, value):
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
        return clean_nature(key, value)
    elif key == 'intention':
        return clean_intention(key, value)
    elif key == 'tg_negotiation_status_comment':
        return 'tg_contract_comment', value
    elif key == 'tg_primary_investor_comment':
        return 'tg_operational_stakeholder_comment', value
    return key, value

def clean_group(group_name, key, value):
    if group_name == 'agreement_duration':
        return 'contract_1'
    if group_name == 'negotiation_status' and key != 'negotiation_status':
        return 'contract_1'
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