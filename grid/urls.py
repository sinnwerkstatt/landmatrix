from grid.views.deal_comparison_view import DealComparisonView
from grid.views.change_deal_view import ChangeDealView
from .views.all_deals_view import AllDealsView
from .views.table_group_view import TableGroupView
from .views.deal_detail_view import DealDetailView
from grid.views.add_deal_view import AddDealView
from grid.views.stakeholder_view import StakeholderView

from django.conf.urls import url, patterns
from django.views.decorators.cache import cache_page

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

""" For more information please see: https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

CACHE_TIMEOUT = 24*3600

urlpatterns = patterns('grid.views',
    # please leave them here, commented out, for quick cache de-/activation when developing
    # url(r'^$', AllDealsView.as_view(), name='app_main'),
    # url(r'^all(?P<type>\.csv)?/$', AllDealsView.as_view(), name='all_deal'),
    # url(r'^all(?P<type>\.xml)?/$', AllDealsView.as_view(), name='all_deal'),
    # url(r'^all(?P<type>\.xls)?/$', AllDealsView.as_view(), name='all_deal'),
    # url(r'^(?P<group>.+)/(?P<list>.+)/$', TableGroupView.as_view(), name='table_list'),

    url(r'^$', cache_page(CACHE_TIMEOUT)(AllDealsView.as_view()), name='app_main'),
    url(r'^all(?P<type>\.csv)?/$', cache_page(CACHE_TIMEOUT)(AllDealsView.as_view()), name='all_deal'),
    url(r'^all(?P<type>\.xml)?/$', cache_page(CACHE_TIMEOUT)(AllDealsView.as_view()), name='all_deal'),
    url(r'^all(?P<type>\.xls)?/$', cache_page(CACHE_TIMEOUT)(AllDealsView.as_view()), name='all_deal'),
    url(
        r'^compare/(?P<activity_1_id>[\d]+)/(?P<activity_2_id>[\d]+)/$',
        cache_page(CACHE_TIMEOUT)(DealComparisonView.as_view()),
        name='compare_deals'
    ),
    url(
        r'^compare/(?P<activity_1>[\d_\.]+)/$',
        cache_page(CACHE_TIMEOUT)(DealComparisonView.as_view()),
        name='compare_deals'
    ),
    url(
        r'^compare/(?P<activity_1>.+)/$',
        cache_page(CACHE_TIMEOUT)(DealComparisonView.as_view()),
        name='compare_deals'
    ),
    url(r'^add/$', AddDealView.as_view(), name='add_deal'),

    url(r'^change/(?P<deal_id>[\d]+)/$', ChangeDealView.as_view(), name='change_deal'),
    url(r'^(?P<deal_id>[\d]+)/$', cache_page(CACHE_TIMEOUT)(DealDetailView.as_view()), name='deal_detail'),
    url(r'^(?P<deal_id>[\d_\.]+)/$', cache_page(CACHE_TIMEOUT)(DealDetailView.as_view()), name='deal_detail'),
    # needs to come last, regexp catches all expressions
    url(r'^(?P<group>.+)/$', cache_page(CACHE_TIMEOUT)(TableGroupView.as_view()), name='table_list'),
    # url(r'^(?P<group>.+)/(?P<list>)/$', cache_page(CACHE_TIMEOUT)(TableGroupView.as_view()), name='table_list'),
)
