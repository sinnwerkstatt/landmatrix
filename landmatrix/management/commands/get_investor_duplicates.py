"""
from editor.models import PrimaryInvestor, Stakeholder, Involvement, A_Key_Value_Lookup, Country, SH_Tag, SH_Tag_Group

def get_country_for_primary_investor(pi_id):
    inv = Involvement.objects.filter(fk_primary_investor_id=pi_id)
    if inv.count() > 0:
        activity = inv[0].fk_activity
        if activity:
            target_country = A_Key_Value_Lookup.objects.filter(activity_identifier=activity.activity_identifier, key="target_country")
            if target_country:
                return Country.objects.get(id=target_country[0].value).name
    return None

pduplicate_keys = []
pinvestors = {}
for pi in PrimaryInvestor.objects.all():
    key = '%s (%s)' % (pi.name, get_country_for_primary_investor(pi.id))
    if key == 'Unknown () (None)':
        continue
    if key in pinvestors and pi.primary_investor_identifier not in pinvestors[key]:
        pinvestors[key].append(pi.primary_investor_identifier)
        if not key in pduplicate_keys:
            pduplicate_keys.append(key)
    else:
        pinvestors[key] = [pi.primary_investor_identifier,]

print("%i primary investors with same name/target country" % len(pduplicate_keys))
for key in pduplicate_keys:
    print('%s: %s' % (
        key,
        ', '.join([str(id) for id in pinvestors[key]]),
    ))


def _get_stakeholder_tag_groups(stakeholder_id):
    return SH_Tag_Group.objects.filter(fk_stakeholder=stakeholder_id)

def get_first_stakeholder_tag_value(stakeholder_id, tag_key):
    attribute_groups = _get_stakeholder_tag_groups(stakeholder_id)
    for group in attribute_groups:
        tags = SH_Tag.objects.filter(fk_sh_tag_group=group.id)
        for tag in tags:
            if tag.fk_sh_key.key == tag_key:
                return tag.fk_sh_value.value
    return None

def get_name_for_stakeholder(stakeholder_id):
    investor_name = get_first_stakeholder_tag_value(stakeholder_id, 'investor_name')
    return '' if investor_name is None else investor_name

def get_country_id_for_stakeholder(stakeholder_id):
    country = _get_country_for_stakeholder(stakeholder_id)
    return country.pk if country else None

def _get_country_for_stakeholder(stakeholder_id):
    country_name = get_first_stakeholder_tag_value(stakeholder_id, 'country')
    if country_name:
        return country_name#Country.objects.get(name=country_name)
    return None


sduplicate_keys = []
sinvestors = {}
for s in Stakeholder.objects.all():
    name = get_name_for_stakeholder(s.id)
    country = _get_country_for_stakeholder(s.id)
    key = '%s (%s)' % (name, country)
    if key in ('Unknown () (None)', ' (None)'):
        continue
    if key in sinvestors and s.stakeholder_identifier not in sinvestors[key]:
        sinvestors[key].append(s.stakeholder_identifier)
        if not key in sduplicate_keys:
            sduplicate_keys.append(key)
    else:
        sinvestors[key] = [s.stakeholder_identifier,]

print("%i secondary investors with same name/target country" % len(sduplicate_keys))
for key in sduplicate_keys:
    print('%s: %s' % (
        key,
        ', '.join([str(id) for id in sinvestors[key]]),
    ))

pinvestors_keys = set(pinvestors.keys())
sinvestors_keys = set(sinvestors.keys())
psduplicates = pinvestors_keys & sinvestors_keys
print("%i duplicates within primary and secondary investors" % len(psduplicates))
for key in psduplicates:
    print('%s: PI (%s), SI (%s)' % (
        key,
        ', '.join([str(id) for id in pinvestors[key]]),
        ', '.join([str(id) for id in sinvestors[key]]),
    ))
"""