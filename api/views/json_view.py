from api.views.transnational_deals_json_view import TransnationalDealsJSONView
from api.views.implementation_status_json_view import ImplementationStatusJSONView
from api.views.intention_of_investment_json_view import IntentionOfInvestmentJSONView
from api.views.negotiation_status_json_view import NegotiationStatusJSONView

from django.views.generic.base import TemplateView

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


todo_list_of_urls = """
/en/api/top-10-countries.json?negotiation_status=concluded&deal_scope=transnational
/en/api/top-10-countries.json?negotiation_status=intended&deal_scope=transnational
/en/api/top-10-countries.json?negotiation_status=concluded&negotiation_status=intended&deal_scope=transnational
/en/api/top-10-countries.json?negotiation_status=failed&deal_scope=transnational
/en/api/top-10-countries.json?negotiation_status=concluded&deal_scope=transnational&data_source_type=1
/en/api/top-10-countries.json?negotiation_status=intended&deal_scope=transnational&data_source_type=1
/en/api/top-10-countries.json?negotiation_status=concluded&negotiation_status=intended&deal_scope=transnational&data_source_type=1
/en/api/top-10-countries.json?negotiation_status=failed&deal_scope=transnational&data_source_type=1

/en/api/transnational_deals_by_country.json?negotiation_status=concluded&deal_scope=transnational&country=384
...

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


class JSONView(TemplateView):

    template_name = "plugins/overview.html"

    def dispatch(self, request, *args, **kwargs):
        if kwargs.get('type') == 'negotiation_status.json':
            return NegotiationStatusJSONView().dispatch(request, args, kwargs)
        elif kwargs.get('type') == "implementation_status.json":
            return ImplementationStatusJSONView().dispatch(request, args, kwargs)
        elif kwargs.get('type') == "intention_of_investment.json":
            return IntentionOfInvestmentJSONView().dispatch(request, args, kwargs)
        elif kwargs.get('type') == "transnational_deals.json":
            return TransnationalDealsJSONView().dispatch(request, args, kwargs)
        raise ValueError('Could not dispatch: ' + str(kwargs))

