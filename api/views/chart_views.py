'''
API calls used for generating charts.
'''
from rest_framework.generics import ListAPIView
from rest_framework.schemas import ManualSchema
import coreapi
import coreschema

from landmatrix.models.activity import Activity
from api.query_sets.filter_query_set import FilterQuerySet
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
from api.serializers import NegotiationStatusSerializer
from api.views.base import FakeQuerySetListView, FakeQuerySetRetrieveView


class NegotiationStatusListView(ListAPIView):
    """
    Get deal aggregations grouped by Negotiation status.
    Used within the charts section.
    """
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


class ImplementationStatusListView(FakeQuerySetListView):
    """
    Get deal aggregations grouped by Implementation status.
    Used within the charts section.
    """
    fake_queryset_class = ImplementationStatusQuerySet


class InvestmentIntentionListView(FakeQuerySetListView):
    """
    Get deal aggregations grouped by Intention.
    Used within the charts section.
    """
    fake_queryset_class = IntentionQuerySet
    schema = ManualSchema(
        fields=[
            coreapi.Field(
                "intention",
                required=False,
                location="query",
                description="Parent intention",
                schema=coreschema.String(),
            ),
        ]
    )


class InvestorCountrySummaryView(FakeQuerySetListView):
    """
    Get deal aggregations grouped by Investor country.
    """
    fake_queryset_class = InvestorCountrySummariesQuerySet


class InvestorCountriesForTargetCountryView(FakeQuerySetListView):
    """
    Get deal aggregations grouped for Investor country.
    """
    schema = ManualSchema(
        fields=[
            coreapi.Field(
                "country_id",
                required=False,
                location="data",
                description="Country ID",
                schema=coreschema.Integer(),
            ),
        ]
    )
    fake_queryset_class = InvestorCountrySummariesQuerySet


class TargetCountrySummaryView(FakeQuerySetListView):
    """
    Get deal aggregations grouped by Target country.
    """
    fake_queryset_class = TargetCountrySummariesQuerySet


class TargetCountriesForInvestorCountryView(FakeQuerySetListView):
    """
    Get deal aggregations grouped for Target country/region.
    """
    schema = ManualSchema(
        fields=[
            coreapi.Field(
                "country_id",
                required=False,
                location="data",
                description="Country ID",
                schema=coreschema.Integer(),
            ),
            coreapi.Field(
                "region_id",
                required=False,
                location="data",
                description="Region ID",
                schema=coreschema.Integer(),
            ),
        ]
    )
    fake_queryset_class = TargetCountrySummariesQuerySet


class TransnationalDealListView(FakeQuerySetListView):
    """
    Get deal aggregations for transnational deals grouped by country.
    Used within the charts section.
    """
    schema = ManualSchema(
        fields=[
            coreapi.Field(
                "region",
                required=False,
                location="data",
                description="Region ID",
                schema=coreschema.Integer(),
            ),
        ]
    )
    fake_queryset_class = TransnationalDealsQuerySet


class Top10CountriesView(FakeQuerySetRetrieveView):
    """
    Get top 10 Investor or Target countries.
    Used within the charts section.
    """
    fake_queryset_class = Top10CountriesQuerySet


class TransnationalDealsByCountryView(FakeQuerySetRetrieveView):
    """
    Get deal aggregations for transnational deals of given country grouped by role (Investor or Target country).
    Used within the charts section.
    """
    fake_queryset_class = TransnationalDealsByCountryQuerySet


class HectaresView(FakeQuerySetRetrieveView):
    """
    Get global deal aggregations (no. of deals and size in hectares).
    Used within the charts section.
    """
    fake_queryset_class = HectaresQuerySet


class AgriculturalProduceListView(FakeQuerySetListView):
    """
    Get deal aggregations grouped by Agricultural Produce.
    Used within the charts section.
    """
    fake_queryset_class = AllAgriculturalProduceQuerySet


class ProduceInfoView(FakeQuerySetRetrieveView):
    """
    Get deal aggregations grouped by Animals, Minerals and Crops.
    Used within the charts section.
    """
    fake_queryset_class = ProduceInfoQuerySet


class ResourceExtractionView(FakeQuerySetListView):
    """
    Get deal aggregations for Resource Extraction deals grouped by Negotiation status.
    Used within the charts section.
    """
    fake_queryset_class = ResourceExtractionQuerySet


class LoggingView(FakeQuerySetRetrieveView):
    """
    Get deal aggregations for Logging deals grouped by Negotiation status.
    Used within the charts section.
    """
    fake_queryset_class = LoggingQuerySet


class ContractFarmingView(FakeQuerySetRetrieveView):
    """
    Get deal aggregations for Contract Farming deals grouped by Negotiation status.
    Used within the charts section.
    """
    fake_queryset_class = ContractFarmingQuerySet
