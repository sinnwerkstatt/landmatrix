#!/usr/bin/env python
import os
import sys
import csv
from collections import OrderedDict
from django.core.management import BaseCommand
from django.db import connections
from api.views.list_views import ElasticSearchMixin

from landmatrix.models import Activity, ActivityAttribute


class Command(ElasticSearchMixin,
              BaseCommand):
    help = 'Compares the public deal lists of the old database with the new database.'

    #def add_arguments(self, parser):
    #    parser.add_argument('file', nargs='+', type=str)

    def handle(self, *args, **options):
        old = self.get_old_activities() or []
        new = self.get_new_activities() or []
        #with open(options['file'][0], 'r') as csvfile:
        #    reader = csv.reader(csvfile, delimiter=';')
        #    for i, row in enumerate(reader):
        #        if i == 0:
        #            continue
        #        old.append(row[0])
        #        new.append(row[2])
        missing = list(set(old) - set(new))
        missing.sort()
        additional = list(set(new) - set(old))
        additional.sort()
        missing_deals = OrderedDict()
        missing_deals['status'] = []
        missing_deals['deal_size'] = []
        missing_deals['init_date'] = []
        missing_deals['deal_scope'] = []
        missing_deals['unknown'] = []
        additional_deals = OrderedDict()
        additional_deals['no_inv'] = []
        additional_deals['oc_only'] = []
        additional_deals['deal_scope'] = []
        additional_deals['unknown'] = []

        for deal_id in missing:
            a = Activity.objects.get(activity_identifier=deal_id)
            inv = a.involvements.all()
            if a.fk_status_id not in (2,3):
                missing_deals['status'].append(a)
            elif a.init_date and a.init_date < "1999-12-31":
                missing_deals['deal_size'].append(a)
            elif a.deal_size < 200:
                missing_deals['deal_size'].append(a)
            elif a.deal_scope == 'domestic':
                missing_deals['deal_scope'].append(a)
            else:
                missing_deals['unknown'].append(a)

        for deal_id in additional:
            a = Activity.objects.get(activity_identifier=deal_id)
            inv = a.involvements.all()
            if inv.count() == 0:
                additional_deals['no_inv'].append(a)
            elif inv[0].fk_investor.venture_involvements.count() == 0:
                additional_deals['oc_only'].append(a)
            else:
                additional_deals['unknown'].append(a)

        for key, value in missing_deals.items():
            self.stdout.write('-- MISSING: %i %s deals:' % (len(value), key))
            for a in value:
                inv = a.involvements.all()
                if inv.count() > 0:
                    investor_name = inv[0].fk_investor.name
                else:
                    investor_name = ''
                self.stdout.write('%s (%s, %s, %s, %s, %s, %s, %s) --> %s' % (
                    a.activity_identifier,
                    a.is_public and 'public' or 'not public',
                    a.deal_size,
                    a.init_date,
                    a.deal_scope,
                    a.negotiation_status,
                    a.fk_status.name,
                    investor_name,
                    a.get_not_public_reason(),
                    )
                )

        for key, value in additional_deals.items():
            self.stdout.write('-- ADDITIONAL: %i %s deals:' % (len(value), key))
            for a in value:
                inv = a.involvements.all()
                if inv.count() > 0:
                    investor_name = inv[0].fk_investor.name
                else:
                    investor_name = ''
                self.stdout.write('%s (%s, %s, %s, %s, %s) --> %s' % (
                    a.activity_identifier,
                    a.is_public and 'public' or 'not public',
                    a.deal_scope,
                    a.negotiation_status,
                    a.fk_status.name,
                    investor_name,
                    a.get_not_public_reason(),
                )
                                  )

    def get_old_activities(self):
        sql = """
                    SELECT
                a.activity_identifier
             FROM
                activities a
             LEFT JOIN a_key_value_lookup size ON a.activity_identifier = size.activity_identifier AND size.key = 'pi_deal_size',
                (SELECT DISTINCT
                   a.id,
                   negotiation.value as negotiation_status,
                   negotiation.year as negotiation_status_year
                 FROM
                   activities a
        JOIN (
          status
        ) ON (status.id = a.fk_status)
        LEFT JOIN (
            involvements i,
            stakeholders s,
            primary_investors pi,
            status pi_st
        ) ON (i.fk_activity = a.id AND i.fk_stakeholder = s.id AND i.fk_primary_investor = pi.id AND pi.fk_status = pi_st.id)
        LEFT JOIN (
        sh_key_value_lookup skvf1,
          countries investor_country,
          regions investor_region
        ) ON (s.stakeholder_identifier = skvf1.stakeholder_identifier AND skvf1.key = 'country' AND skvf1.value = investor_country.id AND investor_country.fk_region = investor_region.id)
        LEFT JOIN (
            a_key_value_lookup intention
        ) ON (a.activity_identifier = intention.activity_identifier AND intention.key = 'intention')
        LEFT JOIN (
            a_key_value_lookup target_country,
             countries deal_country,
             regions deal_region
        ) ON (a.activity_identifier = target_country.activity_identifier AND target_country.key = 'target_country' AND target_country.value = deal_country.id AND deal_country.fk_region = deal_region.id)
        LEFT JOIN (
            a_key_value_lookup negotiation
        ) ON (a.activity_identifier = negotiation.activity_identifier AND negotiation.key = 'pi_negotiation_status')
        LEFT JOIN (
            a_key_value_lookup implementation
        ) ON (a.activity_identifier = implementation.activity_identifier AND implementation.key = 'pi_implementation_status')
        LEFT JOIN (
            a_key_value_lookup bf
        ) ON (a.activity_identifier = bf.activity_identifier AND bf.key = 'pi_deal')
        LEFT JOIN (
            a_key_value_lookup size
        ) ON (a.activity_identifier = size.activity_identifier AND size.key = 'pi_deal_size')
        LEFT JOIN (
            a_key_value_lookup deal_scope
        ) ON (a.activity_identifier = deal_scope.activity_identifier AND deal_scope.key = 'deal_scope')
    
                 WHERE
                   
        a.version = (SELECT max(version) FROM activities amax, status st WHERE amax.fk_status = st.id AND amax.activity_identifier = a.activity_identifier AND st.name IN ("active", "overwritten", "deleted"))
        AND status.name in ("active", "overwritten")
        AND bf.value = 'True'
        AND pi.version = (SELECT max(version) FROM primary_investors pimax, status st WHERE pimax.fk_status = st.id AND pimax.primary_investor_identifier = pi.primary_investor_identifier AND st.name IN ("active", "overwritten", "deleted"))
        AND pi_st.name IN ("active", "overwritten")
        AND lower(negotiation.value) in ('concluded (oral agreement)', 'concluded (contract signed)')  
        AND deal_scope.value = 'transnational' ) AS sub
             WHERE a.id = sub.id;
        """
        cursor = connections['v1_my'].cursor()
        cursor.execute(sql)
        results = [a[0] for a in cursor.fetchall()]
        self.stdout.write('-- Found %i old deals' % len(results))
        return results

    def get_new_activities(self):
        from django.test.client import RequestFactory
        from django.contrib.sessions.middleware import SessionMiddleware
        from django.contrib.auth.models import AnonymousUser
        rf = RequestFactory()
        request = rf.get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.user = AnonymousUser()

        self.request = request
        self.disable_filters()
        query = self.create_query_from_filters()
        query['bool']['filter'].append({
            'terms': {
                'current_negotiation_status': ['Oral agreement',
                                               'Contract signed']
            }
        })
        results = self.execute_elasticsearch_query(query, doc_type='deal', fallback=False)
        results = [r['_source']['activity_identifier'] for r in results]
        self.stdout.write('-- Found %i new deals' % len(results))
        return results
