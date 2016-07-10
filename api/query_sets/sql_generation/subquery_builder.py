
__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from api.query_sets.sql_generation.join_functions import join, join_attributes
from api.query_sets.sql_generation.list_sql_builder import ListSQLBuilder


class SubqueryBuilder(ListSQLBuilder):

    def column_sql(self, column):
        column = column.strip('-')
        if column in self.SQL_COLUMN_MAP:
            return self.SQL_COLUMN_MAP.get(column)[0]
        else:
            # Move this as a fallback to SQLBuilderData
            return "ARRAY_AGG(DISTINCT %(column)s.value) AS %(column)s" % {
            #return "ARRAY_AGG(DISTINCT %(column)s.value) AS %(column)s" % {
                'column': column
            }

    def get_group_sql(self):
        group_by = ["a.id "] + [col for col in self.columns if not self.is_aggregate_column(col)]
        return 'GROUP BY ' + ', '.join(group_by)

    def get_base_sql(self):
        return u"""SELECT DISTINCT
a.activity_identifier,
%(columns)s, a.id AS id
FROM landmatrix_activity AS a
%(from)s
""" + join_attributes('deal_scope') + """
%(from_filter)s
WHERE """ + "\nAND ".join(filter(None, [
            self.status_active_condition(),
            self.is_public_condition(),
            self.not_mining_condition()
        ])) + """
%(where)s
%(where_filter)s
%(group_by)s
%(order_by)s
"""
