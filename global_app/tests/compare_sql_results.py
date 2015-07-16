from setuptools.command.setopt import setopt

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

#
# make script run in django context.
#
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

#
# actual script follows.
#
from global_app.views import DummyActivityProtocol

from django.http import HttpRequest
from django.db import connection
from django.db.utils import ProgrammingError

import os
import json
import time

# first column is thrown away anyway
def _throwaway_column(expected, actual): return True
# data messed up, not all intended use got carried over in MySQL to PostgreSQL conversion
def _actual_intention_in_expected(expected, actual):
    return set(actual.split('##!##')) <= set(expected.split('##!##'))
def _floats_pretty_equal(expected, actual):
    return 0.99 <= expected/actual <= 1.01
# empty years are converted to zero by new SQL. who cares.
def _null_to_zero_conversion(expected, actual):
    return expected[:-1] == actual if isinstance(expected, str) and expected.endswith('#0') else expected == actual
def _same_string_multiple_times(expected, actual):
    return set(expected.split('##!##')) <= set(actual.split('##!##'))
def _none_is_equaled(expected, actual):
    if expected == None and '#!#' in actual and actual.startswith('#'): return True
    return expected == actual

class Compare:

    NUM_COMPARED_RECORDS = 100

    files_to_compare = [
        'by_crop', 'by_data_source_type', 'by_intention', 'by_investor',
        'by_investor_country', 'by_investor_region', 'by_target_country', 'by_target_region', 'all_deals',
    ]
    warnings = {}
    errors = {}
    sql = {}

    _died = False
    _starttime = 0
    _filename = ''

    def run(self):

        self._starttime = time.time()

        try:
            for self._filename in self.files_to_compare:
                self._compare_with_expected()

        except ProgrammingError as e:
            print(e)
            print(connection.queries[-1]['sql'])
            self._died = True

    def show(self, sql=False, warnings=True):
        if self._died: return
        if sql: self._print_messages(self.sql, 'SQL', '.')
        if warnings: self._print_messages(self.warnings, 'Warnings', '=')
        self._print_messages(self.errors, 'Errors', '*')

    def num_errors(self):
        return sum(len(messages) for messages in self.errors.values())

    def _compare_with_expected(self):

        postdata, records = self._read_data('landmatrix_' + self._filename+'.out')
        protocol = DummyActivityProtocol()
        res = protocol.dispatch(self._prepare_request(postdata), action="list_group").content
        query_result = json.loads(res.decode())['activities'][:self.NUM_COMPARED_RECORDS]
        self.sql[self._filename] = [connection.queries[-1]['sql'] if connection.queries else 'WHAT? NO QUERIES? ' + self._filename]

        if len(query_result) != len(records):
            self._add_error('NUMBER OF RECORDS NOT EQUAL: expected %d, got %d' %(len(records), len(query_result)))
            self._add_error(records)
            self._add_error(query_result)
            return

        self._compare_all_items(query_result, records)

    def _prepare_request(self, postdata):
        request = HttpRequest()
        request.POST = {'data': postdata}
        return request

    def _compare_all_items(self, query_result, records):
        for id in range(0, len(records)):
            self._compare_item(records[id], query_result[id])

    def _compare_item(self, expected, got):
        for j in range(0, len(expected)):
            if not self._equal(j, expected[j], got[j]):
                add_message = self._add_warning if self._similar(j, expected[j], got[j]) else self._add_error
                add_message("%-20s field %2i: expected %-24s got %-24s" % (str(expected[1]), j, str(expected[j]), str(got[j])))

    def _print_messages(self, container, what, headerchar):
        if not container: return
        for file, messages in container.items():
            print(headerchar*80, what+': '+file, headerchar*80, sep='\n')
            print(*messages, sep="\n")
            print(headerchar*4, ' '*2, len(messages), what)
        print(headerchar*4, ' '*2, 'Total:', sum(len(messages) for messages in container.values()), what)
        print(headerchar*4, ' '*2, 'Elapsed:', time.time() - self._starttime)

    def _read_data(self, filename):
        with open(os.path.dirname(os.path.realpath(__file__)) + '/data/' + filename, 'r') as f:
            lines = f.readlines()
        parameters = eval(lines[1])
        records = eval(lines[2])
        return (parameters['data'], records[:self.NUM_COMPARED_RECORDS])

    def _add_message(self, container, message):
        if not self._filename in container.keys():
            container[self._filename] = []
        container[self._filename].append(str(message))

    def _add_error(self, error):
        self._add_message(self.errors, error)

    def _add_warning(self, warning):
        self._add_message(self.warnings, warning)

    def _equal(self, field, expected, actual):
        return expected == actual

    similar_table = {
        'all_deals': {
            3: _same_string_multiple_times,
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
            1: _none_is_equaled,
            2: _actual_intention_in_expected,
            4: _floats_pretty_equal
        },
        'by_investor_country': {
            0: _throwaway_column,
            1: _none_is_equaled,
            2: _none_is_equaled,
            3: _actual_intention_in_expected,
            5: _floats_pretty_equal
        },
        'by_investor': {
            0: _throwaway_column,
            1: _none_is_equaled,
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
            1: _none_is_equaled,
        }
    }
    def _similar(self, field, expected, actual):
        if field in self.similar_table[self._filename]:
            return self.similar_table[self._filename][field](expected, actual)
        return False

    def num_errors(self):
        return sum(len(messages) for messages in self.errors.values())

def run_test(sql, warnings):
    from django.conf import settings
    compare = Compare()
    compare.run()
    compare.show(sql=sql, warnings=warnings)
    return compare.num_errors()

def read_args():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-e', '--show-errors', default=True)
    parser.add_argument('-w', '--show-warnings', action="store_true")
    parser.add_argument('-s', '--show-sql', action="store_true")
    return parser.parse_args()


if __name__ == '__main__':
    args = read_args()
    sys.exit(run_test(args.show_sql, args.show_warnings))
