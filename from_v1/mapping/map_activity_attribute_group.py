from mapping.map_model import MapModel
import landmatrix.models
import editor.models
from migrate import V1

from mapping.map_activity_tag_group import MapActivityTagGroup

from mapping.map_activity import MapActivity
from mapping.map_language import MapLanguage

from mapping.aux_functions import year_to_date, replace_model_name_with_id, replace_country_name_with_id, extract_value, is_number

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


def clean_coordinates(attributes):
    if not 'point_lon' in attributes or not 'point_lat' in attributes: return attributes

    if isinstance(attributes, str):
        parts = attributes.split(', ')
    else:
        parts = attributes

    changed = False
    for index, part in enumerate(parts):
        if part.startswith('"' + 'point_lon' + '"') or part.startswith('"' + 'point_lat' + '"'):
            coordinate = extract_value(part)
            if not is_number(coordinate):
                changed = True
                parts[index] = ''
    if changed:
        parts = [ part for part in parts if part ]
        print(parts)

    if isinstance(attributes, str):
        return ', '.join(parts)
    else:
        return parts


def clean_target_country(attributes):
    return replace_country_name_with_id(attributes, 'target_country')


def clean_crops(attributes):
    from old_editor.models import Crop
    attrs = replace_model_name_with_id(Crop, attributes, 'crops')
    attrs = replace_obsolete_crops(attrs)
    return attrs


def replace_obsolete_crops(attrs):
    if attrs.get('crops', 0) == 42:
        attrs['crops'] = 7
    return attrs


def clean_crops_and_target_country(attributes):
    return clean_coordinates(clean_crops(clean_target_country(attributes)))


def replace_obsolete_animals(attrs):
    ANIMALS_TO_REPLACE = {
        'Chicken': 'Poultry', 'Cows': 'Dairy Cattle', 'Mariculture': 'Aquaculture (animals)'
    }
    if attrs.get('animals', 0) in ANIMALS_TO_REPLACE.keys():
        attrs['animals'] = ANIMALS_TO_REPLACE[attrs['animals']]
    return attrs


def rename_changed_attributes(attrs):
    RENAMED_ATTRIBUTES = {
        'community_compensation': 'promised_compensation',
        'community_benefits': 'promised_benefits',
        'community_benefits_comment': 'promised_benefits_comment'
    }
    for attr in RENAMED_ATTRIBUTES.keys():
        if attr in attrs:
            attrs[RENAMED_ATTRIBUTES[attr]] = attrs[attr]
            del attrs[attr]
    return attrs


def rename_negotiation_status(attrs):
    RENAMED_STATUS= {
        'Intended (Expression of interest)': 'Expression of interest',
        'Intended (Under negotiation)': 'Under negotiation',
        'Concluded (Oral Agreement)': 'Oral agreement',
        'Concluded (Contract signed)': 'Contract signed',
        'Failed (Contract canceled)': 'Contract canceled',
        'Failed (Negotiations failed)': 'Negotiations failed',
    }
    if 'negotiation_status' in attrs:
        attrs['negotiation_status'] = RENAMED_STATUS.get(
            attrs['negotiation_status'], attrs['negotiation_status']
        )
    return attrs


def clean_attributes(attributes):
    attributes = clean_crops_and_target_country(attributes)
    attributes = replace_obsolete_animals(attributes)
    attributes = rename_changed_attributes(attributes)
    attributes = rename_negotiation_status(attributes)
    return attributes


if V1 == 'v1_pg':
    class MapActivityAttributeGroup(MapModel):
        old_class = editor.models.ActivityAttributeGroup
        new_class = landmatrix.models.ActivityAttributeGroup
        attributes = {
            'activity': 'fk_activity',
            'language': 'fk_language',
            'year': ('date', year_to_date),
            'attributes': ('attributes', clean_crops_and_target_country)
        }
        depends = [MapActivity, MapLanguage]
else:
    MapActivityAttributeGroup = MapActivityTagGroup
