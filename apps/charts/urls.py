from django.urls import path

from . import views

urlpatterns = [
    path("", views.ChartRedirectView.as_view(), name="charts"),
    # re_path(r'^all(?P<type>\.csv)?/$', #     ChartView.as_view(), name='all_charts'),
    path("intention/", views.IntentionChartView.as_view(), name="chart_intention"),
    path(
        "negotiation-status/",
        views.NegotiationStatusChartView.as_view(),
        name="chart_negotiation_status",
    ),
    path(
        "implementation-status/",
        views.ImplementationStatusChartView.as_view(),
        name="chart_implementation_status",
    ),
    path(
        "intention-agriculture/",
        views.IntentionAgricultureChartView.as_view(),
        name="chart_intention_agriculture",
    ),
    path(
        "web-of-transnational-deals/",
        views.TransnationalDealsChartView.as_view(),
        name="chart_transnational_deals",
    ),
    path(
        "map-of-investments/",
        views.MapOfInvestmentsChartView.as_view(),
        name="chart_map_of_investments",
    ),
    path(
        "perspective/", views.PerspectiveChartView.as_view(), name="chart_perspective"
    ),
    path(
        "agricultural-drivers/",
        views.AgriculturalDriversChartView.as_view(),
        name="chart_agricultural_drivers",
    ),
    path(
        "produce-info/", views.ProduceInfoChartView.as_view(), name="chart_produce_info"
    ),
    path("mining/", views.MiningChartView.as_view(), name="chart_mining"),
    path("logging/", views.LoggingChartView.as_view(), name="chart_logging"),
    path(
        "contract-farming/",
        views.ContractFarmingChartView.as_view(),
        name="chart_contract_farming",
    ),
    # PDF views for charts
    path(
        "intention.pdf",
        views.IntentionChartView.as_view(),
        {"format": "PDF"},
        name="chart_intention_pdf",
    ),
    path(
        "negotiation-status.pdf",
        views.NegotiationStatusChartView.as_view(),
        {"format": "PDF"},
        name="chart_negotiation_status_pdf",
    ),
    path(
        "implementation-status.pdf",
        views.ImplementationStatusChartView.as_view(),
        {"format": "PDF"},
        name="chart_implementation_status_pdf",
    ),
    path(
        "intention-agriculture.pdf",
        views.IntentionAgricultureChartView.as_view(),
        {"format": "PDF"},
        name="chart_intention_agriculture_pdf",
    ),
    path(
        "transnational-deals.pdf",
        views.TransnationalDealsChartView.as_view(),
        {"format": "PDF"},
        name="chart_transnational_deals_pdf",
    ),
    path(
        "map-of-investments.pdf",
        views.MapOfInvestmentsChartView.as_view(),
        {"format": "PDF"},
        name="chart_map_of_investments_pdf",
    ),
    path(
        "perspective.pdf",
        views.PerspectiveChartView.as_view(),
        {"format": "PDF"},
        name="chart_perspective_pdf",
    ),
    path(
        "agricultural-drivers.pdf",
        views.AgriculturalDriversChartView.as_view(),
        {"format": "PDF"},
        name="chart_agricultural_drivers_pdf",
    ),
    path(
        "produce-info.pdf",
        views.ProduceInfoChartView.as_view(),
        {"format": "PDF"},
        name="chart_produce_info_pdf",
    ),
    path(
        "mining.pdf",
        views.MiningChartView.as_view(),
        {"format": "PDF"},
        name="chart_mining_pdf",
    ),
    path(
        "logging.pdf",
        views.LoggingChartView.as_view(),
        {"format": "PDF"},
        name="chart_logging_pdf",
    ),
    path(
        "contract-farming.pdf",
        views.ContractFarmingChartView.as_view(),
        {"format": "PDF"},
        name="chart_contract_farming_pdf",
    ),
]
