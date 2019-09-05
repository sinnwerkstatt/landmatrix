from django.conf.urls import url

from apps.grid.views.deal import DealListView
from apps.grid.views.export import ExportView
from apps.grid.views.investor import InvestorListView

CACHE_TIMEOUT = 24*3600

urlpatterns = [
    # please leave them here, commented out, for quick cache de-/activation when developing
    # url(r'^$', DealsView.as_view(), name='app_main'),
    # url(r'^(?P<group>.+)/(?P<list>.+)/$', DealListView.as_view(), name='deal_list'),

    url(
        r'^$',
        DealListView.as_view(),
        name='data'
    ),
    url(
        r'^all\.(?P<format>(csv|xml|xls))/$',
        ExportView.as_view(),
        name='export'
    ),
    url(
        r'^(?P<group>.+)/(?P<group_value>.+)\.(?P<format>(csv|xml|xls))/$',
        ExportView.as_view(),
        name='export'
    ),
    url(
        r'^(?P<group>.+)\.(?P<format>(csv|xml|xls))/$',
        ExportView.as_view(),
        name='export'
    ),

    url(
        r'^investors/$',
        InvestorListView.as_view(),
        name='investor_list'
    ),
    url(
        r'^investors/(?P<group>[^/]+)/(?P<group_value>.+)/$',
        InvestorListView.as_view(),
        name='investor_list'
    ),
    url(
        r'^investors/(?P<group>.+)/$',
        InvestorListView.as_view(),
        name='investor_list'
    ),

    # needs to come last, regexp catches all expressions
    url(
        r'^(?P<group>[^/]+)/(?P<group_value>.+)/$',
        DealListView.as_view(),
        name='deal_list'
    ),
    url(
        r'^(?P<group>.+)/$',
        DealListView.as_view(),
        name='deal_list'
    ),
]
