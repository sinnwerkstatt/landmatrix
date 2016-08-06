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
from grid.views.activity_protocol import ActivityProtocol
from api.query_sets.sql_generation.record_reader import RecordReader

RecordReader.DEBUG = False
DEFAULT_FLOATS_SIMILAR_DEVIATION = 0.001
# these are basically meaningless and ignore unexplainable differences in availability aggregation.
# aggregated availability values are mostly nonsense anyway though.
FLOATS_SIMILAR_DEVIATION = {
    'by_target_country': 0.17,
    'by_target_region': 0.04,
    'by_crop': 0.13,
    'by_intention': 0.07,
    'by_data_source_type': 0.03
}

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
    if None in actual: actual.remove(None)
    if not expected: return not actual
    return set(expected.split('##!##')) <= set(actual)

def _floats_pretty_equal(difference):
    def do_comparison(expected, actual):
        return 1-difference <= expected/actual <= 1+difference
    return do_comparison

# empty years are converted to zero by new SQL. who cares.
def _null_to_zero_conversion(expected, actual):
    return expected[:-1] == actual if isinstance(expected, str) and expected.endswith('#0') else expected == actual

def _same_string_multiple_times(expected, actual):
    if isinstance(expected, str):
        return set(expected.split('##!##')) <= set(actual)
    return set(expected) <= set(actual)

def _none_is_equaled(expected, actual):
    if expected == None and '#!#' in actual and actual.startswith('#'): return True
    if expected == None: return not actual
    return expected == actual

def _array_equal_to_tinkered_string(expected, actual):
    # return set(expected.split('##!##')) <= set(actual)
    return _same_string_multiple_times(expected, actual)

class Compare:

    NUM_COMPARED_RECORDS = 5000

    files_to_compare = [
        'by_crop',
        'by_data_source_type',
        'by_intention',
        # 'by_investor_country',
        'by_investor',
        # 'by_investor_region',
        'by_target_country',
        'by_target_region',
        'all_deals',
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
        protocol = ActivityProtocol()
        res = protocol.dispatch(self._prepare_request(postdata), action="list_group").content
        query_result = json.loads(res.decode())['activities'][:self.NUM_COMPARED_RECORDS]
        self.sql[self._filename] = [connection.queries[-1]['sql'] if connection.queries else 'WHAT? NO QUERIES? ' + self._filename]

        if len(query_result) != len(records):
            self._add_error('NUMBER OF RECORDS NOT EQUAL: expected %d, got %d' %(len(records), len(query_result)))
            self._add_error('missing: ' + str(record_difference(records, query_result)))
            self._add_error('additional: '+ str(record_difference(query_result, records)))
            return

        self._compare_all_items(query_result, records)

    def _prepare_request(self, postdata):
        from django.conf import settings
        from django.utils.importlib import import_module
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        session_key = None
        request.session = engine.SessionStore(session_key)
        postdata = self._adjust_postdata_to_new_investor_model(postdata)
        request.POST = {'data': postdata}
        return request

    def _adjust_postdata_to_new_investor_model(self, postdata):
        return postdata.replace('primary_investor', 'operational_stakeholder').replace('investor', 'stakeholder')

    def _compare_all_items(self, query_result, records):
        for id in range(0, min(len(records), len(query_result))):
            self._compare_item(records[id], query_result[id])

    def _compare_item(self, expected, got):
        for j in range(0, len(expected)):
            if not self._equal(j, expected[j], got[j]):
                add_message = self._add_warning if self._similar(j, expected[j], got[j]) else self._add_error
                add_message("%-20s field %2i: expected %-24s got %-24s" % (str(expected[1]), j, '"'+str(expected[j])+'"', str(got[j])))

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
        parameters = eval(lines[0])
        records = eval(lines[1])
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
            2: _array_equal_to_tinkered_string,
            3: _same_string_multiple_times,
            4: _array_equal_to_tinkered_string,
            5: _array_equal_to_tinkered_string,
            6: _actual_intention_in_expected,
            7: _array_equal_to_tinkered_string,
            8: _array_equal_to_tinkered_string,
        },
        'by_target_region': {
            0: _throwaway_column,
            2: _actual_intention_in_expected,
            4: _floats_pretty_equal(FLOATS_SIMILAR_DEVIATION.get('by_target_region', DEFAULT_FLOATS_SIMILAR_DEVIATION)),
        },
        'by_target_country': {
            0: _throwaway_column,
            2: _array_equal_to_tinkered_string,
            3: _actual_intention_in_expected,
            5: _floats_pretty_equal(FLOATS_SIMILAR_DEVIATION.get('by_target_country', DEFAULT_FLOATS_SIMILAR_DEVIATION)),
        },
        'by_investor_region': {
            0: _throwaway_column,
            1: _none_is_equaled,
            2: _actual_intention_in_expected,
            4: _floats_pretty_equal(FLOATS_SIMILAR_DEVIATION.get('by_investor_region', DEFAULT_FLOATS_SIMILAR_DEVIATION))
        },
        'by_investor_country': {
            0: _throwaway_column,
            1: _none_is_equaled,
            2: _array_equal_to_tinkered_string,
            3: _actual_intention_in_expected,
            5: _floats_pretty_equal(FLOATS_SIMILAR_DEVIATION.get('by_investor_country', DEFAULT_FLOATS_SIMILAR_DEVIATION))
        },
        'by_investor': {
            0: _throwaway_column,
            1: _none_is_equaled,
            2: _array_equal_to_tinkered_string,
            3: _actual_intention_in_expected,
            5: _floats_pretty_equal(FLOATS_SIMILAR_DEVIATION.get('by_investor', DEFAULT_FLOATS_SIMILAR_DEVIATION))
        },
        'by_intention': {
            0: _throwaway_column,
            3: _floats_pretty_equal(FLOATS_SIMILAR_DEVIATION.get('by_intention', DEFAULT_FLOATS_SIMILAR_DEVIATION)),
        },
        'by_data_source_type': {
            0: _throwaway_column,
            2: _actual_intention_in_expected,
            4: _floats_pretty_equal(FLOATS_SIMILAR_DEVIATION.get('by_data_source_type', DEFAULT_FLOATS_SIMILAR_DEVIATION)),
        },
        'by_crop': {
            0: _throwaway_column,
            1: _none_is_equaled,
            2: _actual_intention_in_expected,
            4: _floats_pretty_equal(FLOATS_SIMILAR_DEVIATION.get('by_crop', DEFAULT_FLOATS_SIMILAR_DEVIATION)),
        }
    }
    def _similar(self, field, expected, actual):
        if field in self.similar_table[self._filename]:
            return self.similar_table[self._filename][field](expected, actual)
        return False


def record_difference(records1, records2):
    records1 = set(lists_to_tuples(records1))
    records2 = set(lists_to_tuples(records2))
    try:
        return sorted(list(records1 - records2))
    except TypeError:
        # print(records1, records2)
        pass


def list_contains_lists(collection):
    if not collection: return False
    if not hasattr(collection, '__iter__'): return False
    if isinstance(collection, str): return False
    for item in collection:
        if isinstance(item, list):
            return True
    return False


def lists_to_tuples(collection):
    return [list_item_to_tuple(record) for record in collection]


def list_item_to_tuple(item):
    if list_contains_lists(item):
        return tuple(lists_to_tuples(item))[:2]
    elif hasattr(item, '__iter__') and not isinstance(item, str):
        return tuple(item)[:2]
    else:
        return item


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
