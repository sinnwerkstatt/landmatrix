from django.db import connection

from api.query_sets.fake_query_set_with_subquery import FakeQuerySetWithSubquery, FakeQuerySetFlat
from landmatrix.models.activity import Activity

class StatisticsQuerySet(FakeQuerySetWithSubquery):

    DEBUG = True

    FIELDS = [
        ('negotiation_status',  'sub.negotiation_status'),
        ('deals',               'COUNT(DISTINCT a.activity_identifier)'),
        ('deal_size',           "COALESCE(ROUND(SUM(a.deal_size)), 0)")
    ]
    SUBQUERY_FIELDS = [
        ('negotiation_status',    "a.negotiation_status")
    ]
    GROUP_BY = ['sub.negotiation_status']
    ORDER_BY = ['sub.negotiation_status']

    ADDITIONAL_JOINS = [
        "LEFT JOIN landmatrix_activityattribute         AS target_country   ON a.id = target_country.fk_activity_id AND target_country.name = 'target_country'",
        "LEFT JOIN landmatrix_country                   AS deal_country     ON CAST(target_country.value AS NUMERIC) = deal_country.id",
    ]

    def __init__(self, request):
        super().__init__(request)
        self.country = request.GET.get('target_country')
        self.region = request.GET.get('target_region')

    def all(self):
        self._filter_sql += self.regional_condition()
        return [[r['negotiation_status'], r['deals'], r['deal_size']] for r in super().all()]

    def regional_condition(self):
        if self.country:
            return "AND deal_country.id = %s" % self.country
        elif self.region:
            return "AND deal_country.fk_region_id = %s" % self.region
        return ''


class PublicDealCountQuerySet(FakeQuerySetFlat):

    DEBUG = False

    def all(self):
        cursor = connection.cursor()
        sql = """
    SELECT
        COUNT(DISTINCT a.activity_identifier) AS deals
    FROM """ + Activity._meta.db_table + """ AS a
    WHERE
        """ + "\nAND ".join(filter(None, [
                self.status_active_condition(),
                self.is_public_condition(),
            ]))

        cursor.execute(sql)
        result = cursor.fetchall()
        return result

    def is_public_condition(self):
        return "a.is_public = 't'"
    