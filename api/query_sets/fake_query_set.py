__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django.db.models.query import QuerySet
from django.db import connection


class FakeModel(dict):
    pk = None


class FakeQuerySet(QuerySet):

    DEBUG = False

    fields = [('field name', 'sql for field'), ]
    _all_results = None
    _result_iterator = None

    def iterator(self):
        if not self._all_results:
            cursor = connection.cursor()
            cursor.execute(self.sql_query())
            self._all_results = list(cursor.fetchall())
            self._result_iterator = iter(self._all_results)
            if self.DEBUG:
                print('Query:', self.sql_query())
                print('Results:', self._all_results)

        as_tuple = next(self._result_iterator)
        as_dict = FakeModel({ self.fields[i][0]: as_tuple[i] for i in range(len(self.fields)) })
        if self.DEBUG:
            print('as tuple', as_tuple)
            print('as dict', as_dict)
        yield as_dict

    def sql_query(self):
        return self.QUERY