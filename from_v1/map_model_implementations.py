import datetime

from django.db import connections

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from map_model import MapModel
import landmatrix.models
import editor.models


def year_to_date(year):
    if not year: return None
    return ('0000'+str(year)+'-01-07')[-10:]


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

    @classmethod
    def all_records(cls):
        ids = cls.all_ids()
        cls._count = len(ids)
        return cls.old_class.objects.using(V1).filter(pk__in=ids).values()

    @classmethod
    def all_ids(cls):
        cursor = connections[V1].cursor()
        cursor.execute("""
SELECT id
FROM activities AS a
WHERE version = (SELECT MAX(version) FROM activities WHERE activity_identifier = a.activity_identifier)
ORDER BY activity_identifier
        """)
        return [id[0] for id in cursor.fetchall()]

def extract_value(part):
    values = part.split('=>')
    return values[1].strip('"')


def replace_model_name_with_id(model, attributes, attribute):

    if attribute not in attributes: return attributes

    if isinstance(attributes, str):
        return replace_model_name_with_id_str(model, attributes, attribute)
    else:
        return replace_model_name_with_id_dict(model, attributes, attribute)


def replace_model_name_with_id_str(model, attributes, attribute):

    def extract_target_country(part):
        return extract_value(part)

    def replace_name_with_id(name):
        from migrate import V1
        id = model.objects.using(V1).filter(name=name).values('id')[0]['id']
        if False: print(name, id)
        return '"' + attribute +'"=>"' + str(id) + '"'

    parts = attributes.split(', ')

    for index, part in enumerate(parts):
        if part.startswith('"' + attribute + '"'):
            target_country = extract_target_country(part)
            if target_country.isdigit():
                return attributes

            parts[index] = replace_name_with_id(target_country)
            break

    return ', '.join(parts)


def replace_model_name_with_id_dict(model, attributes, attribute):

    def replace_name_with_id(name):
        from migrate import V1
        return model.objects.using(V1).filter(name=name).values('id')[0]['id']

    value = attributes[attribute]
    if value.isdigit():
        return attributes

    attributes[attribute] = replace_name_with_id(value)

    return attributes


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

    if isinstance(attributes, str):
        parts = attributes.split(', ')
    else:
        parts = attributes

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

    if isinstance(attributes, str):
        return ', '.join(parts)
    else:
        return parts


from migrate import V1
from map_tag_groups import MapActivityTagGroup, MapStakeholderTagGroup



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
        depends = [ MapActivity, MapLanguage ]
else:
    MapActivityAttributeGroup = MapActivityTagGroup


class MapStakeholder(MapModel):
    old_class = editor.models.Stakeholder
    new_class = landmatrix.models.Stakeholder
    depends = [ MapStatus ]

    @classmethod
    def all_records(cls):
        ids = cls.all_ids()
        cls._count = len(ids)
        return cls.old_class.objects.using(V1).filter(pk__in=ids).values()

    @classmethod
    def all_ids(cls):
        cursor = connections[V1].cursor()
        cursor.execute("""
SELECT id
FROM stakeholders AS s
WHERE version = (SELECT MAX(version) FROM stakeholders WHERE stakeholder_identifier = s.stakeholder_identifier)
ORDER BY stakeholder_identifier
        """)
        return [id[0] for id in cursor.fetchall()]


def clean_country(attributes):
    return replace_country_name_with_id(attributes, 'country')

if V1 == 'v1_pg':
    class MapStakeholderAttributeGroup(MapModel):
        old_class = editor.models.StakeholderAttributeGroup
        new_class = landmatrix.models.StakeholderAttributeGroup
        attributes = {
            'stakeholder': 'fk_stakeholder',
            'language': 'fk_language',
            'attributes': ('attributes', clean_country)
        }
        depends = [ MapStakeholder, MapLanguage ]
else:
    MapStakeholderAttributeGroup = MapStakeholderTagGroup


class MapPrimaryInvestor(MapModel):
    old_class = editor.models.PrimaryInvestor
    new_class = landmatrix.models.PrimaryInvestor
    depends = [ MapStatus ]

    @classmethod
    def all_records(cls):
        ids = cls.all_ids()
        cls._count = len(ids)
        return cls.old_class.objects.using(V1).filter(pk__in=ids).values()

    @classmethod
    def all_ids(cls):
        cursor = connections[V1].cursor()
        cursor.execute("""
SELECT id
FROM primary_investors AS pi
WHERE version = (SELECT MAX(version) FROM primary_investors WHERE primary_investor_identifier = pi.primary_investor_identifier)
ORDER BY primary_investor_identifier
        """)
        return [id[0] for id in cursor.fetchall()]

