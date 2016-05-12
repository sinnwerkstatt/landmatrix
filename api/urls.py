from django.conf.urls import url
from django.views.decorators.cache import cache_page

from api.views.dashboard_filter_view import DashboardFilterView
from api.views.deal_detail_view import DealDetailView
from api.views.filter_preset_view import FilterPresetView
from api.views.investor_network_view import InvestorNetworkView
from api.views.json_view import JSONView
from api.views.filter_view import FilterView

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

CACHE_TIMEOUT = 24*3600

urlpatterns = [
    url(r'^filter\.json', FilterView.as_view(), name='api_filter'),
    url(r'^dashboard_filter\.json', DashboardFilterView.as_view(),
        name='api_dashboard_filter'),
    url(r'^filter_preset\.json', FilterPresetView.as_view(),
        name='api_dashboard_filter_preset'),
    url(r'^deal_detail\.json', DealDetailView.as_view(), {'format': 'json'},
        name='api_deal_detail'),
    url(r'^investor_network\.json', InvestorNetworkView.as_view(),
        {'format': 'json'}, name='api_investor_network'),
    url(r'^(?P<type>.*\.json)', cache_page(CACHE_TIMEOUT)(JSONView.as_view()),
        name='landmatrix_api'),
]
