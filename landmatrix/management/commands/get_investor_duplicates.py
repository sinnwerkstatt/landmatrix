import io
from django.db.models import Max
from editor.models import Activity, PrimaryInvestor, Stakeholder, Involvement, A_Key_Value_Lookup, Country, SH_Tag, SH_Tag_Group

class View:
    def get_country_for_primary_investor(self, pi_id):
        inv = Involvement.objects.filter(fk_primary_investor_id=pi_id)
        if inv.count() > 0:
            activity = inv[0].fk_activity
            if activity:
                target_country = A_Key_Value_Lookup.objects.filter(activity_identifier=activity.activity_identifier, key="target_country")
                if target_country:
                    return Country.objects.get(id=target_country[0].value).name
        return None

    def get_deals_for_pi(self, pi_id):
        qs = Involvement.objects.filter(fk_primary_investor__primary_investor_identifier=pi_id)
        return list(qs.values_list('fk_activity_id__activity_identifier', flat=True).distinct())

    def get_pi_duplicates(self, response):
        writer = csv.writer(response)
        pduplicate_keys = []
        pinvestors = {}
        act_ids = Activity.objects.values('activity_identifier').annotate(Max('id')).values_list('id__max', flat=True)
        for inv in Involvement.objects.filter(fk_activity__in=act_ids):
            pi = inv.fk_primary_investor
            country = self.get_country_for_primary_investor(pi.id)
            key = '%s (%s)' % (pi.name, country)
            if pi.name in ('', 'Unknown', 'Unknown ()'):
                continue
            if key in pinvestors and pi.primary_investor_identifier not in pinvestors[key]['ids']:
                pinvestors[key]['ids'].append(pi.primary_investor_identifier)
                if not inv.fk_activity.activity_identifier in pinvestors[key]['deals']:
                    pinvestors[key]['deals'].append(inv.fk_activity.activity_identifier)
                if not key in pduplicate_keys:
                    pduplicate_keys.append(key)
            else:
                pinvestors[key] = {
                    'name': pi.name,
                    'country': country,
                    'ids' : [pi.primary_investor_identifier,],
                    'deals': [inv.fk_activity.activity_identifier,],
                }
        writer.writerow([u'Name', u'Investors', u'Deals'])
        for key in pduplicate_keys:
            writer.writerow((
                key,
                u','.join([unicode(id) for id in pinvestors[key]['ids']]),
                u','.join([unicode(id) for id in pinvestors[key]['deals']]),
            ))
        return pinvestors, pduplicate_keys


    def _get_stakeholder_tag_groups(self, stakeholder_id):
        return SH_Tag_Group.objects.filter(fk_stakeholder=stakeholder_id)

    def get_first_stakeholder_tag_value(self, stakeholder_id, tag_key):
        attribute_groups = self._get_stakeholder_tag_groups(stakeholder_id)
        for group in attribute_groups:
            tags = SH_Tag.objects.filter(fk_sh_tag_group=group.id)
            for tag in tags:
                if tag.fk_sh_key.key == tag_key:
                    return tag.fk_sh_value.value
        return None

    def get_name_for_stakeholder(self, stakeholder_id):
        investor_name = self.get_first_stakeholder_tag_value(stakeholder_id, 'investor_name')
        return '' if investor_name is None else investor_name

    def get_country_id_for_stakeholder(self, stakeholder_id):
        country = self._get_country_for_stakeholder(stakeholder_id)
        return country.pk if country else None

    def _get_country_for_stakeholder(self, stakeholder_id):
        country_name = self.get_first_stakeholder_tag_value(stakeholder_id, 'country')
        if country_name:
            return country_name#Country.objects.get(name=country_name)
        return None

    def get_deals_for_si(self, si_id):
        qs = Involvement.objects.filter(fk_stakeholder__stakeholder_identifier=si_id)
        return list(qs.values_list('fk_activity_id__activity_identifier', flat=True).distinct())

    def get_si_duplicates(self, response):
        writer = csv.writer(response)
        sduplicate_keys = []
        sinvestors = {}
        act_ids = Activity.objects.values('activity_identifier').annotate(Max('id')).values_list('id__max', flat=True)
        for inv in Involvement.objects.filter(fk_activity__in=act_ids):
            s = inv.fk_stakeholder
            name = self.get_name_for_stakeholder(s.id)
            country = self._get_country_for_stakeholder(s.id)
            key = '%s (%s)' % (name, country)
            if name in ('', 'Unknown', 'Unknown ()'):
                continue
            if key in sinvestors and s.stakeholder_identifier not in sinvestors[key]['ids']:
                sinvestors[key]['ids'].append(s.stakeholder_identifier)
                if not inv.fk_activity.activity_identifier in sinvestors[key]['deals']:
                    sinvestors[key]['deals'].append(inv.fk_activity.activity_identifier)
                if not key in sduplicate_keys:
                    sduplicate_keys.append(key)
            else:
                sinvestors[key] = {
                    'name': name,
                    'country': country,
                    'ids': [s.stakeholder_identifier,],
                    'deals': [inv.fk_activity.activity_identifier,],
                }

        writer.writerow([u'Name', u'Investors', u'Deals'])
        for key in sduplicate_keys:
            writer.writerow((
                key,
                u', '.join([unicode(id) for id in sinvestors[key]['ids']]),
                u', '.join([unicode(id) for id in sinvestors[key]['deals']]),
            ))
        return sinvestors, sduplicate_keys

    def get_pi_si_duplicates(self, response):
        writer = csv.writer(response)
        r = HttpResponse(content_type='text/csv')
        pinvestors, pduplicates = self.get_pi_duplicates(r)
        pinvestors_keys = set(pinvestors.keys())
        sinvestors, sduplicates = self.get_si_duplicates(r)
        sinvestors_keys = set(sinvestors.keys())
        psduplicates_tmp = pinvestors_keys & sinvestors_keys
        psduplicates = []
        for key in psduplicates_tmp:
            name = pinvestors[key]['name']
            if name in ('', 'Unknown', 'Unknown ()'):
                continue
            psduplicates.append(key)

        writer.writerow([u'Name', u'Primary Investors', u'Deals (PI)', u'Secondary Investors', u'Deals (SI)'])
        for key in psduplicates:
            writer.writerow((
                key,
                u', '.join([unicode(id) for id in pinvestors[key]['ids']]),
                u', '.join([unicode(id) for id in pinvestors[key]['deals']]),
                u', '.join([unicode(id) for id in sinvestors[key]['ids']]),
                u', '.join([unicode(id) for id in sinvestors[key]['deals']]),
            ))
        return psduplicates

    def get_si_name_diff_country_classification(self, response):
        writer = csv.writer(response, delimiter=';')
        return None

    def get_pi_name_diff_target_country(self, response):
        writer = csv.writer(response, delimiter=';')
        return None
