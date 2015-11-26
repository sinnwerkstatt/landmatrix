
__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from mapping.map_model import MapModel
import landmatrix.models
import editor.models


def year_to_date(year):
    if not year: return None
    return ('0000'+str(year)+'-01-07')[-10:]


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




def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

from mapping.map_stakeholder import MapStakeholder
from mapping.map_activity import MapActivity
from mapping.map_primary_investor import MapPrimaryInvestor
from migrate import V1


class MapInvolvement(MapModel):
    old_class = editor.models.Involvement
    new_class = landmatrix.models.Involvement
    depends = [ MapActivity, MapStakeholder, MapPrimaryInvestor ]

    @classmethod
    def all_records(cls):
        activity_ids = MapActivity.all_ids()
        primary_investor_ids = MapPrimaryInvestor.all_ids()
        stakeholder_ids = MapStakeholder.all_ids()
        records = cls.old_class.objects.using(V1).\
            filter(fk_activity__in=activity_ids).\
            filter(fk_primary_investor__in=primary_investor_ids).\
            filter(fk_stakeholder__in=stakeholder_ids).values()
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
