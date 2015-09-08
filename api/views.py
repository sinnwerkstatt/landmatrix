__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from global_app.views.sql_generation.sql_builder import SQLBuilder
from api.query_sets.negotiation_status_query_set import NegotiationStatusQuerySet
from landmatrix.models import *

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

list_of_urls = """
/en/api/negotiation_status.json?deal_scope=domestic
/en/api/negotiation_status.json?deal_scope=transnational
/en/api/negotiation_status.json?deal_scope=transnational&deal_scope=domestic
/en/api/negotiation_status.json?deal_scope=domestic&data_source_type=1
/en/api/negotiation_status.json?deal_scope=transnational&data_source_type=1
/en/api/negotiation_status.json?deal_scope=transnational&deal_scope=domestic&data_source_type=1

/en/api/implementation_status.json?deal_scope=domestic
/en/api/implementation_status.json?deal_scope=transnational
/en/api/implementation_status.json?deal_scope=transnational&deal_scope=domestic
/en/api/implementation_status.json?deal_scope=domestic&data_source_type=1
/en/api/implementation_status.json?deal_scope=transnational&data_source_type=1
/en/api/implementation_status.json?deal_scope=transnational&deal_scope=domestic&data_source_type=1

/en/api/intention_of_investment.json?negotiation_status=concluded&deal_scope=transnational
/en/api/intention_of_investment.json?negotiation_status=intended&deal_scope=transnational
/en/api/intention_of_investment.json?negotiation_status=concluded&negotiation_status=intended&deal_scope=transnational
/en/api/intention_of_investment.json?negotiation_status=failed&deal_scope=transnational
/en/api/intention_of_investment.json?negotiation_status=concluded&deal_scope=domestic
/en/api/intention_of_investment.json?negotiation_status=intended&deal_scope=domestic
/en/api/intention_of_investment.json?negotiation_status=concluded&negotiation_status=intended&deal_scope=domestic
/en/api/intention_of_investment.json?negotiation_status=failed&deal_scope=domestic
/en/api/intention_of_investment.json?negotiation_status=concluded&deal_scope=transnational&deal_scope=domestic
/en/api/intention_of_investment.json?negotiation_status=intended&deal_scope=transnational&deal_scope=domestic
/en/api/intention_of_investment.json?negotiation_status=concluded&negotiation_status=intended&deal_scope=transnational&deal_scope=domestic
/en/api/intention_of_investment.json?negotiation_status=failed&deal_scope=transnational&deal_scope=domestic
/en/api/intention_of_investment.json?negotiation_status=concluded&deal_scope=transnational&data_source_type=1
/en/api/intention_of_investment.json?negotiation_status=intended&deal_scope=transnational&data_source_type=1
/en/api/intention_of_investment.json?negotiation_status=concluded&negotiation_status=intended&deal_scope=transnational&data_source_type=1
/en/api/intention_of_investment.json?negotiation_status=failed&deal_scope=transnational&data_source_type=1
/en/api/intention_of_investment.json?negotiation_status=concluded&deal_scope=domestic&data_source_type=1
/en/api/intention_of_investment.json?negotiation_status=intended&deal_scope=domestic&data_source_type=1
/en/api/intention_of_investment.json?negotiation_status=concluded&negotiation_status=intended&deal_scope=domestic&data_source_type=1
/en/api/intention_of_investment.json?negotiation_status=failed&deal_scope=domestic&data_source_type=1
/en/api/intention_of_investment.json?negotiation_status=concluded&deal_scope=transnational&deal_scope=domestic&data_source_type=1
/en/api/intention_of_investment.json?negotiation_status=intended&deal_scope=transnational&deal_scope=domestic&data_source_type=1
/en/api/intention_of_investment.json?negotiation_status=concluded&negotiation_status=intended&deal_scope=transnational&deal_scope=domestic&data_source_type=1
/en/api/intention_of_investment.json?negotiation_status=failed&deal_scope=transnational&deal_scope=domestic&data_source_type=1

/en/api/intention_of_investment.json?deal_scope=domestic&intention=agriculture
/en/api/intention_of_investment.json?deal_scope=transnational&intention=agriculture
/en/api/intention_of_investment.json?deal_scope=domestic&deal_scope=transnational&intention=agriculture
/en/api/intention_of_investment.json?deal_scope=domestic&intention=agriculture&data_source_type=1
/en/api/intention_of_investment.json?deal_scope=transnational&intention=agriculture&data_source_type=1
/en/api/intention_of_investment.json?deal_scope=domestic&deal_scope=transnational&intention=agriculture&data_source_type=1

/en/api/transnational_deals.json?negotiation_status=concluded&deal_scope=transnational
/en/api/transnational_deals.json?negotiation_status=intended&deal_scope=transnational
/en/api/transnational_deals.json?negotiation_status=concluded&negotiation_status=intended&deal_scope=transnational
/en/api/transnational_deals.json?negotiation_status=failed&deal_scope=transnational
/en/api/transnational_deals.json?negotiation_status=concluded&deal_scope=transnational&data_source_type=1
/en/api/transnational_deals.json?negotiation_status=intended&deal_scope=transnational&data_source_type=1
/en/api/transnational_deals.json?negotiation_status=concluded&negotiation_status=intended&deal_scope=transnational&data_source_type=1
/en/api/transnational_deals.json?negotiation_status=failed&deal_scope=transnational&data_source_type=1
/en/api/top-10-countries.json?negotiation_status=concluded&deal_scope=transnational
/en/api/top-10-countries.json?negotiation_status=intended&deal_scope=transnational
/en/api/top-10-countries.json?negotiation_status=concluded&negotiation_status=intended&deal_scope=transnational
/en/api/top-10-countries.json?negotiation_status=failed&deal_scope=transnational
/en/api/top-10-countries.json?negotiation_status=concluded&deal_scope=transnational&data_source_type=1
/en/api/top-10-countries.json?negotiation_status=intended&deal_scope=transnational&data_source_type=1
/en/api/top-10-countries.json?negotiation_status=concluded&negotiation_status=intended&deal_scope=transnational&data_source_type=1
/en/api/top-10-countries.json?negotiation_status=failed&deal_scope=transnational&data_source_type=1

/en/api/investor_country_summaries.json?negotiation_status=intended&deal_scope=transnational&deal_scope=domestic
/en/api/investor_country_summaries.json?negotiation_status=concluded&deal_scope=transnational&deal_scope=domestic
/en/api/investor_country_summaries.json?negotiation_status=concluded&negotiation_status=intended&deal_scope=transnational&deal_scope=domestic
/en/api/investor_country_summaries.json?negotiation_status=failed&deal_scope=transnational&deal_scope=domestic
/en/api/investor_country_summaries.json?negotiation_status=intended&deal_scope=transnational&deal_scope=domestic&data_source_type=1
/en/api/investor_country_summaries.json?negotiation_status=concluded&deal_scope=transnational&deal_scope=domestic&data_source_type=1
/en/api/investor_country_summaries.json?negotiation_status=concluded&negotiation_status=intended&deal_scope=transnational&deal_scope=domestic&data_source_type=1
/en/api/investor_country_summaries.json?negotiation_status=failed&deal_scope=transnational&deal_scope=domestic&data_source_type=1

/en/api/target_country_summaries.json?negotiation_status=intended&deal_scope=transnational&deal_scope=domestic
/en/api/target_country_summaries.json?negotiation_status=concluded&deal_scope=transnational&deal_scope=domestic
/en/api/target_country_summaries.json?negotiation_status=concluded&negotiation_status=intended&deal_scope=transnational&deal_scope=domestic
/en/api/target_country_summaries.json?negotiation_status=failed&deal_scope=transnational&deal_scope=domestic
/en/api/target_country_summaries.json?negotiation_status=intended&deal_scope=transnational&deal_scope=domestic&data_source_type=1
/en/api/target_country_summaries.json?negotiation_status=concluded&deal_scope=transnational&deal_scope=domestic&data_source_type=1
/en/api/target_country_summaries.json?negotiation_status=concluded&negotiation_status=intended&deal_scope=transnational&deal_scope=domestic&data_source_type=1
/en/api/target_country_summaries.json?negotiation_status=failed&deal_scope=transnational&deal_scope=domestic&data_source_type=1

/en/api/agricultural-produce.json?negotiation_status=intended&deal_scope=domestic
/en/api/agricultural-produce.json?negotiation_status=intended&deal_scope=transnational
/en/api/agricultural-produce.json?negotiation_status=intended&deal_scope=domestic&deal_scope=transnational
/en/api/agricultural-produce.json?negotiation_status=concluded&deal_scope=domestic
/en/api/agricultural-produce.json?negotiation_status=concluded&deal_scope=transnational
/en/api/agricultural-produce.json?negotiation_status=concluded&deal_scope=domestic&deal_scope=transnational
/en/api/agricultural-produce.json?negotiation_status=intended&negotiation_status=concluded&deal_scope=domestic
/en/api/agricultural-produce.json?negotiation_status=intended&negotiation_status=concluded&deal_scope=transnational
/en/api/agricultural-produce.json?negotiation_status=intended&negotiation_status=concluded&deal_scope=domestic&deal_scope=transnational
/en/api/agricultural-produce.json?negotiation_status=failed&deal_scope=domestic
/en/api/agricultural-produce.json?negotiation_status=failed&deal_scope=transnational
/en/api/agricultural-produce.json?negotiation_status=failed&deal_scope=domestic&deal_scope=transnational
/en/api/agricultural-produce.json?negotiation_status=intended&deal_scope=domestic&data_source_type=1
/en/api/agricultural-produce.json?negotiation_status=intended&deal_scope=transnational&data_source_type=1
/en/api/agricultural-produce.json?negotiation_status=intended&deal_scope=domestic&deal_scope=transnational&data_source_type=1
/en/api/agricultural-produce.json?negotiation_status=concluded&deal_scope=domestic&data_source_type=1
/en/api/agricultural-produce.json?negotiation_status=concluded&deal_scope=transnational&data_source_type=1
/en/api/agricultural-produce.json?negotiation_status=concluded&deal_scope=domestic&deal_scope=transnational&data_source_type=1
/en/api/agricultural-produce.json?negotiation_status=intended&negotiation_status=concluded&deal_scope=domestic&data_source_type=1
/en/api/agricultural-produce.json?negotiation_status=intended&negotiation_status=concluded&deal_scope=transnational&data_source_type=1
/en/api/agricultural-produce.json?negotiation_status=intended&negotiation_status=concluded&deal_scope=domestic&deal_scope=transnational&data_source_type=1
/en/api/agricultural-produce.json?negotiation_status=failed&deal_scope=domestic&data_source_type=1
/en/api/agricultural-produce.json?negotiation_status=failed&deal_scope=transnational&data_source_type=1
/en/api/agricultural-produce.json?negotiation_status=failed&deal_scope=domestic&deal_scope=transnational&data_source_type=1

/en/api/hectares.json?negotiation_status=intended&deal_scope=domestic
/en/api/hectares.json?negotiation_status=intended&deal_scope=transnational
/en/api/hectares.json?negotiation_status=intended&deal_scope=transnational&deal_scope=domestic
/en/api/hectares.json?negotiation_status=concluded&deal_scope=domestic
/en/api/hectares.json?negotiation_status=concluded&deal_scope=transnational
/en/api/hectares.json?negotiation_status=concluded&deal_scope=transnational&deal_scope=domestic
/en/api/hectares.json?negotiation_status=concluded&negotiation_status=intended&deal_scope=domestic
/en/api/hectares.json?negotiation_status=concluded&negotiation_status=intended&deal_scope=transnational
/en/api/hectares.json?negotiation_status=concluded&negotiation_status=intended&deal_scope=transnational&deal_scope=domestic
/en/api/hectares.json?negotiation_status=failed&deal_scope=domestic
/en/api/hectares.json?negotiation_status=failed&deal_scope=transnational
/en/api/hectares.json?negotiation_status=failed&deal_scope=transnational&deal_scope=domestic
/en/api/hectares.json?negotiation_status=intended&deal_scope=domestic&data_source_type=1
/en/api/hectares.json?negotiation_status=intended&deal_scope=transnational&data_source_type=1
/en/api/hectares.json?negotiation_status=intended&deal_scope=transnational&deal_scope=domestic&data_source_type=1
/en/api/hectares.json?negotiation_status=concluded&deal_scope=domestic&data_source_type=1
/en/api/hectares.json?negotiation_status=concluded&deal_scope=transnational&data_source_type=1
/en/api/hectares.json?negotiation_status=concluded&deal_scope=transnational&deal_scope=domestic&data_source_type=1
/en/api/hectares.json?negotiation_status=concluded&negotiation_status=intended&deal_scope=domestic&data_source_type=1
/en/api/hectares.json?negotiation_status=concluded&negotiation_status=intended&deal_scope=transnational&data_source_type=1
/en/api/hectares.json?negotiation_status=concluded&negotiation_status=intended&deal_scope=transnational&deal_scope=domestic&data_source_type=1
/en/api/hectares.json?negotiation_status=failed&deal_scope=domestic&data_source_type=1
/en/api/hectares.json?negotiation_status=failed&deal_scope=transnational&data_source_type=1
/en/api/hectares.json?negotiation_status=failed&deal_scope=transnational&deal_scope=domestic&data_source_type=1
"""


