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


# first column is thrown away anyway
def _throwaway_column(expected, actual): return True
# data messed up, not all intended use got carried over in MySQL to PostgreSQL conversion
def _actual_intention_in_expected(expected, actual): return set(actual.split('##!##')) <= set(expected.split('##!##'))
def _floats_pretty_equal(expected, actual): return 0.99 <= expected/actual <= 1.01
# empty years are converted to zero by new SQL. who cares.
def _null_to_zero_conversion(expected, actual):
    return expected[:-1] == actual if isinstance(expected, str) and expected.endswith('#0') else expected == actual

class Compare:

    NUM_COMPARED_RECORDS = 10

    files_to_compare = [
        'by_investor', 'by_investor_country', 'by_investor_region', 'by_target_country', 'by_target_region', 'all_deals',
    ]
    warnings = {}
    errors = {}
    sql = {}

    _died = False

    filename = ''
    def run(self):
        try:
            for self.filename in self.files_to_compare:
                self.compare_with_expected()

        except ProgrammingError as e:
            print(e)
            print(connection.queries[-1]['sql'])

    def show(self, sql=False, warnings=True):
        if self._died: return
        if sql: self._print_messages(self.sql, 'SQL', '.')
        if warnings: self._print_messages(self.warnings, 'Warnings', '=')
        self._print_messages(self.errors, 'Errors', '*')

    def compare_with_expected(self):
        postdata, records = self.read_data(self.filename+'.out')
        protocol = DummyActivityProtocol()
        request = HttpRequest()
        request.POST = {'data': postdata}
        res = protocol.dispatch(request, action="list_group").content
        self.sql[self.filename] = [connection.queries[-1]['sql']]
        query_result = json.loads(res.decode())['activities'][:self.NUM_COMPARED_RECORDS]

        if len(query_result) != len(records):
            self.add_error('NUMBER OF RECORDS NOT EQUAL:')
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

    def read_data(self, filename):
        with open(os.path.dirname(os.path.realpath(__file__)) + '/' + filename, 'r') as f:
            lines = f.readlines()
        parameters = eval(lines[1])
        records = eval(lines[2])
        return (parameters['data'][0], records[:self.NUM_COMPARED_RECORDS])
        return ((parse_post_data(parameters)), records[:10])

    def _add_message(self, container, message):
        if not self.filename in container.keys():
            container[self.filename] = []
        container[self.filename].append(str(message))

    def add_error(self, error):
        self._add_message(self.errors, error)

    def add_warning(self, warning):
        self._add_message(self.warnings, warning)

    def parse_post_data(self, parameters):
        null = None
        return eval(parameters['data'][0])


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
            5: _floats_pretty_equal
        },
        'by_intention': {},
        'by_data_source_type': {},
        'by_crop': {}
    }
    def similar(self, field, expected, actual):
        if field in self.similar_table[self.filename]:
            return self.similar_table[self.filename][field](expected, actual)
        return False


if __name__ == '__main__':
    compare = Compare()
    compare.run()
    compare.show(warnings=False)
