from django.urls import path

from .views import *

urlpatterns = [
    path("", ChartRedirectView.as_view(), name="charts"),
    # re_path(r'^all(?P<type>\.csv)?/$', #     ChartView.as_view(), name='all_charts'),
    path("intention/", IntentionChartView.as_view(), name="chart_intention"),
    path(
        "negotiation-status/",
        NegotiationStatusChartView.as_view(),
        name="chart_negotiation_status",
    ),
    path(
        "implementation-status/",
        ImplementationStatusChartView.as_view(),
        name="chart_implementation_status",
    ),
    path(
        "intention-agriculture/",
        IntentionAgricultureChartView.as_view(),
        name="chart_intention_agriculture",
    ),
    path(
        "web-of-transnational-deals/",
        TransnationalDealsChartView.as_view(),
        name="chart_transnational_deals",
    ),
    path(
        "map-of-investments/",
        MapOfInvestmentsChartView.as_view(),
        name="chart_map_of_investments",
    ),
    path("perspective/", PerspectiveChartView.as_view(), name="chart_perspective"),
    path(
        "agricultural-drivers/",
        AgriculturalDriversChartView.as_view(),
        name="chart_agricultural_drivers",
    ),
    path("produce-info/", ProduceInfoChartView.as_view(), name="chart_produce_info"),
    path("mining/", MiningChartView.as_view(), name="chart_mining"),
    path("logging/", LoggingChartView.as_view(), name="chart_logging"),
    path(
        "contract-farming/",
        ContractFarmingChartView.as_view(),
        name="chart_contract_farming",
    ),
    # PDF views for charts
    path(
        "intention.pdf",
        IntentionChartView.as_view(),
        {"format": "PDF"},
        name="chart_intention_pdf",
    ),
    path(
        "negotiation-status.pdf",
        NegotiationStatusChartView.as_view(),
        {"format": "PDF"},
        name="chart_negotiation_status_pdf",
    ),
    path(
        "implementation-status.pdf",
        ImplementationStatusChartView.as_view(),
        {"format": "PDF"},
        name="chart_implementation_status_pdf",
    ),
    path(
        "intention-agriculture.pdf",
        IntentionAgricultureChartView.as_view(),
        {"format": "PDF"},
        name="chart_intention_agriculture_pdf",
    ),
    path(
        "transnational-deals.pdf",
        TransnationalDealsChartView.as_view(),
        {"format": "PDF"},
        name="chart_transnational_deals_pdf",
    ),
    path(
        "map-of-investments.pdf",
        MapOfInvestmentsChartView.as_view(),
        {"format": "PDF"},
        name="chart_map_of_investments_pdf",
    ),
    path(
        "perspective.pdf",
        PerspectiveChartView.as_view(),
        {"format": "PDF"},
        name="chart_perspective_pdf",
    ),
    path(
        "agricultural-drivers.pdf",
        AgriculturalDriversChartView.as_view(),
        {"format": "PDF"},
        name="chart_agricultural_drivers_pdf",
    ),
    path(
        "produce-info.pdf",
        ProduceInfoChartView.as_view(),
        {"format": "PDF"},
        name="chart_produce_info_pdf",
    ),
    path(
        "mining.pdf",
        MiningChartView.as_view(),
        {"format": "PDF"},
        name="chart_mining_pdf",
    ),
    path(
        "logging.pdf",
        LoggingChartView.as_view(),
        {"format": "PDF"},
        name="chart_logging_pdf",
    ),
    path(
        "contract-farming.pdf",
        ContractFarmingChartView.as_view(),
        {"format": "PDF"},
        name="chart_contract_farming_pdf",
    ),
]
