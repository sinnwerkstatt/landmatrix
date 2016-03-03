
__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from landmatrix.models.public_interface_cache import PublicInterfaceCache
from api.query_sets.sql_generation.join_functions import join, join_attributes
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
""" + join(PublicInterfaceCache, 'pi', 'a.id = pi.fk_activity_id AND pi.is_deal') + '\n'\
    + join_attributes('deal_scope') + """
%(from_filter)s
WHERE """ + "\nAND ".join([
            cls.status_active_condition(), cls.is_deal_condition(), cls.not_mining_condition()
        ]) + """
%(where)s
%(where_filter)s
%(group_by)s"""