class MapInvolvement(MapModel):
    old_class = editor.models.Involvement
    new_class = landmatrix.models.Involvement
    depends = [ MapActivity, MapStakeholder, MapPrimaryInvestor ]

    @classmethod
    def all_records(cls):
        activity_ids = MapActivity.all_ids()
        primary_investor_ids = MapPrimaryInvestor.all_ids()
        records = cls.old_class.objects.using(V1).\
            filter(fk_activity__in=activity_ids).\
            filter(fk_primary_investor__in=primary_investor_ids).values()
        cls._count = len(records)
        return records


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


class MapComment(MapModel):
    old_class = editor.models.Comment
    new_class = landmatrix.models.Comment
    attributes = {
        'activity_attribute_group': 'fk_activity_attribute_group',
        'stakeholder_attribute_group': 'fk_stakeholder_attribute_group'
    }


def get_country_for_primary_investor(pi_id):

    activity_ids = editor.models.Involvement.objects.using(V1).filter(fk_primary_investor=pi_id).values_list('fk_activity', flat=True)
    if not activity_ids or None in activity_ids:
        return None

    max_activity = max(activity_ids)
    stakeholder_ids = list(editor.models.Involvement.objects.using(V1).filter(fk_activity=max_activity).order_by('-investment_ratio').values_list('fk_stakeholder', flat=True))
    while stakeholder_ids:
        stakeholder_with_greatest_investment_ratio = stakeholder_ids.pop(0)

        country = get_country_id_for_stakeholder(stakeholder_with_greatest_investment_ratio)

        if country:
            return landmatrix.models.Country(country)

    return None


class MapInvestor(MapPrimaryInvestor):
    # old_class = editor.models.PrimaryInvestor
    new_class = landmatrix.models.Investor
    attributes = {
        'primary_investor_identifier': 'investor_identifier',
        'id': ('id', ('fk_country', get_country_for_primary_investor))
    }


def get_name_for_stakeholder(stakeholder_id):
    investor_name = get_first_stakeholder_tag_value(stakeholder_id, 'investor_name')
    return '' if investor_name is None else investor_name


def get_stakeholder_tag_groups(stakeholder_id):
    return editor.models.SH_Tag_Group.objects.using(V1).filter(fk_stakeholder=stakeholder_id)


def get_first_stakeholder_tag_value(stakeholder_id, tag_key):
    attribute_groups = get_stakeholder_tag_groups(stakeholder_id)
    for group in attribute_groups:
        tags = editor.models.SH_Tag.objects.using(V1).filter(fk_sh_tag_group=group.id)
        for tag in tags:
            if tag.fk_sh_key.key == tag_key:
                return tag.fk_sh_value.value
    return None


def get_country_for_stakeholder(stakeholder_id):
    country_name = get_first_stakeholder_tag_value(stakeholder_id, 'country')
    if country_name:
        return editor.models.Country.objects.using(V1).get(name=country_name)
    return None


def get_country_id_for_stakeholder(stakeholder_id):
    country = get_country_for_stakeholder(stakeholder_id)
    if country:
        return country.pk
    return None


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
    old_class = editor.models.Stakeholder
    new_class = landmatrix.models.Investor
    attributes = {
        'stakeholder_identifier': 'investor_identifier',
        'id': (
            'id',
            ('name', get_name_for_stakeholder),
            ('country', get_country_id_for_stakeholder),
            ('classification', get_classification_for_stakeholder)
        )
    }
    DEBUG = False


def get_status_for_investor(primary_investor_id):
    investor = editor.models.PrimaryInvestor.objects.using(V1).get(pk=primary_investor_id)
    return investor.fk_status.pk


class MapInvestorActivityInvolvement(MapModel):
    old_class = editor.models.Involvement
    new_class = landmatrix.models.InvestorActivityInvolvement
    attributes = {
        'investment_ratio': 'percentage',
        'fk_primary_investor_id': ('fk_investor_id', ('fk_status_id', get_status_for_investor))
    }
    depends = [ MapActivity, MapStakeholder, MapPrimaryInvestor ]

    @classmethod
    def all_records(cls):
        activity_ids = MapActivity.all_ids()
        primary_investor_ids = MapPrimaryInvestor.all_ids()
        records = cls.old_class.objects.using(V1).\
            filter(fk_activity__in=activity_ids).\
            filter(fk_primary_investor__in=primary_investor_ids).values()
        cls._count = len(records)
        return records
