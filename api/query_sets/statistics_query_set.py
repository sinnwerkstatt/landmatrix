from pprint import pprint

from landmatrix.models import *
from api.query_sets.fake_query_set_with_subquery import FakeQuerySetFlat

from django.db import connection

class StatisticsQuerySet(FakeQuerySetFlat):

    DEBUG = False

    FIELDS = [
        ('negotiation_status', 'a.negotiation_status'),
        ('deals', 'COUNT(DISTINCT a.activity_identifier)'),
        ('deal_size', 'ROUND(COALESCE(SUM(a.deal_size)), 0)'),
    ]

    ADDITIONAL_JOINS = [
        "LEFT JOIN landmatrix_activityattribute         AS target_country   ON a.id = target_country.fk_activity_id AND target_country.name = 'target_country'",
        "LEFT JOIN landmatrix_country                   AS deal_country     ON CAST(target_country.value AS NUMERIC) = deal_country.id",
    ]
    GROUP_BY = [
        'negotiation_status',
    ]

    def __init__(self, request):
        super().__init__(request)
        self.country = request.GET.get('target_country')
        self.region = request.GET.get('target_region')

    def all(self):
        self._filter_sql += self.regional_condition()
        return [[r['negotiation_status'], r['deals'], r['deal_size']] for r in super().all()]

#    def all(self):
#        cursor = connection.cursor()
#        sql = """
#    SELECT
#        a.negotiation_status,
#        COUNT(DISTINCT a.activity_identifier) AS deals,
#        ROUND(COALESCE(SUM(a.deal_size)), 0) AS deal_size
#    FROM """ + Activity._meta.db_table + """ AS a
#        LEFT JOIN """ + ActivityAttribute._meta.db_table + """ AS target_country ON a.id = target_country.fk_activity_id AND target_country.name = 'target_country' 
#        LEFT JOIN """ + Country._meta.db_table + """ AS deal_country ON CAST(target_country.value AS NUMERIC) = deal_country.id
#    WHERE
#        """ + "\nAND ".join(filter(None, [
#                self.status_active_condition(),
#                self.is_public_condition(),
#                self.regional_condition(),
#                "a.negotiation_status IS NOT NULL",
#            ])) + " " + self._filter_sql + """
#    GROUP BY a.negotiation_status
#        """
#        cursor.execute(sql)
#        result = cursor.fetchall()
#        return result

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
    