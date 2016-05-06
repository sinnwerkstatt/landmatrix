"""The `urlpatterns` list routes URLs to views. For more information please
   see: https://docs.djangoproject.com/en/1.8/topics/http/urls/
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
from django.conf.urls import url, patterns
from .views import *


__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


urlpatterns = patterns(
    'chart.views',
    url(r'^$', TransnationalDealsChartView.as_view(),
        name='charts'),
    url(r'^$', TransnationalDealsChartView.as_view(),
        name='chart_transnational_deals'),
    url(r'^overview$', OverviewChartView.as_view(), name='chart_overview'),
    url(r'^specialinterest$', SpecialInterestView.as_view(), name='special_interest'),
    url(r'^map-of-investments/$', MapOfInvestmentsChartView.as_view(),
        name='chart_map_of_investments'),
    url(r'^agricultural-drivers/$', AgriculturalDriversChartView.as_view(),
        name='chart_agricultural_drivers'),
    url(r'^perspective/$', PerspectiveChartView.as_view(),
        name='chart_perspective'),
    url(r'^all(?P<type>\.csv)?/$', ChartView.as_view(), name='all_charts'),
    # PDF views for charts
    url(r'^overview\.pdf$', OverviewChartView.as_view(),
        {'format': 'PDF'}, name='chart_overview_pdf'),
    url(r'^transnational-deals\.pdf$', TransnationalDealsChartView.as_view(),
        {'format': 'PDF'}, name='chart_transnational_deals_pdf'),
    url(r'^map-of-investments\.pdf$', MapOfInvestmentsChartView.as_view(),
        {'format': 'PDF'}, name='chart_map_of_investments_pdf'),
    url(r'^agricultural-drivers\.pdf$', AgriculturalDriversChartView.as_view(),
        {'format': 'PDF'}, name='chart_agricultural_drivers_pdf'),
    url(r'^perspective\.pdf$', PerspectiveChartView.as_view(),
        {'format': 'PDF'}, name='chart_perspective_pdf'),
    url(r'^specialinterest\.pdf$', SpecialInterestView.as_view(),
        {'format': 'PDF'}, name='special_interest_pdf'),

)
