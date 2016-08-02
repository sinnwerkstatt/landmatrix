'''
API calls used for generating charts.
'''
from rest_framework.generics import ListAPIView

from landmatrix.models import Activity
from api.query_sets.filter_query_set import FilterQuerySet
from api.query_sets.deals_query_set import DealsQuerySet
from api.query_sets.hectares_query_set import HectaresQuerySet
from api.query_sets.implementation_status_query_set import \
    ImplementationStatusQuerySet
from api.query_sets.intention_query_set import IntentionQuerySet
from api.query_sets.investor_country_summaries_query_set import \
    InvestorCountrySummariesQuerySet
from api.query_sets.target_country_summaries_query_set import \
    TargetCountrySummariesQuerySet
from api.query_sets.top_10_countries_query_set import \
    Top10CountriesQuerySet
from api.query_sets.transnational_deals_by_country_query_set import \
    TransnationalDealsByCountryQuerySet
from api.query_sets.transnational_deals_query_set import \
    TransnationalDealsQuerySet
from api.query_sets.agricultural_produce_query_set import \
    AllAgriculturalProduceQuerySet
from api.query_sets.produce_info_query_set import \
    ProduceInfoQuerySet
from api.query_sets.resource_extraction_query_set import \
    ResourceExtractionQuerySet
from api.query_sets.logging_query_set import \
    LoggingQuerySet
from api.query_sets.contract_farming_query_set import \
    ContractFarmingQuerySet
from api.serializers import DealSerializer, NegotiationStatusSerializer
from api.views.base import FakeQuerySetListView, FakeQuerySetRetrieveView


class NegotiationStatusListView(ListAPIView):
    serializer_class = NegotiationStatusSerializer

    def get_queryset(self):
        '''
        Get deal and deal_size data for activities by negotiation status.
        To do this we use a combination of FakeQueryset (for filtering),
        regular Django queryset, and some manipulation for ordering and
        adding of missing statuses (those not in the DB.)
        '''
        filter_queryset = FilterQuerySet(self.request)
        filtered_ids = [obj['id'] for obj in filter_queryset.all()]

        queryset = Activity.negotiation_status_objects.all()
        queryset = queryset.filter(pk__in=filtered_ids)
        queryset = list(queryset)

        response_data = []
        # Filter out the blank choice
        status_choices = filter(
            lambda c: c[0], Activity.NEGOTIATION_STATUS_CHOICES)
        for status, description in status_choices:
            deals_count = 0
            hectares_sum = 0
            # It may seem strange to iterate over qs results, but it's
            # better than the extra queries
            for obj in queryset:
                if obj['negotiation_status'] == status:
                    deals_count = obj['deals_count']
                    hectares_sum = obj['hectares_sum']
                    break

            response_data.append({
                'name': description,
                'deals': deals_count,
                'hectares': hectares_sum,
            })

        return response_data


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


class AgriculturalProduceListView(FakeQuerySetListView):
    fake_queryset_class = AllAgriculturalProduceQuerySet


class ProduceInfoView(FakeQuerySetRetrieveView):
    fake_queryset_class = ProduceInfoQuerySet


class ResourceExtractionView(FakeQuerySetListView):
    fake_queryset_class = ResourceExtractionQuerySet


class LoggingView(FakeQuerySetRetrieveView):
    fake_queryset_class = LoggingQuerySet


class ContractFarmingView(FakeQuerySetRetrieveView):
    fake_queryset_class = ContractFarmingQuerySet
