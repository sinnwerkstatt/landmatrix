__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from .sql_builder import SQLBuilder

class GroupSQLBuilder(SQLBuilder):

    def get_where_sql(self):
        if not self.filters.get("starts_with", None): return ''

        starts_with = self.filters.get("starts_with", "").lower()
        if self.group == "investor_country":
            return " AND investor_country.slug like '%s%%%%' " % starts_with
        elif self.group == "target_country":
            return " AND deal_country.slug like '%s%%%%' " % starts_with
        return " AND trim(lower(%s.value)) like '%s%%%%' " % (self.group, starts_with)

    def get_group_sql(self):
        if self.group:  return "GROUP BY %s" % self.group
        else:           return 'GROUP BY dummy'

    def get_inner_group_sql(self):
        # query deals grouped by a key
        return ", %s" % self.group

    def column_sql(self, c):
        if c == self.group:
            # use single values for column which gets grouped by
            return self.SQL_COLUMN_MAP.get(c)[1]
        return self.SQL_COLUMN_MAP.get(c)[0]

    @classmethod
    def get_base_sql(cls):
        return u"""
        SELECT DISTINCT
              %(name)s as name,
              %(columns)s
              'dummy' as dummy
        FROM
            landmatrix_activity AS a
        JOIN landmatrix_status ON (landmatrix_status.id = a.fk_status_id)
            %(from)s
        LEFT JOIN landmatrix_activityattributegroup AS pi_deal
            ON (a.id = pi_deal.fk_activity_id AND LENGTH(pi_deal.attributes->'pi_deal') > 0)
        LEFT JOIN landmatrix_activityattributegroup AS deal_scope
            ON (a.id = deal_scope.fk_activity_id AND LENGTH(deal_scope.attributes->'deal_scope') > 0)
        %(from_filter_activity)s
        %(from_filter_investor)s
        WHERE
            a.version = (
                SELECT max(version) FROM landmatrix_activity amax, landmatrix_status st
                WHERE amax.fk_status_id = st.id
                  AND amax.activity_identifier = a.activity_identifier
                  AND st.name IN ('active', 'overwritten', 'deleted')
            )
            AND landmatrix_status.name in ('active', 'overwritten')
            AND pi_deal.attributes->'pi_deal' = 'True'
            AND (pi_deal.attributes->'intention' != 'Mining')
            %(where)s
            %(where_filter_investor)s
            %(where_filter_activity)s
         %(group_by)s
         %(order_by)s
         %(limit)s;
    """
