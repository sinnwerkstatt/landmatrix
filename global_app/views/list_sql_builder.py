__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from .sql_builder import SQLBuilder, join_attributes

class ListSQLBuilder(SQLBuilder):

    GROUP_CONDITIONS = {
        "target_region":    ' AND deal_region.slug = lower(\'%s\') ',
        "target_country":   ' AND deal_country.slug = lower(\'%s\') ',
        "year":             ' AND pi_negotiation_status.year = \'%s\' ',
        "crop":             ' AND crop.slug = lower(\'%s\') ',
        "intention":        ' AND lower(replace(intention.value, \' \', \'-\')) = lower(\'%s\') ',
        "investor_region":  ' AND investor_region.slug = \'%s\' ',
        "investor_country": ' AND investor_country.slug = \'%s\' ',
        "investor_name":    ' AND s.stakeholder_identifier = \'%s\' ',
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
        if additional_group_by: group_by_sql += ', ' + ', '.join(additional_group_by)

        return group_by_sql

    def column_sql(self, c):
        if c in ("intended_size", "contract_size", "production_size"):
            return ''
        elif c == "data_source":
            return "                " + self.SQL_COLUMN_MAP.get(c)[0]

        return "                " + self.SQL_COLUMN_MAP.get(c)[0]

    def get_sub_columns_sql(self):
        sub_columns_sql = ''
        for c in self.columns:
            if c in ("intended_size", "contract_size", "production_size"):
                sub_columns_sql += "            ARRAY_AGG(%(name)s.attributes->'%(name)s' ORDER BY %(name)s.date DESC) as %(name)s,\n" % {"name": c}
            elif c == "data_source":
                sub_columns_sql += "            sub.data_source_type as data_source_type, sub.data_source_url as data_source_url, sub.data_source_date data_source_date, sub.data_source_organisation as data_source_organisation,\n"
            else:
                sub_columns_sql += "            sub.%(name)s as %(name)s,\n" % {"name": c}
        return sub_columns_sql

    @classmethod
    def get_base_sql(cls):
        return u"""
        SELECT
              sub.name as name,
%(sub_columns)s
              'dummy' as dummy
          FROM
              landmatrix_activity AS a """ + "\n" \
              + join_attributes('size', 'pi_deal_size') + "\n" \
              + join_attributes('intended_size') + "\n" \
              + join_attributes('contract_size') + "\n" \
              + join_attributes('production_size') + "\n" \
              + \
          """
          JOIN (
              SELECT DISTINCT
                  a.id as id,
                  %(name)s as name,
%(columns)s
                  'dummy' as dummy
              FROM
                  landmatrix_activity AS a
                  JOIN landmatrix_status ON (landmatrix_status.id = a.fk_status_id)
                  %(from)s""" + "\n" \
                  + join_attributes('pi_deal') + "\n" \
                  + join_attributes('deal_scope') + "\n" \
                  + """
                  %(from_filter_activity)s
                  %(from_filter_investor)s
              WHERE
                  a.version = (
                      SELECT max(version)
                      FROM landmatrix_activity amax, landmatrix_status st
                      WHERE amax.fk_status_id = st.id
                          AND amax.activity_identifier = a.activity_identifier
                          AND st.name IN ('active', 'overwritten', 'deleted')
                  )
                  AND landmatrix_status.name in ('active', 'overwritten')
                  AND pi_deal.attributes->'pi_deal' = 'True'
                  AND (NOT DEFINED(intention.attributes, 'intention') OR intention.attributes->'intention' != 'Mining')
                  %(where)s
                  %(where_filter_investor)s
                  %(where_filter_activity)s
              GROUP BY a.id
          ) AS sub ON (sub.id = a.id)
          %(group_by)s, sub.name
          %(order_by)s
          %(limit)s;
    """

