from django.db.models import Max
from editor.models import PrimaryInvestor, Stakeholder, Involvement, A_Key_Value_Lookup, Country, SH_Tag, SH_Tag_Group
import io

def get_country_for_primary_investor(pi_id):
    inv = Involvement.objects.filter(fk_primary_investor_id=pi_id)
    if inv.count() > 0:
        activity = inv[0].fk_activity
        if activity:
            target_country = A_Key_Value_Lookup.objects.filter(activity_identifier=activity.activity_identifier, key="target_country")
            if target_country:
                return Country.objects.get(id=target_country[0].value).name
    return None

def get_deals_for_pi(pi_id):
    qs = Involvement.objects.filter(fk_primary_investor__primary_investor_identifier=pi_id)
    return list(qs.values_list('fk_activity_id__activity_identifier', flat=True).distinct())


pduplicate_keys = []
pinvestors = {}
current_ids = PrimaryInvestor.objects.filter(fk_status_id__in=(2,3), involvement__isnull=False).\
    values('primary_investor_identifier').annotate(Max('id')).values_list('id__max', flat=True)
for pi in PrimaryInvestor.objects.filter(id__in=current_ids):
    country = get_country_for_primary_investor(pi.id)
    key = '%s (%s)' % (pi.name, country)
    if pi.name in ('', 'Unknown', 'Unknown ()'):
        continue
    if key in pinvestors and pi.primary_investor_identifier not in pinvestors[key]['ids']:
        pinvestors[key]['ids'].append(pi.primary_investor_identifier)
        pinvestors[key]['deals'].extend(get_deals_for_pi(pi.primary_investor_identifier))
        if not key in pduplicate_keys:
            pduplicate_keys.append(key)
    else:
        pinvestors[key] = {
            'name': pi.name,
            'country': country,
            'ids' : [pi.primary_investor_identifier,],
            'deals': get_deals_for_pi(pi.primary_investor_identifier),
        }

print("%i primary investors with same name/target country" % len(pduplicate_keys))
with io.open('duplicates-pi.csv', 'w', encoding='utf8') as file:
    file.write(u'Name;Investors;Deals\n')
    for key in pduplicate_keys:
        file.write('%s;%s;%s\n' % (
            key,
            u','.join([unicode(id) for id in pinvestors[key]['ids']]),
            u','.join([unicode(id) for id in pinvestors[key]['deals']]),
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

def get_deals_for_si(si_id):
    qs = Involvement.objects.filter(fk_stakeholder__stakeholder_identifier=si_id)
    return list(qs.values_list('fk_activity_id__activity_identifier', flat=True).distinct())


sduplicate_keys = []
sinvestors = {}
current_ids = Stakeholder.objects.filter(fk_status_id__in=(2,3), involvement__isnull=False).\
    values('stakeholder_identifier').annotate(Max('id')).values_list('id__max', flat=True)
for s in Stakeholder.objects.filter(id__in=current_ids):
    name = get_name_for_stakeholder(s.id)
    country = _get_country_for_stakeholder(s.id)
    key = '%s (%s)' % (name, country)
    if name in ('', 'Unknown', 'Unknown ()'):
        continue
    if key in sinvestors and s.stakeholder_identifier not in sinvestors[key]['ids']:
        sinvestors[key]['ids'].append(s.stakeholder_identifier)
        sinvestors[key]['deals'].extend(get_deals_for_si(s.stakeholder_identifier))
        if not key in sduplicate_keys:
            sduplicate_keys.append(key)
    else:
        sinvestors[key] = {
            'name': name,
            'country': country,
            'ids': [s.stakeholder_identifier,],
            'deals': get_deals_for_si(s.stakeholder_identifier),
        }

print("%i secondary investors with same name/target country" % len(sduplicate_keys))
with io.open('duplicates-si.csv', 'w', encoding='utf8') as file:
    file.write(u'Name;Investors;Deals\n')
    for key in sduplicate_keys:
        file.write(u'%s;%s;%s\n' % (
            key,
            u', '.join([unicode(id) for id in sinvestors[key]['ids']]),
            u', '.join([unicode(id) for id in sinvestors[key]['deals']]),
        ))

pinvestors_keys = set(pinvestors.keys())
sinvestors_keys = set(sinvestors.keys())
psduplicates_tmp = pinvestors_keys & sinvestors_keys
psduplicates = []
for key in psduplicates_tmp:
    name = pinvestors[key]['name']
    if name in ('', 'Unknown', 'Unknown ()'):
        continue
    psduplicates.append(key)

print("%i duplicates within primary and secondary investors" % len(psduplicates))
with io.open('duplicates-pi-si.csv', 'w', encoding='utf8') as file:
    file.write(u'Name;Primary Investors;Deals (PI);Secondary Investors;Deals (SI)\n')
    for key in psduplicates:
        file.write(u'%s;%s;%s;%s;%s\n' % (
            key,
            u', '.join([unicode(id) for id in pinvestors[key]['ids']]),
            u', '.join([unicode(id) for id in pinvestors[key]['deals']]),
            u', '.join([unicode(id) for id in sinvestors[key]['ids']]),
            u', '.join([unicode(id) for id in sinvestors[key]['deals']]),
        ))