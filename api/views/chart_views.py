'''
API calls used for generating charts.
'''
from api.query_sets.agricultural_produce_query_set import \
    AllAgriculturalProduceQuerySet
from api.query_sets.deals_query_set import DealsQuerySet
from api.query_sets.hectares_query_set import HectaresQuerySet
from api.query_sets.implementation_status_query_set import \
    ImplementationStatusQuerySet
from api.query_sets.intention_query_set import IntentionQuerySet
from api.query_sets.investor_country_summaries_query_set import \
    InvestorCountrySummariesQuerySet
from api.query_sets.negotiation_status_query_set import \
    NegotiationStatusQuerySet
from api.query_sets.target_country_summaries_query_set import \
    TargetCountrySummariesQuerySet
from api.query_sets.top_10_countries_query_set import \
    Top10CountriesQuerySet
from api.query_sets.transnational_deals_by_country_query_set import \
    TransnationalDealsByCountryQuerySet
from api.query_sets.transnational_deals_query_set import \
    TransnationalDealsQuerySet

from api.serializers import DealSerializer
from api.views.base import FakeQuerySetListView, FakeQuerySetRetrieveView


class AgriculturalProduceListView(FakeQuerySetListView):
    fake_queryset_class = AllAgriculturalProduceQuerySet


class NegotiationStatusListView(FakeQuerySetListView):
    fake_queryset_class = NegotiationStatusQuerySet


class DealListView(FakeQuerySetListView):
    fake_queryset_class = DealsQuerySet
    serializer_class = DealSerializer


class ImplementationStatusListView(FakeQuerySetListView):
    fake_queryset_class = ImplementationStatusQuerySet


class InvestmentIntentionListView(FakeQuerySetListView):
    fake_queryset_class = IntentionQuerySet


class InvestorCountrySummaryListView(FakeQuerySetListView):
    fake_queryset_class = InvestorCountrySummariesQuerySet


class TargetCountrySummaryListView(FakeQuerySetListView):
    fake_queryset_class = TargetCountrySummariesQuerySet


class TransnationalDealListView(FakeQuerySetListView):
    fake_queryset_class = TransnationalDealsQuerySet


class Top10CountriesView(FakeQuerySetRetrieveView):
    fake_queryset_class = Top10CountriesQuerySet


class TransnationalDealsByCountryView(FakeQuerySetRetrieveView):
    fake_queryset_class = TransnationalDealsByCountryQuerySet


class HectaresView(FakeQuerySetRetrieveView):
    fake_queryset_class = HectaresQuerySet