class JSONView(TemplateView, ProtocolAPI):
    template_name = "plugins/overview.html"

    def dispatch(self, request, *args, **kwargs):
        if kwargs.get('type') == 'negotiation_status.json':
            return NegotiationStatusJSONView().dispatch(request, args, kwargs)
        elif kwargs.get('type').endswith('.json'):
            return HttpResponse(json.dumps(self.FAKE_VALUES[kwargs['type'][:-5]]))
        raise ValueError('Could not dispatch: ' + str(kwargs))


class NegotiationStatusJSONView(JSONView):
    BASE_FILTER_MAP = {
        "concluded": ("concluded (oral agreement)", "concluded (contract signed)"),
        "intended": ("intended (expression of interest)", "intended (under negotiation)" ),
        "failed": ("failed (contract canceled)", "failed (negotiations failed)"),
    }

    def dispatch(self, request, *args, **kwargs):
        with_names = list(self.get_negotiation_status(request))
        return HttpResponse(json.dumps(with_names, cls=DecimalEncoder))

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
            filter_sql += " AND LOWER(negotiation.attributes->'pi_negotiation_status') IN ('%s') " % "', '".join(stati)
        if len(deal_scope) == 1:
            filter_sql += " AND deal_scope.attributes->'deal_scope' = '%s' " % deal_scope[0]
        if data_source_type:
            filter_sql += " AND 'Media report' <> ( SELECT GROUP_CONCAT(data_source_type.value) FROM a_key_value_lookup data_source_type WHERE a.activity_identifier = data_source_type.activity_identifier AND data_source_type.key = 'type')"

        return filter_sql
