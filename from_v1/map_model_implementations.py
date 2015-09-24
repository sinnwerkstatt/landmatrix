__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


from map_model import MapModel
import landmatrix.models
import editor.models

class MapLanguage(MapModel):
    old_class = editor.models.Language
    new_class = landmatrix.models.Language

class MapStatus(MapModel):
    old_class = editor.models.Status
    new_class = landmatrix.models.Status

class MapActivity(MapModel):
    old_class = editor.models.Activity
    new_class = landmatrix.models.Activity
    depends = [ MapStatus ]

def year_to_date(year):
    if not year: return None
    return ('0000'+str(year)+'-01-07')[-10:]

def extract_value(part):
    values = part.split('=>')
    return values[1].strip('"')

def replace_model_name_with_id(model, attributes, attribute):

    def extract_target_country(part):
        return extract_value(part)

    def replace_name_with_id(name):
        from migrate import V1
        id = model.objects.using(V1).filter(name=name).values('id')[0]['id']
        if False: print(name, id)
        return '"' + attribute +'"=>"' + str(id) + '"'

    if not attribute in attributes: return attributes

    parts = attributes.split(', ')
    for index, part in enumerate(parts):
        if part.startswith('"' + attribute + '"'):
            target_country = extract_target_country(part)
            if target_country.isdigit():
                return attributes

            parts[index] = replace_name_with_id(target_country)
            break

    return ', '.join(parts)

def replace_country_name_with_id(attributes, attribute):
    from editor.models import Country
    return replace_model_name_with_id(Country, attributes, attribute)

def clean_target_country(attributes):
    return replace_country_name_with_id(attributes, 'target_country')

def clean_crops(attributes):
    from editor.models import Crop
    return replace_model_name_with_id(Crop, attributes, 'crops')

def clean_crops_and_target_country(attributes):
    return clean_coordinates(clean_crops(clean_target_country(attributes)))

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def clean_coordinates(attributes):
    if not 'point_lon' in attributes or not 'point_lat' in attributes: return attributes
    parts = attributes.split(', ')
    changed = False
    for index, part in enumerate(parts):
        coordinate = None
        if part.startswith('"' + 'point_lon' + '"') or part.startswith('"' + 'point_lat' + '"'):
            coordinate = extract_value(part)
            if not is_number(coordinate):
                changed = True
                parts[index] = ''
    if changed:
        parts = [ part for part in parts if part ]
        print(parts)

    return ', '.join(parts)

class MapActivityAttributeGroup(MapModel):
    old_class = editor.models.ActivityAttributeGroup
    new_class = landmatrix.models.ActivityAttributeGroup
    attributes = {
        'activity': 'fk_activity',
        'language': 'fk_language',
        'year': ('date', year_to_date),
        'attributes': ('attributes', clean_crops_and_target_country)
    }
    depends = [ MapActivity, MapLanguage ]

class MapStakeholder(MapModel):
    old_class = editor.models.Stakeholder
    new_class = landmatrix.models.Stakeholder
    depends = [ MapStatus ]

def clean_country(attributes):
    return replace_country_name_with_id(attributes, 'country')

class MapStakeholderAttributeGroup(MapModel):
    old_class = editor.models.StakeholderAttributeGroup
    new_class = landmatrix.models.StakeholderAttributeGroup
    attributes = {
        'stakeholder': 'fk_stakeholder',
        'language': 'fk_language',
        'attributes': ('attributes', clean_country)
    }
    depends = [ MapStakeholder, MapLanguage ]

class MapPrimaryInvestor(MapModel):
    old_class = editor.models.PrimaryInvestor
    new_class = landmatrix.models.PrimaryInvestor
    depends = [ MapStatus ]

class MapInvolvement(MapModel):
    old_class = editor.models.Involvement
    new_class = landmatrix.models.Involvement
    depends = [ MapActivity, MapStakeholder, MapPrimaryInvestor ]

class MapRegion(MapModel):
    old_class = editor.models.Region
    new_class = landmatrix.models.Region

class MapCountry(MapModel):
    old_class = editor.models.Country
    new_class = landmatrix.models.Country
    attributes = {
        'region': 'fk_region',
    }
    depends = [ MapRegion ]

class MapBrowseRule(MapModel):
    old_class = editor.models.BrowseRule
    new_class = landmatrix.models.BrowseRule

class MapBrowseCondition(MapModel):
    old_class = editor.models.BrowseCondition
    new_class = landmatrix.models.BrowseCondition
    depends = [ MapBrowseRule ]


class MapAgriculturalProduce(MapModel):
    old_class = editor.models.AgriculturalProduce
    new_class = landmatrix.models.AgriculturalProduce

class MapCrop(MapModel):
    old_class = editor.models.Crop
    new_class = landmatrix.models.Crop
    attributes = {
        'agricultural_produce': 'fk_agricultural_produce',
    }
    depends = [ MapAgriculturalProduce ]
