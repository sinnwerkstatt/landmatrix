__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from api.query_sets.sql_generation.sql_builder import SQLBuilder
from api.query_sets.sql_generation.join_functions import join_attributes


class ListSQLBuilder(SQLBuilder):

    GROUP_CONDITIONS = {
        "target_region":    ' AND deal_region.slug = lower(\'%s\') ',
        "target_country":   ' AND deal_country.slug = lower(\'%s\') ',
        "year":             ' AND negotiation_status.year = \'%s\' ',
        "crop":             ' AND crop.slug = lower(\'%s\') ',
        "intention":        ' AND lower(replace(intention.value, \' \', \'-\')) = lower(\'%s\') ',
        "investor_region":  ' AND investor_region.slug = \'%s\' ',
        "investor_country": ' AND investor_country.slug = \'%s\' ',
        "stakeholder_country": ' AND stakeholder_country.slug = \'%s\' ',
        "stakeholder_name": ' AND stakeholders.investor_identifier = \'%s\' ',
        "data_source_type": ' AND lower(replace(replace(data_source_type.value, \' \', \'-\'), \'/\', \'+\')) = lower(\'%s\') '
    }

    def get_where_sql(self):
        if self.group != 'all' and self.group_value:
            return self.GROUP_CONDITIONS[self.group] % self.group_value
        return ''

    def get_group_sql(self):
        group_by_sql = " GROUP BY a.id "
        additional_group_by = []
        for c in [ col for col in self.columns if not col in ["intended_size", "contract_size", "production_size", "data_source"]]:
            additional_group_by.append("sub.%(name)s" % {"name": c})
        if additional_group_by:
            group_by_sql += ', ' + ', '.join(additional_group_by)
        return group_by_sql

    def column_sql(self, c):
        if c in ("intended_size", "contract_size", "production_size"):
            return ''
        else:
            return self.SQL_COLUMN_MAP[c][0]

    def get_sub_columns_sql(self):
        sub_columns_sql = ''
        for c in self.columns:
            if c in ("intended_size", "contract_size", "production_size"):
                sub_columns_sql += "NULLIF(ARRAY_TO_STRING(ARRAY_AGG(DISTINCT %(name)s.value), ', '), '') AS %(name)s,\n" % {"name": c}
            elif c == "data_source":
                sub_columns_sql += "sub.data_source_type AS data_source_type, sub.data_source_url AS data_source_url, sub.data_source_date AS data_source_date, sub.data_source_organisation AS data_source_organisation,\n"
            else:
                sub_columns_sql += "sub.%(name)s AS %(name)s,\n" % {"name": c}
        return sub_columns_sql

    def get_base_sql(self):
        return u"""SELECT
sub.name AS name,
%(sub_columns)s
'dummy' AS dummy
FROM
landmatrix_activity AS a """ + "\n" \
+ join_attributes('intended_size') + "\n" \
+ join_attributes('contract_size') + "\n" \
+ join_attributes('production_size') + "\n" \
+ \
"""
JOIN (
    SELECT DISTINCT
    a.id AS id,
    %(name)s AS name,
    %(columns)s    'dummy' AS dummy
    FROM landmatrix_activity AS a
    %(from)s""" + "\n" + \
     join_attributes('deal_scope') + """
    %(from_filter)s
    WHERE """ + "\nAND ".join(filter(None, [
#            cls.max_version_condition(),
            self.status_active_condition(),
            self.is_public_condition(),
            self.not_mining_condition()
        ])) + """
    %(where)s
    %(where_filter)s
    GROUP BY a.id
) AS sub ON (sub.id = a.id)
%(group_by)s, sub.name
%(order_by)s
%(limit)s"""
