from pprint import pprint

from landmatrix.models import *
from api.query_sets.fake_query_set_with_subquery import FakeQuerySetFlat

from django.db import connection


__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


BASE_JOIN = """LEFT JOIN """ + Status._meta.db_table + """ AS status ON status.id = a.fk_status_id
    LEFT JOIN """ + InvestorActivityInvolvement._meta.db_table + """ AS iai ON iai.fk_activity_id = a.id
    LEFT JOIN """ + Investor._meta.db_table + """ AS os ON iai.fk_investor_id = os.id
    LEFT JOIN """ + InvestorVentureInvolvement._meta.db_table + """ AS ivi ON ivi.fk_venture_id = os.id
    LEFT JOIN """ + Investor._meta.db_table + """ AS s ON ivi.fk_investor_id = s.id
    LEFT JOIN """ + Status._meta.db_table + """ AS os_st ON os.fk_status_id = os_st.id
    LEFT JOIN """ + ActivityAttribute._meta.db_table + """ AS target_country ON a.id = target_country.fk_activity_id AND target_country.name = 'target_country' 
    LEFT JOIN """ + Country._meta.db_table + """ AS deal_country ON CAST(target_country.value AS NUMERIC) = deal_country.id
    LEFT JOIN """ + Region._meta.db_table + """ AS deal_region ON deal_country.fk_region_id = deal_region.id
    LEFT JOIN """ + PublicInterfaceCache._meta.db_table + """ AS pi ON a.id = pi.fk_activity_id AND pi.is_public"""
HECTARES_SQL = "ROUND(COALESCE(SUM(sub.deal_size)), 0) AS deal_size"
BASE_CONDITION = "status.name IN ('active', 'overwritten') AND os_st.name IN ('active', 'overwritten')"


class StatisticsQuerySet(FakeQuerySetFlat):

    DEBUG = False

    def __init__(self, request):
        super().__init__(request)
        self.country = request.GET.get('target_country')
        self.region = request.GET.get('target_region')

    def all(self):
        cursor = connection.cursor()
        sql = """SELECT
    sub.negotiation_status,
    COUNT(DISTINCT a.activity_identifier) AS deals,
    """ + HECTARES_SQL + """
FROM """ + Activity._meta.db_table + """ AS a
LEFT JOIN """ + ActivityAttribute._meta.db_table + """ AS activity_attrs ON a.id = activity_attrs.fk_activity_id,
(
    SELECT DISTINCT
        a.id,
        pi.negotiation_status AS negotiation_status,
        pi.deal_size AS deal_size
    FROM """ + Activity._meta.db_table + """ AS a
    """ + BASE_JOIN + """
    WHERE """ + BASE_CONDITION + ' ' + self.regional_condition() + """
    AND pi.negotiation_status IS NOT NULL
    GROUP BY a.activity_identifier, a.id, pi.negotiation_status, pi.deal_size
) AS sub
WHERE a.id = sub.id
GROUP BY sub.negotiation_status"""

        if self.DEBUG: print(sql)
        cursor.execute(sql)
        result = cursor.fetchall()
        if self.DEBUG: pprint(result)
        return result

    def regional_condition(self):
        if self.country:
            return """
    AND target_country.value = '%s'
            """ % self.country
        elif self.region:
            return """
    AND deal_country.fk_region_id = %s
            """ % self.region
        return ''