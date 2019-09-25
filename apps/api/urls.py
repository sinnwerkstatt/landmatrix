from django.urls import path
from django.urls.converters import StringConverter, register_converter
from rest_framework_swagger.views import get_swagger_view

from apps.api.views import *
from apps.api.views.list_views import PolygonGeomView

schema_view = get_swagger_view(title="Land Matrix API")


class DealInvestorMatch(StringConverter):
    regex = "deal|investor"


register_converter(DealInvestorMatch, "di")

urlpatterns = [
    path(
        "agricultural-produce.json",
        AgriculturalProduceListView.as_view(),
        name="agricultural_produce_api",
    ),
    path(
        "contract-farming.json",
        ContractFarmingView.as_view(),
        name="contract_farming_api",
    ),
    path("countries-geom.json", CountryGeomView.as_view(), name="countries_geom_api"),
    path(
        "target-countries.json",
        TargetCountryListView.as_view(),
        name="target_countries_api",
    ),
    path("countries.json", CountryListView.as_view(), name="countries_api"),
    path("country_deals.json", CountryDealsView.as_view(), name="country_deals_api"),
    path("deals.json", GlobalDealsView.as_view(), name="deals_api"),
    path(
        "filter/<di:doc_type>/add/default/",
        SetDefaultFiltersView.as_view(),
        name="api_filter_set_default_filters",
    ),
    path(
        "filter/<di:doc_type>/add/",
        FilterCreateView.as_view(),
        name="api_filter_create",
    ),
    path(
        "filter/<di:doc_type>/delete/",
        FilterDeleteView.as_view(),
        name="api_filter_delete",
    ),
    path(
        "filter/<di:doc_type>/clear/",
        FilterClearView.as_view(),
        name="api_filter_clear",
    ),
    path("filter/<di:doc_type>/", FilterListView.as_view(), name="api_filter_list"),
    path(
        "filter_preset/<di:doc_type>/",
        FilterPresetView.as_view(),
        name="api_filter_preset",
    ),
    path("hectares.json", HectaresView.as_view(), name="hectares_api"),
    path(
        "implementation_status.json",
        ImplementationStatusListView.as_view(),
        name="implementation_status_api",
    ),
    path("intention.json", InvestmentIntentionListView.as_view(), name="intention"),
    path(
        "investor_countries_for_target_country.json",
        InvestorCountriesForTargetCountryView.as_view(),
        name="investor_countries_for_target_country_api",
    ),
    path(
        "investor_country_summaries.json",
        InvestorCountrySummaryView.as_view(),
        name="investor_country_summaries_api",
    ),
    path(
        "investor_network.json",
        InvestorNetworkView.as_view(),
        name="api_investor_network",
    ),
    path("investors.json", InvestorListView.as_view(), name="investors_api"),
    path("logging.json", LoggingView.as_view(), name="logging_api"),
    path(
        "negotiation_status.json",
        NegotiationStatusListView.as_view(),
        name="negotiation_status_api",
    ),
    path(
        "polygons/<polygon_field>.json",
        PolygonGeomView.as_view(),
        name="polygon_geom_api",
    ),
    path("produce-info.json", ProduceInfoView.as_view(), name="produce_info_api"),
    path(
        "transnational_deals.json",
        TransnationalDealListView.as_view(),
        name="transnational_deals_api",
    ),
    path(
        "top-10-countries.json",
        Top10CountriesView.as_view(),
        name="top_10_countries_api",
    ),
    path(
        "transnational_deals_by_country.json",
        TransnationalDealsByCountryView.as_view(),
        name="transnational_deals_by_country_api",
    ),
    path(
        "target_country_summaries.json",
        TargetCountrySummaryView.as_view(),
        name="target_country_summaries_api",
    ),
    path(
        "target_countries_for_investor_country.json",
        TargetCountrySummaryView.as_view(),
        name="target_countries_for_investor_country_api",
    ),
    path("users.json", UserListView.as_view(), name="users_api"),
    path("regions.json", RegionListView.as_view(), name="regions_api"),
    path(
        "resource-extraction.json",
        ResourceExtractionView.as_view(),
        name="resource_extraction_api",
    ),
    path("statistics.json", StatisticsView.as_view(), name="statistics_api"),
    path("latest_changes.json", LatestChangesView.as_view(), name="latest_changes_api"),
    path("", schema_view),
]
