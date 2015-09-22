from api.views.agricultural_produce_json_view import AgriculturalProduceJSONView
from api.views.target_country_summaries_json_view import TargetCountrySummariesJSONView
from api.views.investor_country_summaries_json_view import InvestorCountrySummariesJSONView
from api.views.top_10_countries_json_view import Top10CountriesJSONView
from api.views.transnational_deals_by_country_json_view import TransnationalDealsByCountryJSONView
from api.views.transnational_deals_json_view import TransnationalDealsJSONView
from api.views.implementation_status_json_view import ImplementationStatusJSONView
from api.views.intention_of_investment_json_view import IntentionOfInvestmentJSONView
from api.views.negotiation_status_json_view import NegotiationStatusJSONView

from django.views.generic.base import TemplateView

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


todo_list_of_urls = """
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

    template_name = 'plugins/overview.html'

    targets = {
        'negotiation_status.json': NegotiationStatusJSONView,
        'implementation_status.json': ImplementationStatusJSONView,
        'intention_of_investment.json': IntentionOfInvestmentJSONView,
        'transnational_deals.json': TransnationalDealsJSONView,
        'top-10-countries.json': Top10CountriesJSONView,
        'transnational_deals_by_country.json': TransnationalDealsByCountryJSONView,
        'investor_country_summaries.json': InvestorCountrySummariesJSONView,
        'target_country_summaries.json': TargetCountrySummariesJSONView,
        'agricultural-produce.json': AgriculturalProduceJSONView,
    }

    def dispatch(self, request, *args, **kwargs):
        if kwargs.get('type') in self.targets:
            return self.targets[kwargs.get('type')]().dispatch(request, args, kwargs)
        raise ValueError(str(kwargs) + ' could not be resolved to any of ' + str(list(self.targets.keys())))

