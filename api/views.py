
__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from landmatrix.models import *
from django.db import models
from django.db import connection
from django.conf import settings


class StatisticsManager(models.Manager):

    def all(self):
        BASE_JOIN = """LEFT JOIN """ + Status._meta.db_table + """ AS status ON status.id = a.fk_status_id
    LEFT JOIN """ + Involvement._meta.db_table + """ AS i ON i.fk_activity_id = a.id
    LEFT JOIN """ + Stakeholder._meta.db_table + """ AS s ON i.fk_stakeholder_id = s.id
    LEFT JOIN """ + PrimaryInvestor._meta.db_table + """ AS pi ON i.fk_primary_investor_id = pi.id
    LEFT JOIN """ + Status._meta.db_table + """ AS pi_st ON pi.fk_status_id = pi_st.id
    LEFT JOIN """ + StakeholderAttributeGroup._meta.db_table + """ AS stakeholder_attrs ON s.id = stakeholder_attrs.fk_stakeholder_id
    LEFT JOIN """ + ActivityAttributeGroup._meta.db_table + """ AS activity_attrs ON a.id = activity_attrs.fk_activity_id
    LEFT JOIN  """ + Country._meta.db_table + """ AS investor_country ON stakeholder_attrs.attributes->'country' = investor_country.name
    LEFT JOIN  """ + Region._meta.db_table + """ AS investor_region ON investor_country.fk_region_id = investor_region.id
    LEFT JOIN """ + Country._meta.db_table + """ AS deal_country ON activity_attrs.attributes->'target_country' = deal_country.name
    LEFT JOIN """ + Region._meta.db_table + """ AS deal_region ON deal_country.fk_region_id = deal_region.id"""

        HECTARES_SQL = "ROUND(COALESCE(SUM(CAST(REPLACE(activity_attrs.attributes->'pi_deal_size', ',', '.') AS numeric)), 0)) AS deal_size"

        BASE_CONDITON = """a.version = (
        SELECT MAX(version)
        FROM """ + Activity._meta.db_table + """ AS amax, """ + Status._meta.db_table + """ AS st
        WHERE amax.fk_status_id = st.id AND amax.activity_identifier = a.activity_identifier
            AND st.name IN ('active', 'overwritten', 'deleted')
    )
    AND pi.version = (
        SELECT MAX(version)
        FROM """ + PrimaryInvestor._meta.db_table + """ AS pimax, """ + Status._meta.db_table + """ AS st
        WHERE pimax.fk_status_id = st.id AND pimax.primary_investor_identifier = pi.primary_investor_identifier
            AND st.name IN ('active', 'overwritten', 'deleted')
    )
    AND status.name IN ('active', 'overwritten') AND pi_st.name IN ('active', 'overwritten')
    AND activity_attrs.attributes->'pi_deal' = 'True'"""

        cursor = connection.cursor()
        sql = """SELECT
    sub.negotiation_status,
    COUNT(DISTINCT a.activity_identifier) AS deals,
    """ + HECTARES_SQL + """,
    MIN(sub.negotiation_status_date) AS year
FROM """ + Activity._meta.db_table + """ AS a
LEFT JOIN """ + ActivityAttributeGroup._meta.db_table + """ AS activity_attrs ON a.id = activity_attrs.fk_activity_id,
(
    SELECT DISTINCT
        a.id,
        activity_attrs.attributes->'pi_negotiation_status' AS negotiation_status,
        activity_attrs.date AS negotiation_status_date
    FROM """ + Activity._meta.db_table + """ AS a
    """ + BASE_JOIN + """
    WHERE """ + BASE_CONDITON + """
) AS sub
WHERE a.id = sub.id
GROUP BY sub.negotiation_status"""
        cursor.execute(sql)
        result = cursor.fetchall()
        if settings.DEBUG and connection.queries: print(connection.queries[-1]['sql'])
        return result


from django.http import HttpResponse
from django.views.generic.base import TemplateView
import json


class JSONView(TemplateView):
    template_name = "plugins/overview.html"

    FAKE_VALUES = {
        'negotiation_status': [
            {"deals": 71, "hectares": 1814686.0, "name": "Concluded (Oral Agreement)"},
            {"deals": 978, "hectares": 36619575.0, "name": "Concluded (Contract signed)"},
            {"deals": 0, "hectares": 0, "name": "Intended (Expression of interest)"},
            {"deals": 0, "hectares": 0, "name": "Intended (Under negotiation)"},
            {"deals": 0, "hectares": 0, "name": "Failed (Negotiations failed)"},
            {"deals": 0, "hectares": 0, "name": "Failed (Contract canceled)"},
            {"deals": 0, "hectares": 0, "name": ""}
        ],
        'implementation_status': [
            {"deals": 112, "hectares": 8867937.0, "name": "Project not started"},
            {"deals": 145, "hectares": 3347947.0, "name": "Startup phase (no production)"},
            {"deals": 604, "hectares": 17474652.0, "name": "In operation (production)"},
            {"deals": 59, "hectares": 3966570.0, "name": "Project abandoned"},
            {"deals": 500, "hectares": 28122741.0, "name": ""}
        ],
        'intention_of_investment': [
            {"deals": 790, "hectares": 18192014.0, "name": "Agriculture"},
            {"deals": 101, "hectares": 9429665.0, "name": "Forestry"},
            {"deals": 10, "hectares": 528501.0, "name": "Tourism"},
            {"deals": 9, "hectares": 24003.0, "name": "Industry"},
            {"deals": 2, "hectares": 46100.0, "name": "Conservation"},
            {"deals": 7, "hectares": 278280.0, "name": "Renewable Energy"},
            {"deals": 7, "hectares": 33280.0, "name": "Other"},
            {"deals": 116, "hectares": 9755468.0, "name": "Multiple intention"},
            {"deals": 7, "hectares": 146950.0, "name": ""}
        ],
    }

    def dispatch(self, request, *args, **kwargs):
        if kwargs.get('type').endswith('.json'):
            return HttpResponse(json.dumps(self.FAKE_VALUES[kwargs['type'][:-5]]))

def stats(*args, **kwargs):
    return HttpResponse('woo hoo: <br/>'+str(kwargs) )