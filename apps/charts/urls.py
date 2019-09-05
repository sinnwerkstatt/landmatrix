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
from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^$', ChartRedirectView.as_view(), name='charts'),
    # url(r'^all(?P<type>\.csv)?/$', #     ChartView.as_view(), name='all_charts'),
    url(r'^intention/$', IntentionChartView.as_view(), name='chart_intention'),
    url(r'^negotiation-status/$', NegotiationStatusChartView.as_view(), name='chart_negotiation_status'),
    url(r'^implementation-status/$', ImplementationStatusChartView.as_view(), name='chart_implementation_status'),
    url(r'^intention-agriculture/$', IntentionAgricultureChartView.as_view(), name='chart_intention_agriculture'),
    url(r'^web-of-transnational-deals/$', TransnationalDealsChartView.as_view(), name='chart_transnational_deals'),
    url(r'^map-of-investments/$', MapOfInvestmentsChartView.as_view(), name='chart_map_of_investments'),
    url(r'^perspective/$', PerspectiveChartView.as_view(), name='chart_perspective'),
    url(r'^agricultural-drivers/$', AgriculturalDriversChartView.as_view(), name='chart_agricultural_drivers'),
    url(r'^produce-info/$', ProduceInfoChartView.as_view(), name='chart_produce_info'),
    url(r'^mining/$', MiningChartView.as_view(), name='chart_mining'),
    url(r'^logging/$', LoggingChartView.as_view(), name='chart_logging'),
    url(r'^contract-farming/$', ContractFarmingChartView.as_view(), name='chart_contract_farming'),

    # PDF views for charts
    url(r'^intention\.pdf$', IntentionChartView.as_view(), {'format': 'PDF'}, name='chart_intention_pdf'),
    url(r'^negotiation-status\.pdf$', NegotiationStatusChartView.as_view(), {'format': 'PDF'},
        name='chart_negotiation_status_pdf'),
    url(r'^implementation-status\.pdf$', ImplementationStatusChartView.as_view(), {'format': 'PDF'},
        name='chart_implementation_status_pdf'),
    url(r'^intention-agriculture\.pdf$', IntentionAgricultureChartView.as_view(), {'format': 'PDF'},
        name='chart_intention_agriculture_pdf'),
    url(r'^transnational-deals\.pdf$', TransnationalDealsChartView.as_view(), {'format': 'PDF'},
        name='chart_transnational_deals_pdf'),
    url(r'^map-of-investments\.pdf$', MapOfInvestmentsChartView.as_view(), {'format': 'PDF'},
        name='chart_map_of_investments_pdf'),
    url(r'^perspective\.pdf$', PerspectiveChartView.as_view(), {'format': 'PDF'}, name='chart_perspective_pdf'),
    url(r'^agricultural-drivers\.pdf$', AgriculturalDriversChartView.as_view(), {'format': 'PDF'},
        name='chart_agricultural_drivers_pdf'),
    url(r'^produce-info\.pdf$', ProduceInfoChartView.as_view(), {'format': 'PDF'}, name='chart_produce_info_pdf'),
    url(r'^mining\.pdf$', MiningChartView.as_view(), {'format': 'PDF'}, name='chart_mining_pdf'),
    url(r'^logging\.pdf$', LoggingChartView.as_view(), {'format': 'PDF'}, name='chart_logging_pdf'),
    url(r'^contract-farming\.pdf$', ContractFarmingChartView.as_view(), {'format': 'PDF'},
        name='chart_contract_farming_pdf'),
]
