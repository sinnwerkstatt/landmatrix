'''
API calls used by the nav menus.
'''
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination

from wagtailcms.models import RegionPage
from api.query_sets.countries_query_set import CountriesQuerySet
from api.query_sets.investors_query_set import InvestorsQuerySet
from api.serializers import RegionSerializer
from api.views.base import FakeQuerySetListView


class CountryListView(FakeQuerySetListView):
    """
    Get all countries grouped by National Observatories and Others.
    Used by the navigation.
    """
    fake_queryset_class = CountriesQuerySet


class RegionListView(ListAPIView):
    """
    Get all regions.
    Used by the navigation.
    """
    # Filter out pages without an assigned region, those just error
    queryset = RegionPage.objects.filter(
        region__isnull=False).order_by('title')
    serializer_class = RegionSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 1000


class InvestorListView(FakeQuerySetListView):
    """
    Get all Operational companies, Parent companies and Tertiary investors/lenders.
    """
    fake_queryset_class = InvestorsQuerySet
    pagination_class = StandardResultsSetPagination

