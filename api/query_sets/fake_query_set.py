__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django.db.models.query import QuerySet
from django.db import connection


class FakeModel(dict):
    pk = None


class FakeQuerySet:

    DEBUG = False

    _filter_sql = ''

    def __init__(self):
        self._all_results = []

    def all(self):
        self._fetch_all()
        return self._all_results

    def _fetch_all(self):
        if not self._all_results:
            cursor = connection.cursor()
            cursor.execute(self.sql_query())
            all_results = list(cursor.fetchall())
            if self.DEBUG or False:
                print('Query:', self.sql_query())
                print('Results:', all_results)

            for result in all_results:
                as_tuple = result
                as_dict = FakeModel({ self.fields[i][0]: as_tuple[i] for i in range(len(self.fields)) })
                self._all_results.append(as_dict)

    @classmethod
    def set_filter_sql(cls, filter):
        cls._filter_sql = filter

    def sql_query(self):
        return self.QUERY % self._filter_sql
