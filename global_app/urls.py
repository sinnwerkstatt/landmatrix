from global_app.views.deal_comparison_view import DealComparisonView
from .views.all_deals_view import AllDealsView
from .views.table_group_view import TableGroupView
from .views.deal_detail_view import DealDetailView
from global_app.views.add_deal_view import AddDealView

from django.conf.urls import url, patterns

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

urlpatterns = patterns('globalapp.views',
    url(r'^$', AllDealsView.as_view(), name='app_main'),
    url(r'^all(?P<type>\.csv)?/$', AllDealsView.as_view(), name='all_deal'),
    url(r'^all(?P<type>\.xml)?/$', AllDealsView.as_view(), name='all_deal'),
    url(r'^all(?P<type>\.xls)?/$', AllDealsView.as_view(), name='all_deal'),
    url(r'^compare/(?P<activity_1_id>[\d]+)/(?P<activity_2_id>[\d]+)/$', DealComparisonView.as_view(), name='compare_deals'),
    url(r'^(?P<group>.+)/(?P<list>.+)/$', TableGroupView.as_view(), name='table_list'),
    url(r'^(?P<deal_id>[\d]+)/$', DealDetailView.as_view(), name='deal_detail'),
    url(r'^add/$', AddDealView.as_view(), name='deal_detail'),

)
