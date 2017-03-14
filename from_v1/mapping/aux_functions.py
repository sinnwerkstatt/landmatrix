import old_editor.models
from from_v1.migrate import V1
from django.utils import timezone
from django.db import connections



def stakeholder_ids():
    cursor = connections[V1].cursor()
    cursor.execute("""
SELECT id
FROM stakeholders AS s
WHERE version = (SELECT MAX(version) FROM stakeholders WHERE stakeholder_identifier = s.stakeholder_identifier)
ORDER BY stakeholder_identifier
            """)
    return [id[0] for id in cursor.fetchall()]


def get_now(_):
    return timezone.now()


def year_to_date(year):
    if not year: return None
    return ('0000'+str(year)+'-01-07')[-10:]


def extract_value(part):
    values = part.split('=>')
    return values[1].strip('"')


def replace_model_name_with_id(model, value):
    if is_number(value):
        return value
    value = model.objects.using(V1).filter(name=value).values('id')[0]['id']
    return value


def replace_country_name_with_id(value):
    return replace_model_name_with_id(old_editor.models.Country, value)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def get_first_stakeholder_tag_value(stakeholder_id, tag_key):
    attribute_groups = _get_stakeholder_tag_groups(stakeholder_id)
    for group in attribute_groups:
        tags = old_editor.models.SH_Tag.objects.using(V1).filter(fk_sh_tag_group=group.id)
        for tag in tags:
            if tag.fk_sh_key.key == tag_key:
                return tag.fk_sh_value.value
    return None


def get_country_id_for_stakeholder(stakeholder_id):
    country = _get_country_for_stakeholder(stakeholder_id)
    return country.pk if country else None


#def _replace_model_name_with_id_str(model, attributes, attribute):
#
#    def replace_name_with_id(name):
#        id = model.objects.using(V1).filter(name=name).values('id')[0]['id']
#        if False: print(name, id)
#        return '"' + attribute +'"=>"' + str(id) + '"'
#
#    parts = attributes.split(', ')
#
#    for index, part in enumerate(parts):
#        if part.startswith('"' + attribute + '"'):
#            target_country = extract_value(part)
#            if target_country.isdigit():
#                return attributes
#
#            parts[index] = replace_name_with_id(target_country)
#            break
#
#    return ', '.join(parts)


def _get_stakeholder_tag_groups(stakeholder_id):
    return old_editor.models.SH_Tag_Group.objects.using(V1).filter(fk_stakeholder=stakeholder_id)


def _get_country_for_stakeholder(stakeholder_id):
    country_name = get_first_stakeholder_tag_value(stakeholder_id, 'country')
    if country_name:
        return old_editor.models.Country.objects.using(V1).get(name=country_name)
    return None


from from_v1.mapping.map_activity import MapActivity
def all_involvement_records(cls):
    activity_ids = MapActivity.all_ids()
    primary_investor_ids = MapPrimaryInvestor.all_ids()
    stakeholder_ids = stakeholder_ids()
    records = cls.old_class.objects.using(V1).\
        filter(fk_activity__in=activity_ids).\
        filter(fk_primary_investor__in=primary_investor_ids).\
        filter(fk_stakeholder__in=stakeholder_ids).values()
    cls._count = len(records)
    return records
