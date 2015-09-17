__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django.db.models.query import QuerySet
from django.db import connection


class FakeModel(dict):
    pk = None


class FakeQuerySet(QuerySet):

    DEBUG = False

    _filter_sql = ''

    def __init__(self):
        self._all_results = []
        super().__init__()

    def all(self):
        self._fetch_all()
        return self._all_results

    @classmethod
    def set_filter_sql(cls, filter):
        cls._filter_sql = filter

    def sql_query(self):
        return self.QUERY % self._filter_sql

    def _fetch_all(self):
        if not self._all_results:
            for result in self._execute_query():
                try:
                    as_dict = {self.fields[i][0]: result[i] for i in range(len(self.fields))}
                except KeyError:
                    raise RuntimeError('You probably haven\'t defined the correct fields for your FakeQuerySet.')
                as_model = FakeModel(as_dict)
                self._all_results.append(as_model)

    def _execute_query(self):
        if self.DEBUG:
            print('Query:', self.sql_query())
        cursor = connection.cursor()
        cursor.execute(self.sql_query())
        all_results = list(cursor.fetchall())
        if self.DEBUG:
            print('Results:', all_results)
        return all_results
