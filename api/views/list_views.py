from rest_framework.generics import ListAPIView

from api.serializers import PassThruSerializer
from api.query_sets.agricultural_produce_query_set import \
    AllAgriculturalProduceQuerySet
from api.query_sets.countries_query_set import CountriesQuerySet
from api.query_sets.deals_query_set import DealsQuerySet
from api.query_sets.hectares_query_set import HectaresQuerySet
from api.query_sets.implementation_status_query_set import \
    ImplementationStatusQuerySet
from api.query_sets.intention_query_set import IntentionQuerySet
from api.query_sets.investor_country_summaries_query_set import \
    InvestorCountrySummariesQuerySet
from api.query_sets.investors_query_set import InvestorsQuerySet
from api.query_sets.latest_changes_query_set import LatestChangesQuerySet
from api.query_sets.negotiation_status_query_set import \
    NegotiationStatusQuerySet
from api.query_sets.regions_query_set import RegionsQuerySet
from api.query_sets.statistics_query_set import StatisticsQuerySet
from api.query_sets.target_country_summaries_query_set import \
    TargetCountrySummariesQuerySet
from api.query_sets.top_10_countries_query_set import \
    Top10CountriesQuerySet
from api.query_sets.transnational_deals_by_country_query_set import \
    TransnationalDealsByCountryQuerySet
from api.query_sets.transnational_deals_query_set import \
    TransnationalDealsQuerySet
from api.query_sets.users_query_set import UsersQuerySet
from grid.views.activity_protocol import ActivityQuerySet


__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class FakeQuerySetListView(ListAPIView):
    '''
    Base view class that handles fake querysets (they return presentation
    ready data.
    '''
    serializer_class = PassThruSerializer
    fake_queryset_class = None

    def get_queryset(self):
        queryset_class = self.fake_queryset_class
        queryset = queryset_class(self.request)
        return queryset.all()


class CountryListView(FakeQuerySetListView):
    '''
    Country list for nav menus.
    '''
    fake_queryset_class = CountriesQuerySet


class RegionListView(FakeQuerySetListView):
    '''
    Region list for nav menus.
    '''
    fake_queryset_class = RegionsQuerySet


class InvestorListView(FakeQuerySetListView):
    '''
    Investor list for nav menus.
    '''
    fake_queryset_class = InvestorsQuerySet


class UserListView(FakeQuerySetListView):
    fake_queryset_class = UsersQuerySet


class StatisticsListView(FakeQuerySetListView):
    fake_queryset_class = StatisticsQuerySet


class ActivityListView(FakeQuerySetListView):
    fake_queryset_class = ActivityQuerySet


class LatestChangesListView(FakeQuerySetListView):
    '''
    Lists recent changes to the database (add, change, delete or comment)
    '''
    fake_queryset_class = LatestChangesQuerySet


class AgriculturalProduceListView(FakeQuerySetListView):
    '''
    For chart views of agricultural produce breakdowns.
    '''
    fake_queryset_class = AllAgriculturalProduceQuerySet


class NegotiationStatusListView(FakeQuerySetListView):
    '''
    For charting the number of deals per status.
    '''
    fake_queryset_class = NegotiationStatusQuerySet


class DealListView(FakeQuerySetListView):
    '''
    Used to generate charts.
    '''
    fake_queryset_class = DealsQuerySet


class ImplementationStatusListView(FakeQuerySetListView):
    '''
    Used to generate charts.
    '''
    fake_queryset_class = ImplementationStatusQuerySet


class InvestmentIntentionListView(FakeQuerySetListView):
    '''
    Used to generate charts.
    '''
    fake_queryset_class = IntentionQuerySet


class InvestorCountrySummaryListView(FakeQuerySetListView):
    '''
    Used to generate charts.
    '''
    fake_queryset_class = InvestorCountrySummariesQuerySet


class TargetCountrySummaryListView(FakeQuerySetListView):
    '''
    Used to generate charts.
    '''
    fake_queryset_class = TargetCountrySummariesQuerySet


class Top10CountriesListView(FakeQuerySetListView):
    '''
    Used to generate charts.
    '''
    fake_queryset_class = Top10CountriesQuerySet


class TransnationalDealListView(FakeQuerySetListView):
    '''
    Used to generate charts.
    '''
    fake_queryset_class = TransnationalDealsQuerySet


class TransnationalDealsByCountryListView(FakeQuerySetListView):
    '''
    Used to generate charts.
    '''
    fake_queryset_class = TransnationalDealsByCountryQuerySet


class HectareListView(FakeQuerySetListView):
    '''
    Used to generate charts.
    '''
    fake_queryset_class = HectaresQuerySet
