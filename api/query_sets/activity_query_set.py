import json
from pprint import pprint

from api.query_sets.sql_generation.record_reader import RecordReader
from grid.views.profiling_decorators import print_execution_time_and_num_queries
from grid.views.view_aux_functions import FILTER_VAR_INV

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class ActivityQuerySet:

    DEBUG = False

    def __init__(self, request):
        data = request.POST.get('data', '{"filters": {}, "columns": {}}')
        self.data = json.loads(data)
        for filter in request.session.get('filters', {}).items():
            self.data['filters'][get_filter_name(filter)]['tags'].update(get_filter_definition(filter))
        if self.DEBUG: pprint(self.data['filters'], width=120, compact=True)
        if 'columns' not in self.data:
            self.data['columns'] = {}

    @print_execution_time_and_num_queries
    def all(self):
        return {
            "errors": [],
            "activities":  self._get_activities_by_filter_and_grouping(self.data["filters"], self.data["columns"])
        }

    @print_execution_time_and_num_queries
    def _get_activities_by_filter_and_grouping(self, filters, columns):

        # if filters.get('group_value') == '':
        reader = RecordReader(filters, columns)
        if self.DEBUG:
            print(reader.get_all_sql())
        return reader.get_all(assemble=reader._make_padded_record_from_column_data)


def get_filter_name(filter_data):
    if filter_data[0] in FILTER_VAR_INV:
        return 'investor'
    return 'activity'


def get_filter_definition(filter_data):
    filter_data = filter_data[1]
    value = filter_data['value'][0]
    if '[' in value:
        value = [str(v) for v in json.loads(value)]
    variable = filter_data['variable'][0]
    operator = filter_data['operator'][0]
    return {'{}__{}'.format(variable, operator): value}
