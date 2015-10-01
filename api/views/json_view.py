from api.query_sets.agricultural_produce_query_set import AllAgriculturalProduceQuerySet
from api.query_sets.deals_query_set import DealsQuerySet
from api.query_sets.hectares_query_set import HectaresQuerySet
from api.query_sets.implementation_status_query_set import ImplementationStatusQuerySet
from api.query_sets.intention_query_set import IntentionQuerySet
from api.query_sets.investor_country_summaries_query_set import InvestorCountrySummariesQuerySet
from api.query_sets.negotiation_status_query_set import NegotiationStatusQuerySet
from api.query_sets.target_country_summaries_query_set import TargetCountrySummariesQuerySet
from api.query_sets.top_10_countries_query_set import Top10CountriesQuerySet
from api.query_sets.transnational_deals_by_country_query_set import TransnationalDealsByCountryQuerySet
from api.query_sets.transnational_deals_query_set import TransnationalDealsQuerySet


from api.views.decimal_encoder import DecimalEncoder

from django.http.response import HttpResponse
import json

from django.views.generic.base import TemplateView

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


def json_generator(query_set_class):

    class Generator:
        def dispatch(self, request):
            data = query_set_class(request.GET).all()
            return HttpResponse(json.dumps(data, cls=DecimalEncoder), content_type="application/json")

    return Generator

AgriculturalProduceJSONGenerator = json_generator(AllAgriculturalProduceQuerySet)
DealsJSONGenerator = json_generator(DealsQuerySet)
ImplementationStatusJSONGenerator = json_generator(ImplementationStatusQuerySet)
IntentionOfInvestmentJSONGenerator = json_generator(IntentionQuerySet)
InvestorCountrySummariesJSONGenerator = json_generator(InvestorCountrySummariesQuerySet)
NegotiationStatusJSONGenerator = json_generator(NegotiationStatusQuerySet)
TargetCountrySummariesJSONGenerator = json_generator(TargetCountrySummariesQuerySet)
Top10CountriesJSONGenerator = json_generator(Top10CountriesQuerySet)
TransnationalDealsJSONGenerator = json_generator(TransnationalDealsQuerySet)
TransnationalDealsByCountryJSONGenerator = json_generator(TransnationalDealsByCountryQuerySet)
HectaresJSONGenerator = json_generator(HectaresQuerySet)


class JSONView(TemplateView):

    template_name = 'plugins/overview.html'

    targets = {
        'negotiation_status.json':             NegotiationStatusJSONGenerator,
        'implementation_status.json':          ImplementationStatusJSONGenerator,
        'intention_of_investment.json':        IntentionOfInvestmentJSONGenerator,
        'transnational_deals.json':            TransnationalDealsJSONGenerator,
        'top-10-countries.json':               Top10CountriesJSONGenerator,
        'transnational_deals_by_country.json': TransnationalDealsByCountryJSONGenerator,
        'investor_country_summaries.json':     InvestorCountrySummariesJSONGenerator,
        'target_country_summaries.json':       TargetCountrySummariesJSONGenerator,
        'agricultural-produce.json':           AgriculturalProduceJSONGenerator,
        'hectares.json':                       HectaresJSONGenerator,
        'deals.json':                          DealsJSONGenerator,
    }

    def dispatch(self, request, *args, **kwargs):
        if kwargs.get('type') in self.targets:
            return self.targets[kwargs.get('type')]().dispatch(request)
        raise ValueError(str(kwargs) + ' could not be resolved to any of ' + str(list(self.targets.keys())))

