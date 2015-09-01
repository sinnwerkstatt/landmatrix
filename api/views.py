__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from landmatrix.models import *
from global_app.views.sql_generation.sql_builder import SQLBuilder
from api.query_sets.negotiation_status_query_set import NegotiationStatusQuerySet

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
import decimal


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)


class ProtocolAPI:

    HECTARES_SQL = """ROUND(SUM(CAST(REPLACE(size.attributes->'pi_deal_size', ',', '.') AS NUMERIC))) as deal_size"""

    BASE_JOIN = """
    JOIN      landmatrix_status                                        ON (landmatrix_status.id = a.fk_status_id)
    LEFT JOIN landmatrix_involvement               AS i                ON i.fk_activity_id = a.id
    LEFT JOIN landmatrix_stakeholder               AS s                ON i.fk_stakeholder_id = s.id
    LEFT JOIN landmatrix_primaryinvestor           AS pi               ON i.fk_primary_investor_id = pi.id
    LEFT JOIN landmatrix_status                    AS pi_st            ON pi.fk_status_id = pi_st.id
    LEFT JOIN landmatrix_stakeholderattributegroup AS skvf1            ON s.id = skvf1.fk_stakeholder_id AND skvf1.attributes ? 'country'
    LEFT JOIN landmatrix_country                   AS investor_country ON CAST(skvf1.attributes->'country' AS NUMERIC) = investor_country.id
    LEFT JOIN landmatrix_region                    AS investor_region  ON investor_country.fk_region_id = investor_region.id
    LEFT JOIN landmatrix_activityattributegroup    AS intention        ON a.id = intention.fk_activity_id AND intention.attributes ? 'intention'
    LEFT JOIN landmatrix_activityattributegroup    AS target_country   ON a.id = target_country.fk_activity_id AND target_country.attributes ? 'target_country'
    LEFT JOIN landmatrix_country                   AS deal_country     ON CAST(target_country.attributes->'target_country' AS NUMERIC) = deal_country.id
    LEFT JOIN landmatrix_region                    AS deal_region      ON  deal_country.fk_region_id = deal_region.id
    LEFT JOIN landmatrix_activityattributegroup    AS negotiation      ON a.id = negotiation.fk_activity_id AND negotiation.attributes ? 'pi_negotiation_status'
    LEFT JOIN landmatrix_activityattributegroup    AS implementation   ON a.id = implementation.fk_activity_id AND implementation.attributes ? 'pi_implementation_status'
    LEFT JOIN landmatrix_activityattributegroup    AS bf               ON a.id = bf.fk_activity_id AND bf.attributes ? 'pi_deal'
    LEFT JOIN landmatrix_activityattributegroup    AS size             ON a.id = size.fk_activity_id AND size.attributes ? 'pi_deal_size'
    LEFT JOIN landmatrix_activityattributegroup    AS deal_scope       ON a.id = deal_scope.fk_activity_id AND deal_scope.attributes ? 'deal_scope'
    """

    BASE_CONDITON = ' AND '.join([
        SQLBuilder.max_version_condition(), SQLBuilder.status_active_condition(), "bf.attributes->'pi_deal' = 'True'",
        SQLBuilder.max_version_condition(PrimaryInvestor, 'pi', 'primary_investor_identifier')
    ]) + """
        AND pi_st.name IN ('active', 'overwritten')
    """

    BASE_FILTER_MAP = {
        "concluded": ("concluded (oral agreement)", "concluded (contract signed)"),
        "intended": ("intended (expression of interest)", "intended (under negotiation)" ),
        "failed": ("failed (contract canceled)", "failed (negotiations failed)"),
    }

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


class JSONView(TemplateView, ProtocolAPI):
    template_name = "plugins/overview.html"

    def dispatch(self, request, *args, **kwargs):
        if kwargs.get('type') == 'negotiation_status.json':
            try:
                with_names = list(self.get_negotiation_status(request))
                return HttpResponse(json.dumps(with_names, cls=DecimalEncoder))
            except Exception as e:
                print(e)
                raise e
        elif kwargs.get('type').endswith('.json'):
            return HttpResponse(json.dumps(self.FAKE_VALUES[kwargs['type'][:-5]]))
        raise ValueError('Could not dispatch: ' + str(kwargs))

    def get_negotiation_status(self, request):

        filter_sql = self._get_filter(request.GET.getlist("negotiation_status", []), request.GET.getlist("deal_scope", []), request.GET.get("data_source_type"))
        another_queryset = NegotiationStatusQuerySet()
        another_queryset.set_filter_sql(filter_sql)
        return another_queryset.all()

    def _get_filter(self, negotiation_status, deal_scope, data_source_type):
        filter_sql = ""
        if len(deal_scope) == 0:
            # when no negotiation stati or deal scope given no deals should be shown at the public interface
            return " AND 1 <> 1 "
        if negotiation_status:
            stati = []
            for n in negotiation_status:
                stati.extend(self.BASE_FILTER_MAP.get(n))
            filter_sql += " AND lower(negotiation.attributes->'pi_negotiation_status') in ('%s') " % "', '".join(stati)
        if len(deal_scope) == 1:
            filter_sql += " AND deal_scope.attributes->'deal_scope' = '%s' " % deal_scope[0]
        if data_source_type:
            filter_sql += " AND 'Media report' <> ( SELECT GROUP_CONCAT(data_source_type.value) FROM a_key_value_lookup data_source_type WHERE a.activity_identifier = data_source_type.activity_identifier AND data_source_type.key = 'type')"
        return filter_sql
