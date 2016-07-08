from api.query_sets.sql_generation.join_functions import join, join_attributes
from api.query_sets.sql_generation.list_sql_builder import ListSQLBuilder


__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class SubqueryBuilder(ListSQLBuilder):

    def column_sql(self, column):
        column = column.strip('-')
        # SQL_COLUMN_MAP is a defaultdict and won't raise KeyError
        return self.SQL_COLUMN_MAP[column][0]

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
