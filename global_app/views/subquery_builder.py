__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from .sql_builder import join_attributes
from .list_sql_builder import ListSQLBuilder

from landmatrix.models import Status

class SubqueryBuilder(ListSQLBuilder):

    def column_sql(self, c):
        if c in ("intended_size", "contract_size", "production_size"):
            return "NULLIF(ARRAY_TO_STRING(ARRAY_AGG(DISTINCT %(name)s.attributes->'%(name)s'), ', '), '') AS %(name)s,\n" % {"name": c}
        elif c == "data_source":
            return "                " + self.SQL_COLUMN_MAP.get(c)[0]

        try:
            return "                " + self.SQL_COLUMN_MAP.get(c)[0]
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
        return 'ARRAY_AGG' in self.SQL_COLUMN_MAP[c][0]

    @classmethod
    def get_base_sql(cls):
        return u"""SELECT DISTINCT
            a.activity_identifier,
%(columns)s              a.id AS id
FROM landmatrix_activity AS a
%(from)s""" + "\n" \
+ join_attributes('pi_deal') + "\n" \
+ join_attributes('deal_scope') + """
%(from_filter)s
WHERE """ + "\nAND ".join([ cls.max_version_condition(), cls.status_active_condition(), cls.is_deal_condition(), cls.not_mining_condition() ]) + """
              %(where)s
              %(where_filter)s
%(group_by)s"""

    @classmethod
    def max_version_condition(cls):
        return """a.version = (
            SELECT max(version) FROM landmatrix_activity amax
            WHERE amax.activity_identifier = a.activity_identifier AND amax.fk_status_id IN (%s)
        )""" % ', '.join(map(str, cls.registered_status_ids()))

    @classmethod
    def status_active_condition(cls):
        return "a.fk_status_id IN (%s)" % ', '.join(map(str, cls.valid_status_ids()))

    @classmethod
    def is_deal_condition(cls):
        return "pi_deal.attributes->'pi_deal' = 'True'"

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
FROM
landmatrix_activity AS a
              JOIN landmatrix_status ON (landmatrix_status.id = a.fk_status_id)
LEFT JOIN landmatrix_activityattributegroup    AS pi_deal               ON a.id = pi_deal.fk_activity_id AND pi_deal.attributes ? 'pi_deal' AND NOT (pi_deal.attributes->'pi_deal') IS NULL
LEFT JOIN landmatrix_activityattributegroup    AS intention             ON a.id = intention.fk_activity_id AND intention.attributes ? 'intention' AND NOT (intention.attributes->'intention') IS NULL
          WHERE
""" + "\nAND ".join([ cls.max_version_condition(), cls.status_active_condition(), cls.is_deal_condition() ]) + """
        AND intention.attributes->'intention' = 'Mining'"""

        cursor = connection.cursor()
        cursor.execute(sql)
        res = cursor.fetchall()
        # print('excluded deals:', res)
        # print('excluded deals SQL:\n', sql)
        return ['0'] + [id for sublist in res for id in sublist]

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
