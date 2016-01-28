
__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from landmatrix.models import *
from api.query_sets.sql_generation.filter_to_sql import FilterToSQL
from api.query_sets.sql_generation.join_functions import *
from api.query_sets.sql_generation.sql_builder_data import SQLBuilderData


def list_view_wanted(filters):
    group = filters.get("group_by", "")
    group_value = filters.get("group_value", "")
    return group == "all" or group_value


class SQLBuilder(SQLBuilderData):

    @classmethod
    def create(cls, filters, columns):
        from .list_sql_builder import ListSQLBuilder
        from .group_sql_builder import GroupSQLBuilder

        if list_view_wanted(filters):
            return ListSQLBuilder(filters, columns)
        else:
            return GroupSQLBuilder(filters, columns)

    def __init__(self, filters, columns):
        self.filters = filters
        self.columns = columns
        self._add_order_by_columns()
        self.group = filters.get("group_by", "")
        self.group_value = filters.get("group_value", "")
        self.filter_to_sql = FilterToSQL(filters, self.columns)
        super(SQLBuilder, self).__init__()

    def _add_order_by_columns(self):
        for c in self.filters.get('order_by', []):
            if self._strip_order_sql(c) not in self.columns:
                self.columns.append(self._strip_order_sql(c))

    def get_sql(self):
        return self.get_base_sql() % {
            "from": self.get_from_sql(),
            "where": self.get_where_sql(),
            "limit": self.get_limit_sql(),
            "order_by": self.get_order_sql(),
            "from_filter": self.filter_from(),
            "where_filter": self.filter_where(),
            "group_by": self.get_group_sql(),
            "inner_group_by": self.get_inner_group_sql(),
            "name": self.get_name_sql(),
            "columns": self.get_columns_sql(),
            "sub_columns": self.get_sub_columns_sql()
        }

    def get_from_sql(self):

        self.join_expressions = []

        if self._need_involvements_and_stakeholders():
            self.join_expressions.extend([
                join_expression(InvestorActivityInvolvement, 'iai', 'a.id', 'iai.fk_activity_id'),
                join_expression(Investor, 'operational_stakeholder', 'operational_stakeholder.id', 'iai.fk_investor_id'),
                join_expression(InvestorVentureInvolvement, 'ivi', 'operational_stakeholder.id', 'ivi.fk_venture_id'),
                join_expression(Investor, 'stakeholder', 'stakeholder.id', 'ivi.fk_venture_id')
            ])

        for c in get_join_columns(self.columns, self.group, self.group_value):
            if not c == 'deal_id':
                self._add_join_for_column(c)

        return "\n".join(self.join_expressions)

    def get_name_sql(self):
        return self.GROUP_TO_NAME.get(self.group, "'%s'" % self.group)

    def get_where_sql(self):
        raise RuntimeError('SQLBuilder.get_where_sql() not implemented')

    def get_group_sql(self):
        raise RuntimeError('SQLBuilder.get_group_sql() not implemented')

    def get_inner_group_sql(self):
        return ''

    def get_columns_sql(self):
        return ",\n".join(map(lambda c: self.column_sql(c), self.columns))

    def get_sub_columns_sql(self):
        return ''

    def get_order_sql(self):
        order_by = self.filters.get('order_by')
        if not order_by: return ''

        fields = []
        for field in order_by:
            if field[0] == "-":
                field = field[1:]
                fields.append("%s %s DESC" % self._natural_sort(field))
            else:
                fields.append("%s %s ASC" % self._natural_sort(field))

        return 'ORDER BY ' + ', '.join(fields)

    def _strip_order_sql(self, order_by):
        return order_by.strip('-+0')

    def _natural_sort(self, field):
        return (field.split("+0")[0], '+0') if "+0" in field else (field, '')

    def get_limit_sql(self):
        limit = self.filters.get('limit')
        return " LIMIT %s " % limit if limit else ''

    def filter_from(self):
        return self.filter_to_sql.filter_from()

    def filter_where(self):
        return self.filter_to_sql.filter_where()

    @classmethod
    def get_base_sql(cls):
        raise RuntimeError('SQLBuilder.get_base_sql() not implemented')

    def is_aggregate_column(self, c):
        try:
            return any(x in self.SQL_COLUMN_MAP[c][0] for x in ['ARRAY_AGG', 'COUNT'])
        except KeyError:
            return False

    def _need_involvements_and_stakeholders(self):
        return self._investor_filter_is_set() or any(
            x in ("investor_country","investor_region", "investor_name", 'primary_investor', "primary_investor_name")
            for x in self.columns
        )

    def _investor_filter_is_set(self):
        return 'investor' in self.filters and 'tags' in self.filters['investor'] and self.filters['investor']['tags']

    def _add_join_for_column(self, c):
        spec = self.COLUMNS.get(c, [join_attributes(c)])
        if isinstance(spec, tuple):
            if not any(spec[0] in string for string in self.join_expressions):
                self._add_join_if_not_present(spec[1])
        else:
            self._add_join_if_not_present(spec)

    def _add_join_if_not_present(self, new_join_expressions):
        for new_join_expression in new_join_expressions:
            if new_join_expression not in self.join_expressions:
                self.join_expressions.append(new_join_expression)


    @classmethod
    def max_version_condition(cls, model=Activity, alias='a', id_field='activity_identifier'):
        return """%s.version = (
            SELECT MAX(version) FROM %s AS amax
            WHERE amax.%s = %s.%s AND amax.fk_status_id IN (%s)
        )""" % (alias, model._meta.db_table, id_field, alias, id_field, ', '.join(map(str, cls.registered_status_ids())))

    @classmethod
    def status_active_condition(cls):
        return "a.fk_status_id IN (%s)" % ', '.join(map(str, cls.valid_status_ids()))

    @classmethod
    def is_deal_condition(cls):
        return "pi.is_deal"

    @classmethod
    def not_mining_condition(cls):
        return "a.activity_identifier NOT IN (%s)" % ', '.join(map(str, cls.mining_deals()))

    miningdeals = []
    @classmethod
    def mining_deals(cls):
        if not cls.miningdeals:
            cls.miningdeals = cls.read_mining_deals()
        return cls.miningdeals

    @classmethod
    def read_mining_deals(cls):
        from django.db import connection

        sql = """SELECT DISTINCT a.activity_identifier AS deal_id
FROM landmatrix_activity                    AS a
LEFT JOIN landmatrix_publicinterfacecache   AS pi        ON a.id = pi.fk_activity_id AND pi.is_deal
LEFT JOIN landmatrix_activityattributegroup AS intention ON a.id = intention.fk_activity_id AND intention.attributes ? 'intention'
          WHERE
""" + "\nAND ".join([
#            cls.max_version_condition(),
            cls.status_active_condition(), cls.is_deal_condition()
        ]) + """
        AND intention.attributes->'intention' = 'Mining'"""

        cursor = connection.cursor()
        cursor.execute(sql)
        return ['0'] + [id for sublist in (cursor.fetchall()) for id in sublist]

    registeredstatusids = []
    @classmethod
    def registered_status_ids(cls):
        if not cls.registeredstatusids:
            cls.registeredstatusids = Status.objects.filter(name__in=['active', 'overwritten', 'deleted']).values_list('id', flat=True)
        return cls.registeredstatusids

    validstatusids = []
    @classmethod
    def valid_status_ids(cls):
        if not cls.validstatusids:
            cls.validstatusids = Status.objects.filter(name__in=['active', 'overwritten']).values_list('id', flat=True)
        return cls.validstatusids
