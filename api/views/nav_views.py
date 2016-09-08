'''
API calls used by the nav menus.
'''
from rest_framework.generics import ListAPIView

from wagtailcms.models import RegionPage
from api.query_sets.countries_query_set import CountriesQuerySet
from api.query_sets.investors_query_set import InvestorsQuerySet
from api.serializers import RegionSerializer
from api.views.base import FakeQuerySetListView


class CountryListView(FakeQuerySetListView):
    fake_queryset_class = CountriesQuerySet


class RegionListView(ListAPIView):
    # Filter out pages without an assigned region, those just error
    queryset = RegionPage.objects.filter(
        region__isnull=False).order_by('title')
    serializer_class = RegionSerializer


class InvestorListView(FakeQuerySetListView):
    fake_queryset_class = InvestorsQuerySet
