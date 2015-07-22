__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from global_app.views.sql_generation.join_functions import join_attributes
from global_app.views.sql_generation.list_sql_builder import ListSQLBuilder


class SubqueryBuilder(ListSQLBuilder):

    def column_sql(self, c):
        if c in ("intended_size", "contract_size", "production_size"):
            return "NULLIF(ARRAY_TO_STRING(ARRAY_AGG(DISTINCT %(name)s.attributes->'%(name)s'), ', '), '') AS %(name)s" % {"name": c}
        elif c == "data_source":
            return self.SQL_COLUMN_MAP.get(c)[0]

        try:
            return self.SQL_COLUMN_MAP.get(c)[0]
        except TypeError as e:
            print('column_sql', c, self.SQL_COLUMN_MAP.get(c))
            raise e
        # elif c == "data_source":
        #     return "data_source_type, data_source_url, data_source_date, data_source_organisation,\n"
        # else:
        #     return "%(name)s,\n" % {"name": c}

    def get_group_sql(self):
        group_by_sql = " GROUP BY a.id "
        additional_group_by = []
        for c in [ col for col in self.columns if not col in ["intended_size", "contract_size", "production_size", "data_source"] and not self._is_aggregate_column(col)]:
            additional_group_by.append("%(name)s" % {"name": c})
        if additional_group_by: group_by_sql += ', ' + ', '.join(additional_group_by)

        return group_by_sql

    def _is_aggregate_column(self, c):
        return any(x in self.SQL_COLUMN_MAP[c][0] for x in ['ARRAY_AGG', 'COUNT'])

    @classmethod
    def get_base_sql(cls):
        return u"""SELECT DISTINCT
a.activity_identifier,
%(columns)s, a.id AS id
FROM landmatrix_activity AS a
%(from)s""" + "\n" \
+ join_attributes('pi_deal') + "\n" \
+ join_attributes('deal_scope') + """
%(from_filter)s
WHERE """ + "\nAND ".join([ cls.max_version_condition(), cls.status_active_condition(), cls.is_deal_condition(), cls.not_mining_condition() ]) + """
%(where)s
%(where_filter)s
%(group_by)s"""
