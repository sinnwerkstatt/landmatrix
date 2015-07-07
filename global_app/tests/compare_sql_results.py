__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

import os
import pprint
from django.http import HttpRequest
from django.utils.datastructures import MultiValueDict
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

class Compare:

    files_to_compare = ['by_target_region', 'all_deals', ]
    warnings = {}
    errors = {}
    sql = {}

    filename = ''
    def run(self):
        for self.filename in self.files_to_compare:
            self.compare_with_expected()

        self._print_messages(self.sql, 'SQL', '.')
        self._print_messages(self.warnings, 'Warnings', '=')
        self._print_messages(self.errors, 'Errors', '*')

    def compare_with_expected(self):
        postdata, records = self.read_data(self.filename+'.out')
        protocol = DummyActivityProtocol()
        request = HttpRequest()
        request.POST = {'data': postdata}
        res = protocol.dispatch(request, action="list_group").content
        self.sql[self.filename] = [connection.queries[-1]['sql']]
        query_result = json.loads(res.decode())['activities'][:10]

        if len(query_result) != len(records):
            self.add_error('NUMBER OF RECORDS NOT EQUAL:')
            self.add_error(records)
            self.add_error(query_result)
            return

        for id in range(0, len(records)):
            for j in range(0, len(records[id])):
                if not self.equal(j, records[id][j], query_result[id][j]):
                    func = self.add_warning if self.similar(j, records[id][j], query_result[id][j]) else self.add_error
                    func("ID: %s, field %i: expected %s, got %s" % (str(records[id][1]), j, str(records[id][j]), str(query_result[id][j])))

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
        return (parameters['data'][0], records[:10])
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
            # data messed up, not all intended use got carried over in MySQL to PostgreSQL conversion
            6: lambda expected, actual: set(actual.split('##!##')) <= set(expected.split('##!##')),
            # empty years are converted to zero by new SQL. whatever.
            7: lambda expected, actual: expected[:-1] == actual if isinstance(expected, str) and expected.endswith('#0') else expected == actual,
            8: lambda expected, actual: expected[:-1] == actual if isinstance(expected, str) and expected.endswith('#0') else expected == actual,
        },
        'by_target_region': {
            # first column is thrown away anyway
            0: lambda expected, actual: True,
            # data messed up, not all intended use got carried over in MySQL to PostgreSQL conversion
            2: lambda expected, actual: set(actual.split('##!##')) <= set(expected.split('##!##')),
            # tolerate small differences in floaing point numbers
            4: lambda expected, actual: 0.99 <= expected/actual <= 1.01
        },
    }
    def similar(self, field, expected, actual):
        if field in self.similar_table[self.filename]:
            return self.similar_table[self.filename][field](expected, actual)
        return False


if __name__ == '__main__':
    compare = Compare()
    compare.run()
