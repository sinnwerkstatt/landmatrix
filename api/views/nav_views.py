'''
API calls used by the nav menus.
'''

from api.query_sets.countries_query_set import CountriesQuerySet
from api.query_sets.investors_query_set import InvestorsQuerySet
from api.query_sets.regions_query_set import RegionsQuerySet
from api.views.base import FakeQuerySetListView


class CountryListView(FakeQuerySetListView):
    fake_queryset_class = CountriesQuerySet


class RegionListView(FakeQuerySetListView):
    fake_queryset_class = RegionsQuerySet


class InvestorListView(FakeQuerySetListView):
    fake_queryset_class = InvestorsQuerySet
