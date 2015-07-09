__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

import os
import pprint
from django.http import HttpRequest
import json

import os.path
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))


proj_path = os.path.join(os.path.dirname(__file__), "../..")
# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "landmatrix.settings")
sys.path.append(proj_path)

# This is so my local_settings.py gets loaded.
os.chdir(proj_path)

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from global_app.views import DummyActivityProtocol

from django.db import connection
from django.db.utils import ProgrammingError
import time

# first column is thrown away anyway
def _throwaway_column(expected, actual): return True
# data messed up, not all intended use got carried over in MySQL to PostgreSQL conversion
def _actual_intention_in_expected(expected, actual): return set(actual.split('##!##')) <= set(expected.split('##!##'))
def _floats_pretty_equal(expected, actual): return 0.99 <= expected/actual <= 1.01
# empty years are converted to zero by new SQL. who cares.
def _null_to_zero_conversion(expected, actual):
    return expected[:-1] == actual if isinstance(expected, str) and expected.endswith('#0') else expected == actual

class Compare:

    NUM_COMPARED_RECORDS = 20

    files_to_compare = [
        'by_crop',
        'by_data_source_type',
        'by_intention',
        'by_investor',
        'by_investor_country', 'by_investor_region', 'by_target_country', 'by_target_region', 'all_deals',
    ]
    warnings = {}
    errors = {}
    sql = {}

    _died = False
    _starttime = 0

    filename = ''
    def run(self):

        self._starttime = time.time()

        try:
            for self.filename in self.files_to_compare:
                self.compare_with_expected()

        except ProgrammingError as e:
            print(e)
            print(connection.queries[-1]['sql'])
            self._died = True

    def show(self, sql=False, warnings=True):
        if self._died: return
        if sql: self._print_messages(self.sql, 'SQL', '.')
        if warnings: self._print_messages(self.warnings, 'Warnings', '=')
        self._print_messages(self.errors, 'Errors', '*')


    def compare_with_expected(self):
        from collections import deque
        from operator import itemgetter

        postdata, records = self.read_data(self.filename+'.out')
        protocol = DummyActivityProtocol()
        request = HttpRequest()
        request.POST = {'data': postdata}
        res = protocol.dispatch(request, action="list_group").content
        self.sql[self.filename] = [connection.queries[-1]['sql']]
        query_result = json.loads(res.decode())['activities'][:self.NUM_COMPARED_RECORDS]

        if self.filename == 'by_intention':
            # postprocess because postgres ORDER BY sorts differently from MySQL :-/
            query_result = deque(query_result)
            query_result.rotate(1)
            query_result = list(query_result)
            query_result.pop(0)
            records.pop(0)
            query_result.sort(key=itemgetter(1))

        if len(query_result) != len(records):
            self.add_error('NUMBER OF RECORDS NOT EQUAL: expected %d, got %d' %(len(records), len(query_result)))
            self.add_error(records)
            self.add_error(query_result)
            return

        for id in range(0, len(records)):
            for j in range(0, len(records[id])):
                if not self.equal(j, records[id][j], query_result[id][j]):
                    func = self.add_warning if self.similar(j, records[id][j], query_result[id][j]) else self.add_error
                    func("%-20s field %2i: expected %-24s got %-24s" % (str(records[id][1]), j, str(records[id][j]), str(query_result[id][j])))

    def _print_messages(self, container, what, headerchar):
        if not container: return
        for file, messages in container.items():
            print(headerchar*80, what+': '+file, headerchar*80, sep='\n')
            print(*messages, sep="\n")
            print(headerchar*4, ' '*2, len(messages), what)
        print(headerchar*4, ' '*2, 'Total:', sum(len(messages) for messages in container.values()), what)
        print(headerchar*4, ' '*2, 'Elapsed:', time.time() - self._starttime)

    def read_data(self, filename):
        with open(os.path.dirname(os.path.realpath(__file__)) + '/' + filename, 'r') as f:
            lines = f.readlines()
        parameters = eval(lines[1])
        records = eval(lines[2])
        return (parameters['data'][0], records[:self.NUM_COMPARED_RECORDS])

    def _add_message(self, container, message):
        if not self.filename in container.keys():
            container[self.filename] = []
        container[self.filename].append(str(message))

    def add_error(self, error):
        self._add_message(self.errors, error)

    def add_warning(self, warning):
        self._add_message(self.warnings, warning)

    def equal(self, field, expected, actual):
        return expected == actual

    similar_table = {
        'all_deals': {
            6: _actual_intention_in_expected,
            7: _null_to_zero_conversion,
            8: _null_to_zero_conversion
        },
        'by_target_region': {
            0: _throwaway_column,
            2: _actual_intention_in_expected,
            4: _floats_pretty_equal
        },
        'by_target_country': {
            0: _throwaway_column,
            3: _actual_intention_in_expected,
        },
        'by_investor_region': {
            0: _throwaway_column,
            2: _actual_intention_in_expected,
            4: _floats_pretty_equal
        },
        'by_investor_country': {
            0: _throwaway_column,
            3: _actual_intention_in_expected,
            5: _floats_pretty_equal
        },
        'by_investor': {
            0: _throwaway_column,
            3: _actual_intention_in_expected,
            5: _floats_pretty_equal
        },
        'by_intention': {
            0: _throwaway_column,
        },
        'by_data_source_type': {
            0: _throwaway_column,
            2: _actual_intention_in_expected,
        },
        'by_crop': {
            0: _throwaway_column,
        }
    }
    def similar(self, field, expected, actual):
        if field in self.similar_table[self.filename]:
            return self.similar_table[self.filename][field](expected, actual)
        return False

    def original_sql_queries(self):
        return {
            'all_deals': """
        SELECT
            sub.name as name,
            sub.deal_id as 'deal_id', sub.target_country as 'target_country', sub.primary_investor as 'primary_investor', sub.investor_name as 'investor_name', sub.investor_country
 as 'investor_country', sub.intention as 'intention', sub.negotiation_status as 'negotiation_status', sub.implementation_status as 'implementation_status', GROUP_CONCAT(intended_size.value ORDER BY intended_size.year DESC) as 'intended_size', GROUP_CONCAT(contract_size.value ORDER BY contract_size.year DESC) as 'contract_size',
            'dummy' as dummy
          FROM
             activities a
          LEFT JOIN a_key_value_lookup size ON a.activity_identifier = size.activity_identifier AND size.key = 'pi_deal_size'
          LEFT JOIN a_key_value_lookup intended_size ON a.activity_identifier = intended_size.activity_identifier AND intended_size.key = 'intended_size'
          LEFT JOIN a_key_value_lookup contract_size ON a.activity_identifier = contract_size.activity_identifier AND contract_size.key = 'contract_size'
          LEFT JOIN a_key_value_lookup production_size ON a.activity_identifier = production_size.activity_identifier AND production_size.key = 'production_size'
          JOIN (SELECT DISTINCT
              a.id as id,
               'all deals'  as name,
              a.activity_identifier as deal_id, GROUP_CONCAT(DISTINCT deal_country.name SEPARATOR '##!##') as target_country, GROUP_CONCAT(DISTINCT p.name SEPARATOR '##!##') as primary_investor,GROUP_CONCAT(DISTINCT CONCAT(investor_name.value, '#!#', s.stakeholder_identifier) SEPARATOR '##!##')  as investor_name,GROUP_CONCAT(DISTINCT CONCAT(investor_country.name, '#!#', investor_country.code_alpha3) SEPARATOR '##!##') as investor_country,GROUP_CONCAT(DISTINCT intention.value ORDER BY intention.value SEPARATOR '##!##') AS intention,GROUP_CONCAT(DISTINCT CONCAT(negotiation_status.value, '#!#', IFNULL(negotiation_status.year, 0)) SEPARATOR '##!##') as negotiation_status,GROUP_CONCAT(DISTINCT CONCAT(implementation_status.value, '#!#', IFNULL(implementation_status.year, 0)) SEPARATOR '##!##') as implementation_status,
              'dummy' as dummy
          FROM
            activities a
          JOIN (status) ON (status.id = a.fk_status)
            LEFT JOIN (involvements i, primary_investors pi,
            status pi_st) ON (i.fk_activity = a.id AND i.fk_primary_investor = pi.id AND pi.fk_status = pi_st.id)
                          LEFT JOIN (stakeholders s) ON (i.fk_stakeholder = s.id)
            LEFT JOIN (a_key_value_lookup deal_id) ON (a.activity_identifier = deal_id.activity_identifier AND deal_id.key = 'deal_id') LEFT JOIN (a_key_value_lookup target_country) ON (a.activity_identifier = target_country.activity_identifier AND target_country.key = 'target_country')
                                   LEFT JOIN (countries deal_country) ON (target_country.value = deal_country.id)
                                   LEFT JOIN (regions deal_region) ON (deal_country.fk_region = deal_region.id)LEFT JOIN (primary_investors p) ON (i.fk_primary_investor = p.id) LEFT JOIN (sh_key_value_lookup investor_name) ON (s.stakeholder_identifier = investor_name.stakeholder_identifier AND investor_name.key = 'investor_name')
                        LEFT JOIN (sh_key_value_lookup skvl1) ON (s.stakeholder_identifier = skvl1.stakeholder_identifier AND skvl1.key = 'country')
                        LEFT JOIN (countries investor_country) ON (investor_country.id = skvl1.value)
                        LEFT JOIN (regions investor_region) ON (investor_region.id = investor_country.fk_region)LEFT JOIN (a_key_value_lookup intention) ON (a.activity_identifier = intention.activity_identifier AND intention.key = 'intention') LEFT JOIN (a_key_value_lookup negotiation_status) ON (a.activity_identifier = negotiation_status.activity_identifier AND negotiation_status.key = 'pi_negotiation_status') LEFT JOIN (a_key_value_lookup implementation_status) ON (a.activity_identifier = implementation_status.activity_identifier AND implementation_status.key = 'pi_implementation_status')
            LEFT JOIN (a_key_value_lookup pi_deal) ON (a.activity_identifier = pi_deal.activity_identifier AND pi_deal.key = 'pi_deal')
            LEFT JOIN (a_key_value_lookup deal_scope) ON (a.activity_identifier = deal_scope.activity_identifier AND deal_scope.key = 'deal_scope')
            LEFT JOIN (a_key_value_lookup akv0)
 ON (a.activity_identifier = akv0.activity_identifier AND akv0.key = 'pi_negotiation_status')

          WHERE
            a.version = (SELECT max(version) FROM activities amax, status st WHERE amax.fk_status = st.id AND amax.activity_identifier = a.activity_identifier AND st.name IN ("active", "overwritten", "deleted"))
            AND status.name in ("active", "overwritten")
            AND pi_deal.value = 'True'
            AND pi.version = (SELECT max(version) FROM primary_investors pimax, status st WHERE pimax.fk_status = st.id AND pimax.primary_investor_identifier = pi.primary_investor_identifier AND st.name IN ("active", "overwritten", "deleted"))
            AND pi_st.name IN ("active", "overwritten")

            AND (intention.value IS NULL OR intention.value != "Mining")


             AND deal_scope.value = 'transnational'  AND akv0.value IN ('Concluded (Oral Agreement)','Concluded (Contract signed)')
            GROUP BY a.id
            ) AS sub ON (sub.id = a.id)
          GROUP BY a.id
         ORDER BY `deal_id`  ASC
         ;
""",
            'by_target_region': """
        SELECT DISTINCT
              'target_region' as name,
               deal_region.name as target_region, GROUP_CONCAT(DISTINCT intention.value ORDER BY intention.value SEPARATOR '##!##') AS intention,COUNT(DISTINCT a.activity_identifier) as deal_count,SUM(a.availability) / COUNT(a.activity_identifier) as availability,
              'dummy' as dummy
          FROM
            activities a
          JOIN (status) ON (status.id = a.fk_status)
            LEFT JOIN (involvements i, primary_investors pi,
            status pi_st) ON (i.fk_activity = a.id AND i.fk_primary_investor = pi.id AND pi.fk_status = pi_st.id)
                          LEFT JOIN (stakeholders s) ON (i.fk_stakeholder = s.id)
            LEFT JOIN (a_key_value_lookup target_country) ON (a.activity_identifier = target_country.activity_identifier AND target_country.key = 'target_country')
                                   LEFT JOIN (countries deal_country) ON (target_country.value = deal_country.id)
                                   LEFT JOIN (regions deal_region) ON (deal_country.fk_region = deal_region.id)LEFT JOIN (a_key_value_lookup intention) ON (a.activity_identifier = intention.activity_identifier AND intention.key = 'intention') LEFT JOIN (a_key_value_lookup deal_count) ON (a.activity_identifier = deal_count.activity_identifier AND deal_count.key = 'deal_count') LEFT JOIN (a_key_value_lookup availability) ON (a.activity_identifier = availability.activity_identifier AND availability.key = 'availability')
          LEFT JOIN (a_key_value_lookup pi_deal) ON (a.activity_identifier = pi_deal.activity_identifier AND pi_deal.key = 'pi_deal')
          LEFT JOIN (a_key_value_lookup deal_scope) ON (a.activity_identifier = deal_scope.activity_identifier AND deal_scope.key = 'deal_scope')
            LEFT JOIN (a_key_value_lookup akv0)
 ON (a.activity_identifier = akv0.activity_identifier AND akv0.key = 'pi_negotiation_status')

          WHERE
            a.version = (SELECT max(version) FROM activities amax, status st WHERE amax.fk_status = st.id AND amax.activity_identifier = a.activity_identifier AND st.name IN ("active", "overwritten", "deleted"))
            AND status.name in ("active", "overwritten")
            AND pi_deal.value = 'True'
            AND (intention.value IS NULL OR intention.value != "Mining")


             AND deal_scope.value = 'transnational'  AND akv0.value IN ('Concluded (Oral Agreement)','Concluded (Contract signed)')
          GROUP BY target_region
         ORDER BY `target_region`  ASC
         ;

""",
            'by_target_country': """
        SELECT DISTINCT
              'target_country' as name,
               deal_country.name as target_country,  GROUP_CONCAT(DISTINCT deal_region.name SEPARATOR '##!##') as target_region, GROUP_CONCAT(DISTINCT intention.value ORDER BY intention.value SEPARATOR '##!##') AS intention,COUNT(DISTINCT a.activity_identifier) as deal_count,SUM(a.availability) / COUNT(a.activity_identifier) as availability,
              'dummy' as dummy
          FROM
            activities a
          JOIN (status) ON (status.id = a.fk_status)
            LEFT JOIN (involvements i, primary_investors pi,
            status pi_st) ON (i.fk_activity = a.id AND i.fk_primary_investor = pi.id AND pi.fk_status = pi_st.id)
                          LEFT JOIN (stakeholders s) ON (i.fk_stakeholder = s.id)
            LEFT JOIN (a_key_value_lookup target_country) ON (a.activity_identifier = target_country.activity_identifier AND target_country.key = 'target_country')
                                   LEFT JOIN (countries deal_country) ON (target_country.value = deal_country.id)
                                   LEFT JOIN (regions deal_region) ON (deal_country.fk_region = deal_region.id)LEFT JOIN (a_key_value_lookup intention) ON (a.activity_identifier = intention.activity_identifier AND intention.key = 'intention') LEFT JOIN (a_key_value_lookup deal_count) ON (a.activity_identifier = deal_count.activity_identifier AND deal_count.key = 'deal_count') LEFT JOIN (a_key_value_lookup availability) ON (a.activity_identifier = availability.activity_identifier AND availability.key = 'availability')
          LEFT JOIN (a_key_value_lookup pi_deal) ON (a.activity_identifier = pi_deal.activity_identifier AND pi_deal.key = 'pi_deal')
          LEFT JOIN (a_key_value_lookup deal_scope) ON (a.activity_identifier = deal_scope.activity_identifier AND deal_scope.key = 'deal_scope')
            LEFT JOIN (a_key_value_lookup akv0)
 ON (a.activity_identifier = akv0.activity_identifier AND akv0.key = 'pi_negotiation_status')

          WHERE
            a.version = (SELECT max(version) FROM activities amax, status st WHERE amax.fk_status = st.id AND amax.activity_identifier = a.activity_identifier AND st.name IN ("active", "overwritten", "deleted"))
            AND status.name in ("active", "overwritten")
            AND pi_deal.value = 'True'
            AND (intention.value IS NULL OR intention.value != "Mining")


             AND deal_scope.value = 'transnational'  AND akv0.value IN ('Concluded (Oral Agreement)','Concluded (Contract signed)')
          GROUP BY target_country
         ORDER BY `target_country`  ASC
         ;


""",
            'by_investor_region': """
        SELECT DISTINCT
              'investor_region' as name,
              CONCAT(investor_region.name, '#!#', investor_region.id) as investor_region,GROUP_CONCAT(DISTINCT intention.value ORDER BY intention.value SEPARATOR '##!##') AS intention,COUNT(DISTINCT a.activity_identifier) as deal_count,SUM(a.availability) / COUNT(a.activity_identifier) as availability,
              'dummy' as dummy
          FROM
            activities a
          JOIN (status) ON (status.id = a.fk_status)
            LEFT JOIN (involvements i, primary_investors pi,
            status pi_st) ON (i.fk_activity = a.id AND i.fk_primary_investor = pi.id AND pi.fk_status = pi_st.id)
                          LEFT JOIN (stakeholders s) ON (i.fk_stakeholder = s.id)

                        LEFT JOIN (sh_key_value_lookup skvl1) ON (s.stakeholder_identifier = skvl1.stakeholder_identifier AND skvl1.key = 'country')
                        LEFT JOIN (countries investor_country) ON (investor_country.id = skvl1.value)
                        LEFT JOIN (regions investor_region) ON (investor_region.id = investor_country.fk_region)LEFT JOIN (a_key_value_lookup intention) ON (a.activity_identifier = intention.activity_identifier AND intention.key = 'intention') LEFT JOIN (a_key_value_lookup deal_count) ON (a.activity_identifier = deal_count.activity_identifier AND deal_count.key = 'deal_count') LEFT JOIN (a_key_value_lookup availability) ON (a.activity_identifier = availability.activity_identifier AND availability.key = 'availability')
          LEFT JOIN (a_key_value_lookup pi_deal) ON (a.activity_identifier = pi_deal.activity_identifier AND pi_deal.key = 'pi_deal')
          LEFT JOIN (a_key_value_lookup deal_scope) ON (a.activity_identifier = deal_scope.activity_identifier AND deal_scope.key = 'deal_scope')
            LEFT JOIN (a_key_value_lookup akv0)
 ON (a.activity_identifier = akv0.activity_identifier AND akv0.key = 'pi_negotiation_status')

          WHERE
            a.version = (SELECT max(version) FROM activities amax, status st WHERE amax.fk_status = st.id AND amax.activity_identifier = a.activity_identifier AND st.name IN ("active", "overwritten", "deleted"))
            AND status.name in ("active", "overwritten")
            AND pi_deal.value = 'True'
            AND (intention.value IS NULL OR intention.value != "Mining")


             AND deal_scope.value = 'transnational'  AND akv0.value IN ('Concluded (Oral Agreement)','Concluded (Contract signed)')
          GROUP BY investor_region
         ORDER BY `investor_region`  ASC
         ;

""",
            'by_investor_country': """
        SELECT DISTINCT
              'investor_country' as name,
              CONCAT(investor_country.name, '#!#', investor_country.code_alpha3) as investor_country,GROUP_CONCAT(DISTINCT CONCAT(investor_region.name, '#!#', investor_region.id) SEPARATOR '##!##') as investor_region,GROUP_CONCAT(DISTINCT intention.value ORDER BY intention.value SEPARATOR '##!##') AS intention,COUNT(DISTINCT a.activity_identifier) as deal_count,SUM(a.availability) / COUNT(a.activity_identifier) as availability,
              'dummy' as dummy
          FROM
            activities a
          JOIN (status) ON (status.id = a.fk_status)
            LEFT JOIN (involvements i, primary_investors pi,
            status pi_st) ON (i.fk_activity = a.id AND i.fk_primary_investor = pi.id AND pi.fk_status = pi_st.id)
                          LEFT JOIN (stakeholders s) ON (i.fk_stakeholder = s.id)

                        LEFT JOIN (sh_key_value_lookup skvl1) ON (s.stakeholder_identifier = skvl1.stakeholder_identifier AND skvl1.key = 'country')
                        LEFT JOIN (countries investor_country) ON (investor_country.id = skvl1.value)
                        LEFT JOIN (regions investor_region) ON (investor_region.id = investor_country.fk_region)LEFT JOIN (a_key_value_lookup intention) ON (a.activity_identifier = intention.activity_identifier AND intention.key = 'intention') LEFT JOIN (a_key_value_lookup deal_count) ON (a.activity_identifier = deal_count.activity_identifier AND deal_count.key = 'deal_count') LEFT JOIN (a_key_value_lookup availability) ON (a.activity_identifier = availability.activity_identifier AND availability.key = 'availability')
          LEFT JOIN (a_key_value_lookup pi_deal) ON (a.activity_identifier = pi_deal.activity_identifier AND pi_deal.key = 'pi_deal')
          LEFT JOIN (a_key_value_lookup deal_scope) ON (a.activity_identifier = deal_scope.activity_identifier AND deal_scope.key = 'deal_scope')
            LEFT JOIN (a_key_value_lookup akv0)
 ON (a.activity_identifier = akv0.activity_identifier AND akv0.key = 'pi_negotiation_status')

          WHERE
            a.version = (SELECT max(version) FROM activities amax, status st WHERE amax.fk_status = st.id AND amax.activity_identifier = a.activity_identifier AND st.name IN ("active", "overwritten", "deleted"))
            AND status.name in ("active", "overwritten")
            AND pi_deal.value = 'True'
            AND (intention.value IS NULL OR intention.value != "Mining")


             AND deal_scope.value = 'transnational'  AND akv0.value IN ('Concluded (Oral Agreement)','Concluded (Contract signed)')
          GROUP BY investor_country
         ORDER BY `investor_country`  ASC
         ;

""",
            'by_investor': """
        SELECT DISTINCT
              'investor_name' as name,
              CONCAT(investor_name.value, '#!#', s.stakeholder_identifier)  as investor_name,GROUP_CONCAT(DISTINCT CONCAT(investor_country.name, '#!#', investor_country.code_alpha3) SEPARATOR '##!##') as investor_country,GROUP_CONCAT(DISTINCT intention.value ORDER BY intention.value SEPARATOR '##!##') AS intention,COUNT(DISTINCT a.activity_identifier) as deal_count,SUM(a.availability) / COUNT(a.activity_identifier) as availability,
              'dummy' as dummy
          FROM
            activities a
          JOIN (status) ON (status.id = a.fk_status)
            LEFT JOIN (involvements i, primary_investors pi,
            status pi_st) ON (i.fk_activity = a.id AND i.fk_primary_investor = pi.id AND pi.fk_status = pi_st.id)
                          LEFT JOIN (stakeholders s) ON (i.fk_stakeholder = s.id)
            LEFT JOIN (sh_key_value_lookup investor_name) ON (s.stakeholder_identifier = investor_name.stakeholder_identifier AND investor_name.key = 'investor_name')
                        LEFT JOIN (sh_key_value_lookup skvl1) ON (s.stakeholder_identifier = skvl1.stakeholder_identifier AND skvl1.key = 'country')
                        LEFT JOIN (countries investor_country) ON (investor_country.id = skvl1.value)
                        LEFT JOIN (regions investor_region) ON (investor_region.id = investor_country.fk_region)LEFT JOIN (a_key_value_lookup intention) ON (a.activity_identifier = intention.activity_identifier AND intention.key = 'intention') LEFT JOIN (a_key_value_lookup deal_count) ON (a.activity_identifier = deal_count.activity_identifier AND deal_count.key = 'deal_count') LEFT JOIN (a_key_value_lookup availability) ON (a.activity_identifier = availability.activity_identifier AND availability.key = 'availability')
          LEFT JOIN (a_key_value_lookup pi_deal) ON (a.activity_identifier = pi_deal.activity_identifier AND pi_deal.key = 'pi_deal')
          LEFT JOIN (a_key_value_lookup deal_scope) ON (a.activity_identifier = deal_scope.activity_identifier AND deal_scope.key = 'deal_scope')
            LEFT JOIN (a_key_value_lookup akv0)
 ON (a.activity_identifier = akv0.activity_identifier AND akv0.key = 'pi_negotiation_status')

          WHERE
            a.version = (SELECT max(version) FROM activities amax, status st WHERE amax.fk_status = st.id AND amax.activity_identifier = a.activity_identifier AND st.name IN ("active", "overwritten", "deleted"))
            AND status.name in ("active", "overwritten")
            AND pi_deal.value = 'True'
            AND (intention.value IS NULL OR intention.value != "Mining")


             AND deal_scope.value = 'transnational'  AND akv0.value IN ('Concluded (Oral Agreement)','Concluded (Contract signed)')
          GROUP BY investor_name
         ORDER BY `investor_name`  ASC
         ;

""",
            'by_intention': """
        SELECT DISTINCT
              'intention' as name,
              intention.value AS intention,COUNT(DISTINCT a.activity_identifier) as deal_count,SUM(a.availability) / COUNT(a.activity_identifier) as availability,
              'dummy' as dummy
          FROM
            activities a
          JOIN (status) ON (status.id = a.fk_status)
            LEFT JOIN (involvements i, primary_investors pi,
            status pi_st) ON (i.fk_activity = a.id AND i.fk_primary_investor = pi.id AND pi.fk_status = pi_st.id)
                          LEFT JOIN (stakeholders s) ON (i.fk_stakeholder = s.id)
            LEFT JOIN (a_key_value_lookup intention) ON (a.activity_identifier = intention.activity_identifier AND intention.key = 'intention') LEFT JOIN (a_key_value_lookup deal_count) ON (a.activity_identifier = deal_count.activity_identifier AND deal_count.key = 'deal_count') LEFT JOIN (a_key_value_lookup availability) ON (a.activity_identifier = availability.activity_identifier AND availability.key = 'availability')
          LEFT JOIN (a_key_value_lookup pi_deal) ON (a.activity_identifier = pi_deal.activity_identifier AND pi_deal.key = 'pi_deal')
          LEFT JOIN (a_key_value_lookup deal_scope) ON (a.activity_identifier = deal_scope.activity_identifier AND deal_scope.key = 'deal_scope')
            LEFT JOIN (a_key_value_lookup akv0)
 ON (a.activity_identifier = akv0.activity_identifier AND akv0.key = 'pi_negotiation_status')

          WHERE
            a.version = (SELECT max(version) FROM activities amax, status st WHERE amax.fk_status = st.id AND amax.activity_identifier = a.activity_identifier AND st.name IN ("active", "overwritten", "deleted"))
            AND status.name in ("active", "overwritten")
            AND pi_deal.value = 'True'
            AND (intention.value IS NULL OR intention.value != "Mining")


             AND deal_scope.value = 'transnational'  AND akv0.value IN ('Concluded (Oral Agreement)','Concluded (Contract signed)')
          GROUP BY intention
         ORDER BY `intention`  ASC
         ;

""",
            'by_data_source_type': """
        SELECT DISTINCT
              'data_source_type' as name,
               data_source_type.value AS data_source_type, GROUP_CONCAT(DISTINCT intention.value ORDER BY intention.value SEPARATOR '##!##') AS intention,COUNT(DISTINCT a.activity_identifier) as deal_count,SUM(a.availability) / COUNT(a.activity_identifier) as availability,
              'dummy' as dummy
          FROM
            activities a
          JOIN (status) ON (status.id = a.fk_status)
            LEFT JOIN (involvements i, primary_investors pi,
            status pi_st) ON (i.fk_activity = a.id AND i.fk_primary_investor = pi.id AND pi.fk_status = pi_st.id)
                          LEFT JOIN (stakeholders s) ON (i.fk_stakeholder = s.id)
            LEFT JOIN (a_key_value_lookup data_source_type) ON (a.activity_identifier = data_source_type.activity_identifier AND data_source_type.key = 'type') LEFT JOIN (a_key_value_lookup intention) ON (a.activity_identifier = intention.activity_identifier AND intention.key = 'intention') LEFT JOIN (a_key_value_lookup deal_count) ON (a.activity_identifier = deal_count.activity_identifier AND deal_count.key = 'deal_count') LEFT JOIN (a_key_value_lookup availability) ON (a.activity_identifier = availability.activity_identifier AND availability.key = 'availability')
          LEFT JOIN (a_key_value_lookup pi_deal) ON (a.activity_identifier = pi_deal.activity_identifier AND pi_deal.key = 'pi_deal')
          LEFT JOIN (a_key_value_lookup deal_scope) ON (a.activity_identifier = deal_scope.activity_identifier AND deal_scope.key = 'deal_scope')
            LEFT JOIN (a_key_value_lookup akv0)
 ON (a.activity_identifier = akv0.activity_identifier AND akv0.key = 'pi_negotiation_status')

          WHERE
            a.version = (SELECT max(version) FROM activities amax, status st WHERE amax.fk_status = st.id AND amax.activity_identifier = a.activity_identifier AND st.name IN ("active", "overwritten", "deleted"))
            AND status.name in ("active", "overwritten")
            AND pi_deal.value = 'True'
            AND (intention.value IS NULL OR intention.value != "Mining")


             AND deal_scope.value = 'transnational'  AND akv0.value IN ('Concluded (Oral Agreement)','Concluded (Contract signed)')
          GROUP BY data_source_type
         ORDER BY `data_source_type`  ASC
         ;

""",
            'by_crop': """
        SELECT DISTINCT
              'crop' as name,
              CONCAT(crop.name, '#!#', crop.code ) AS crop,GROUP_CONCAT(DISTINCT intention.value ORDER BY intention.value SEPARATOR '##!##') AS intention,COUNT(DISTINCT a.activity_identifier) as deal_count,SUM(a.availability) / COUNT(a.activity_identifier) as availability,
              'dummy' as dummy
          FROM
            activities a
          JOIN (status) ON (status.id = a.fk_status)
            LEFT JOIN (involvements i, primary_investors pi,
            status pi_st) ON (i.fk_activity = a.id AND i.fk_primary_investor = pi.id AND pi.fk_status = pi_st.id)
                          LEFT JOIN (stakeholders s) ON (i.fk_stakeholder = s.id)
            LEFT JOIN (a_key_value_lookup akvl1) ON (a.activity_identifier = akvl1.activity_identifier AND akvl1.key = 'crops')
                               LEFT JOIN (crops crop) ON (crop.id = akvl1.value)LEFT JOIN (a_key_value_lookup intention) ON (a.activity_identifier = intention.activity_identifier AND intention.key = 'intention') LEFT JOIN (a_key_value_lookup deal_count) ON (a.activity_identifier = deal_count.activity_identifier AND deal_count.key = 'deal_count') LEFT JOIN (a_key_value_lookup availability) ON (a.activity_identifier = availability.activity_identifier AND availability.key = 'availability')
          LEFT JOIN (a_key_value_lookup pi_deal) ON (a.activity_identifier = pi_deal.activity_identifier AND pi_deal.key = 'pi_deal')
          LEFT JOIN (a_key_value_lookup deal_scope) ON (a.activity_identifier = deal_scope.activity_identifier AND deal_scope.key = 'deal_scope')
            LEFT JOIN (a_key_value_lookup akv0)
 ON (a.activity_identifier = akv0.activity_identifier AND akv0.key = 'pi_negotiation_status')

          WHERE
            a.version = (SELECT max(version) FROM activities amax, status st WHERE amax.fk_status = st.id AND amax.activity_identifier = a.activity_identifier AND st.name IN ("active", "overwritten", "deleted"))
            AND status.name in ("active", "overwritten")
            AND pi_deal.value = 'True'
            AND (intention.value IS NULL OR intention.value != "Mining")


             AND deal_scope.value = 'transnational'  AND akv0.value IN ('Concluded (Oral Agreement)','Concluded (Contract signed)')
          GROUP BY crop
         ORDER BY `crop`  ASC
         ;

""",
        }

if __name__ == '__main__':
    compare = Compare()
    compare.run()
    compare.show(sql=True, warnings=True)
