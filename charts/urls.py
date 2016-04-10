__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

""" he `urlpatterns` list routes URLs to views. For more information please see:
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
from django.conf.urls import url, patterns
from .views import *

urlpatterns = patterns('chart.views',
	url(r'^$', TransnationalDealsChartView.as_view(), name='chart_transnational_deals'),
    url(r'^transnational_deals\.pdf$', TransnationalDealsPDFView.as_view(),
        name='chart_transnational_deals_pdf'),
    url(r'^overview$', OverviewChartView.as_view(), name='chart_overview'),
	url(r'^map-of-investments/$', MapOfInvestmentsChartView.as_view(), name='chart_map_of_investments'),
	url(r'^agricultural-drivers/$', AgriculturalDriversChartView.as_view(), name='chart_agricultural_drivers'),
	url(r'^perspective/$', PerspectiveChartView.as_view(), name='chart_perspective'),
    url(r'^all(?P<type>\.csv)?/$', ChartView.as_view(), name='all_charts'),
)
