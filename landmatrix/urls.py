"""landmatrix URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
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

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin

from grid.views.add_deal_view import AddDealView
from grid.views.change_deal import ChangeDealView
from grid.views.deal_comparison_view import DealComparisonView
from grid.views.deal_detail_view import DealDetailView
from grid.views.filter_widget_ajax_view import FilterWidgetAjaxView
from api import urls as api_urls
from grid import urls as grid_urls
from map import urls as map_urls
from charts import urls as charts_urls
from editor import urls as editor_urls
from landmatrix.views.start_view import StartView
from grid.views.stakeholder_view import StakeholderView

urlpatterns = i18n_patterns('',

    url('^accounts/', include('django.contrib.auth.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^api/', include(api_urls)),
    url(r'^global/data/', include(grid_urls)),
    url(r'^global/map/', include(map_urls)),
    url(r'^global/charts/', include(charts_urls)),

    url(r'^deal/(?P<deal_id>[\d]+)/$', DealDetailView.as_view(), name='deal_detail'),
    url(r'^deal/(?P<deal_id>[\d_\.]+)/$', DealDetailView.as_view(), name='deal_detail'),
    url(r'^deal/add/$', AddDealView.as_view(), name='add_deal'),
    url(r'^deal/compare/(?P<activity_1_id>[\d]+)/(?P<activity_2_id>[\d]+)/$', DealComparisonView.as_view(), name='compare_deals'),
    url(r'^deal/compare/(?P<activity_1>[\d_\.]+)/$', DealComparisonView.as_view(), name='compare_deals'),
    url(r'^deal/compare/(?P<activity_1>.+)/$', DealComparisonView.as_view(), name='compare_deals'),
    url(r'^deal/edit/(?P<deal_id>[\d]+)$', ChangeDealView.as_view(), name='change_deal'),

    url(r'^stakeholder/$', StakeholderView.as_view(), name='stakeholder_form'),

    url(r'^editor/', include(editor_urls)),
    url(r'^ajax/widget/(?P<action>operators|values)', FilterWidgetAjaxView.as_view(), name='ajax_widget'),
    url(r'^chart/', include(chart_urls)),
    url(r'^$', StartView.as_view(), name='start'),
    #url(r'^', include('cms.urls')),
    url(r'^select2/', include('django_select2.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
