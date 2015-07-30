__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from landmatrix.models import ActivityAttributeGroup, Activity, Crop

from django.db import connection
from copy import deepcopy

def get_monkey_patch(columns, group):
    if True:
        return DummyMonkeyPatch(columns, group)
    else:
        return ColumnMonkeyPatch(columns, group)

class DummyMonkeyPatch:

    def __init__(self, columns, group):
        self.columns = columns
        self.group = group

    def is_patched_column(self, c):
        return False

    def _single_column_results(self, query_result):
        return {}

    def _optimize_columns(self):
        return deepcopy(self.columns)

class ColumnMonkeyPatch:

    """ The single columns SQL queries. """
    SINGLE_SQL_QUERIES = {
        'location': """
                SELECT activity_identifier, ARRAY_AGG(DISTINCT aag.attributes->'location') AS location
                FROM """+ Activity._meta.db_table + " AS a JOIN " + ActivityAttributeGroup._meta.db_table+""" AS aag ON a.id = aag.fk_activity_id
                WHERE aag.attributes ? 'location' AND activity_identifier IN (%s)
                group by activity_identifier;
        """,
        'crop': """
                SELECT activity_identifier, ARRAY_AGG(DISTINCT CONCAT(crops.name, '#!#', crops.code )) AS crop
                FROM """ + Activity._meta.db_table + " AS a JOIN " + ActivityAttributeGroup._meta.db_table+""" AS aag ON a.id = aag.fk_activity_id
                JOIN """ + Crop._meta.db_table + """ AS crops ON CAST(aag.attributes->'crops' AS NUMERIC) = crops.id
                WHERE aag.attributes ? 'crops' and activity_identifier in (%s)
                group by activity_identifier;
        """
    }

    def __init__(self, columns, group):
        self.columns = columns
        self.group = group

    def is_patched_column(self, c):
        return c in self.affected_columns() and not self.extra_special_treatment(c)

    def _single_column_results(self, query_result):

        single_column_results = {}
        activity_ids = None
        for col in self.affected_columns():
            # do not remove crop column if we expect a grouping in the sql string
            if col not in self.columns or self.extra_special_treatment(col):
                continue
            # get the activity ids from the large sql dataset
            # Assumption: dataset contains column deal_id in second column
            activity_ids = activity_ids or [str(row[0 + 1]) for row in query_result]
            if activity_ids:
                cursor = connection.cursor()
                sql = self.SINGLE_SQL_QUERIES[col] % (','.join(activity_ids))
                cursor.execute(sql)
                single_column_results.update({col: dict(cursor.fetchall())})
        return single_column_results

    def _optimize_columns(self):
        """ IMPORTANT! we are patching certain column fields out, so they don't get executed within the large SQL query.
            Instead we later send a single query for each column and add the resulting data back into the large result
            object.
        """

        if not self.needs_patching():
            return self.columns

        optimized_columns = deepcopy(self.columns)
        for col in self.affected_columns():
            # do not remove crop column if we expect a grouping in the sql string
            if col in self.columns and not self.extra_special_treatment(col):
                optimized_columns.remove(col)

        return optimized_columns

    @classmethod
    def affected_columns(cls):
        return cls.SINGLE_SQL_QUERIES.keys()

    def extra_special_treatment(self, col):
        return self.group == "crop" and col == "crop"

    def needs_patching(self):
        return any(special_column in self.columns for special_column in self.affected_columns())

