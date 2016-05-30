from django.conf.urls import url
from django.views.decorators.cache import cache_page

from api.views import *


__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'
CACHE_TIMEOUT = 24*3600


def cache_view_class(cls):
    return cache_page(CACHE_TIMEOUT)(cls.as_view())


urlpatterns = [
    url(r'^filter\.json', FilterView.as_view(), {'format': 'json'},
        name='api_filter'),
    url(r'^dashboard_filter\.json', DashboardFilterView.as_view(),
        {'format': 'json'}, name='api_dashboard_filter'),
    url(r'^filter_preset\.json', FilterPresetView.as_view(),
        {'format': 'json'}, name='api_dashboard_filter_preset'),
    url(r'^deal_detail\.json', DealDetailView.as_view(), {'format': 'json'},
        name='api_deal_detail'),
    url(r'^investor_network\.json', InvestorNetworkView.as_view(),
        {'format': 'json'}, name='api_investor_network'),
    url(r'^latest_changes\.json', cache_view_class(LatestChangesListView),
        {'format': 'json'}, name='latest_changes_api'),
    url(r'^agricultural-produce\.json',
        cache_view_class(AgriculturalProduceListView), {'format': 'json'},
        name='agricultural_produce_api'),
    url(r'^negotiation_status\.json',
        cache_view_class(NegotiationStatusListView), {'format': 'json'},
        name='negotiation_status_api'),
    url(r'^countries\.json', cache_view_class(CountryListView),
        {'format': 'json'}, name='countries_api'),
    url(r'^regions\.json', cache_view_class(RegionListView),
        {'format': 'json'}, name='regions_api'),
    url(r'^investors\.json', cache_view_class(InvestorListView),
        {'format': 'json'}, name='investors_api'),
    url(r'^implementation_status\.json',
        cache_view_class(ImplementationStatusListView), {'format': 'json'},
        name='implementation_status_api'),
    url(r'^intention_of_investment\.json',
        cache_view_class(InvestmentIntentionListView), {'format': 'json'},
        name='intention_of_investment_api'),
    url(r'^transnational_deals\.json',
        cache_view_class(TransnationalDealListView), {'format': 'json'},
        name='transnational_deals_api'),
    url(r'^top-10-countries\.json', cache_view_class(Top10CountriesView),
        {'format': 'json'}, name='top_10_countries_api'),
    url(r'^transnational_deals_by_country\.json',
        cache_view_class(TransnationalDealsByCountryView),
        {'format': 'json'}, name='transnational_deals_by_country_api'),
    url(r'^investor_country_summaries\.json',
        cache_view_class(InvestorCountrySummaryListView),
        {'format': 'json'}, name='investor_country_summaries_api'),
    url(r'^target_country_summaries\.json',
        cache_view_class(TargetCountrySummaryListView),
        {'format': 'json'}, name='target_country_summaries_api'),
    url(r'^investor_countries_for_target_country\.json',
        cache_view_class(InvestorCountriesForTargetCountryView),
        {'format': 'json'}, name='investor_countries_for_target_country_api'),
    url(r'^target_countries_for_investor_country\.json',
        cache_view_class(TargetCountriesForInvestorCountryView),
        {'format': 'json'}, name='target_countries_for_investor_country_api'),
    url(r'^hectares\.json', cache_view_class(HectaresView),
        {'format': 'json'}, name='hectares_api'),
    url(r'^deals\.json', cache_view_class(DealListView), {'format': 'json'},
        name='deals_api'),
    url(r'^activities\.json', cache_view_class(ActivityListView),
        {'format': 'json'}, name='activities_api'),
    url(r'^statistics\.json', cache_view_class(StatisticsListView),
        {'format': 'json'}, name='statistics_api'),
    url(r'^users\.json', cache_view_class(UserListView), {'format': 'json'},
        name='users_api'),
]
