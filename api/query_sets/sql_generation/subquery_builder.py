__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from api.query_sets.sql_generation.join_functions import join_attributes
from api.query_sets.sql_generation.list_sql_builder import ListSQLBuilder


class SubqueryBuilder(ListSQLBuilder):

    def column_sql(self, c):
        try:
            return self.SQL_COLUMN_MAP.get(c)[0]
        except TypeError:
            raise KeyError(c)

    def get_group_sql(self):
        group_by = ["a.id "] + [col for col in self.columns if not self.is_aggregate_column(col)]
        return 'GROUP BY ' + ', '.join(group_by)

    @classmethod
    def get_base_sql(cls):
        return u"""SELECT DISTINCT
a.activity_identifier,
%(columns)s, a.id AS id
FROM landmatrix_activity AS a
%(from)s
LEFT JOIN landmatrix_publicinterfacecache   AS pi        ON a.id = pi.fk_activity_id AND pi.is_deal
""" + join_attributes('deal_scope') + """
%(from_filter)s
WHERE """ + "\nAND ".join([ cls.max_version_condition(), cls.status_active_condition(), cls.is_deal_condition(), cls.not_mining_condition() ]) + """
%(where)s
%(where_filter)s
%(group_by)s"""
