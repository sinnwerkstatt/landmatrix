__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django.conf import settings


def join_attributes(table_alias, attribute, attribute_table='landmatrix_activityattributegroup', attribute_field='fk_activity_id'):
    from string import Template
    template = Template("""
          LEFT JOIN $table AS $alias ON (a.id = $alias.$field AND $alias.attributes ? '$attr')"""
    )
    return template.substitute(alias=table_alias, attr=attribute, table=attribute_table, field=attribute_field)

class SQLBuilder:
    def __init__(self, columns, group):
        self.columns = columns
        self.group = group

    @classmethod
    def get_base_sql(cls):
        raise RuntimeError('SQLBuilder.get_base_sql() not implemented')

class ListSQLBuilder(SQLBuilder):

    def __init__(self, columns, group, group_value):
        super(ListSQLBuilder, self).__init__(columns, group)
        self.group_value = group_value

    def get_group_sql(self):
        group_by_sql = " GROUP BY a.id "
        additional_group_by = []
        for c in [ col for col in self.columns if not col in ["intended_size", "contract_size", "production_size", "data_source"]]:
            additional_group_by.append("sub.%(name)s" % {"name": c})
        if (settings.DEBUG): print('addnl group by:', additional_group_by)
        if additional_group_by: group_by_sql += ', ' + ', '.join(additional_group_by)

        return group_by_sql

    @classmethod
    def get_base_sql(cls):
        return u"""
        SELECT
            sub.name as name,
%(sub_columns)s            'dummy' as dummy
          FROM
            landmatrix_activity AS a""" \
            + join_attributes('size', 'pi_deal_size') \
            + join_attributes('intended_size', 'intended_size') \
            + join_attributes('contract_size', 'contract_size') \
            + join_attributes('production_size', 'production_size') \
            + \
        """
          JOIN (
            SELECT DISTINCT
              a.id as id,
              %(name)s as name,
%(columns)s                'dummy' as dummy
            FROM
              landmatrix_activity a
            JOIN landmatrix_status ON (landmatrix_status.id = a.fk_status_id)
              %(from)s""" \
            + join_attributes('pi_deal', 'pi_deal') \
            + join_attributes('deal_scope', 'deal_scope') \
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

class GroupSQLBuilder(SQLBuilder):

    def __init__(self, columns, group, filter):
        super(GroupSQLBuilder, self).__init__(columns, group)
        self.filter = filter

    def get_group_sql(self):
        if self.group:  return "GROUP BY %s" % self.group
        else:           return 'GROUP BY dummy'

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
