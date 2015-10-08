import json
from api.query_sets.sql_generation.record_reader import RecordReader

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class ActivityQuerySet:

    DEBUG = False

    def __init__(self, post_data):
        data = post_data.get('data', '{"filters": {}, "columns": {}}')
        self.data = json.loads(data)

    def all(self):
        return {
            "errors": [],
            "activities":  self._get_activities_by_filter_and_grouping(self.data["filters"], self.data["columns"])
        }

    def _get_activities_by_filter_and_grouping(self, filters, columns):

        # if filters.get('group_value') == '':
        reader = RecordReader(filters, columns)
        if self.DEBUG:
            print(reader.get_all_sql())
        return reader.get_all(assemble=reader._make_padded_record_from_column_data)
