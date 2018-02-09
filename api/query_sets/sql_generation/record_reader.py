from api.query_sets.sql_generation.sql_builder import SQLBuilder
from api.query_sets.sql_generation.subquery_builder import SubqueryBuilder

from django.db import connection


class RecordReader:

    DEBUG = False

    def __init__(self, filters, columns, status, is_staff=False):
        self.filters = filters
        self.columns = columns
        self.status = status
        if self.DEBUG:
            print('*'*80, 'Filters: \n', filters)
            print('*'*80, 'columns: \n', columns)
        self.is_staff = is_staff

    def get_all(self, assemble=None):
        #if list_view_wanted(self.filters):
        #    records = self._slap_columns_together(assemble)
        #else:
        #    records = self.get_all_at_once()
        return self.get_all_at_once()

    def get_all_sql(self):
        #if list_view_wanted(self.filters):
        #    sql = ''
        #    for column in self.columns:
        #        sql += '\n' + self.get_column_sql(column)
        #    return sql
        return self.get_all_at_once_sql()

    def get_column(self, column):
        if not column in self.columns:
            raise KeyError('Column %s not in columns' % column)
        return self._execute_sql(self.get_column_sql(column))

    def get_column_sql(self, column):
        columns = [column]
        order_by = self.filters.get('order_by', [])
        if not order_by:
            order_by = ['deal_id']
        for c in order_by:
            if c.strip('-') not in columns:
                columns.append(c.strip('-'))
        return SubqueryBuilder(self.filters, columns, self.status, self.is_staff).get_sql()

    def get_all_at_once(self):
        return self._execute_sql(self.get_all_at_once_sql())

    def get_all_at_once_sql(self):
        return SQLBuilder.create(self.filters, self.columns, self.status, self.is_staff).get_sql()

    def _execute_sql(self, sql):
        import time
        start_time = time.time()

        if self.DEBUG:
            print('*'*80, 'SQL: \n', sql)

        cursor = connection.cursor()
        cursor.execute(sql)

        if self.DEBUG:
            print('*'*40, 'execution time:', time.time() - start_time)

        return cursor.fetchall()

    #def _slap_columns_together(self, assemble=None):
    #    assemble = assemble or self._make_record_from_column_data
    #
    #    column_data = self.get_all_columns()
    #
    #    final_data = []
    #    for i in range(0, len(column_data.get(self.columns[0], []))):
    #        self._ensure_records_equal(column_data, i)
    #        record = assemble(column_data, i)
    #        final_data.append(record)
    #    return final_data

    def get_all_columns(self):
        from django.db.utils import ProgrammingError

        column_data = dict()

        for column in self.columns:
            try:
                column_data[column] = self.get_column(column)
            except ProgrammingError as e:
                print('SQL for column "%s" failed:\n%s' % (column, self.get_column_sql(column)))
                raise

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
