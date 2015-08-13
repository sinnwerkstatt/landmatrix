__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django.db import connection
from django.conf import settings

from global_app.views.sql_generation.subquery_builder import SubqueryBuilder
from global_app.views.sql_generation.sql_builder import SQLBuilder, list_view_wanted


class RecordReader:

    def __init__(self, filters, columns):
        self.filters = filters
        self.columns = columns

    def get_all(self, assemble=None):
        if list_view_wanted(self.filters):
            return self._slap_columns_together(assemble)
        return self.get_all_at_once()

    def get_all_sql(self):
        if list_view_wanted(self.filters):
            sql = ''
            for column in self.columns:
                sql += '\n' + self.get_column_sql(column)
            return sql
        return self.get_all_at_once_sql()

    def get_column(self, column):
        if not column in self.columns: raise KeyError('Column %s not in columns' % column)
        return self._execute_sql(self.get_column_sql(column))

    def get_column_sql(self, column):
        return SubqueryBuilder(self.filters, [column]).get_sql()

    def get_all_at_once(self):
        return self._execute_sql(self.get_all_at_once_sql())

    def get_all_at_once_sql(self):
        return SQLBuilder.create(self.filters, self.columns).get_sql()

    def _execute_sql(self, sql):
        if (False and settings.DEBUG): print('*'*80, 'SQL: \n', sql)

        cursor = connection.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def _slap_columns_together(self, assemble=None):
        assemble = assemble or self._make_record_from_column_data

        column_data = self.get_all_columns()
        final_data = []
        for i in range(0, len(column_data[self.columns[0]])):
            self._ensure_records_equal(column_data, i)
            record = assemble(column_data, i)
            final_data.append(record)
        return final_data

    def get_all_columns(self):
        from django.db.utils import ProgrammingError
        from operator import itemgetter

        column_data = dict()
        for column in self.columns:
            try:
                column_data[column] = sorted(self.get_column(column), key=itemgetter(0))
            except ProgrammingError as e:
                print('SQL for column "%s" failed:\n%s' % (column, self.get_column_sql(column)))

        return column_data

    def _ensure_records_equal(self, column_data, i):
        act_ids = [column_data[col][i][0] for col in self.columns]
        equal = all(x == act_ids[0] for x in act_ids)
        if not equal:
            raise RuntimeError("Activity IDs not equal for element %i: %s" % (i, ', '.join(map(str, act_ids))))

    def _make_record_from_column_data(self, column_data, i):
        return tuple(self._record_subset(column_data[col][i]) for col in self.columns)

    def _make_padded_record_from_column_data(self, column_data, i):
        padded_record = ['all deals'] + self._record_core(column_data,i) + ['dummy']
        return tuple(padded_record)

    def _record_core(self, column_data, i):
        core = []
        for col in self.columns:
            core.extend(self._record_subset(column_data[col][i]))
        return core

    def _record_subset(self, field_data):
        return [field_data[1]]
