__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from .subquery_builder import SubqueryBuilder, SQLBuilder

from django.db import connection
from django.conf import settings

class RecordReader:

    def __init__(self, filters, columns):
        self.filters = filters
        self.columns = columns

    def get_all(self):
        sql = SQLBuilder.create(self.filters, self.columns).get_sql()

        if (False and settings.DEBUG): print('*'*80, 'SQL: \n', sql)

        cursor = connection.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def get_column(self, column):
        if not column in self.columns: raise KeyError('Column %s not in columns' % column)
        builder = SubqueryBuilder(self.filters, self.columns)