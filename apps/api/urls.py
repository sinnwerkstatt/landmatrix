from drf_spectacular.views import (
    SpectacularJSONAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
    SpectacularYAMLAPIView,
)

from django.urls import include, path
from django.views.generic import RedirectView
from rest_framework import routers

import apps.landmatrix.views.management as management_views
from apps.accounts import views as user_views
from apps.api import views as api_views
from apps.landmatrix import views as oldviews
from apps.landmatrix.views import newviews
from apps.message.views import MessageViewSet

from ..blog.views import BlogCategoryViewSet, BlogPageViewSet
from .export import DataDownload
from .gis_export import gis_export_areas, gis_export_locations
from .upload_view import upload_datasource_file


def data_download(request):
    return DataDownload(request).get_response()


router = routers.DefaultRouter()
router.register(r"users", user_views.UserViewSet)
router.register(r"currencies", oldviews.CurrencyViewSet)
router.register(r"countries", oldviews.CountryViewSet)
router.register(r"regions", oldviews.RegionViewSet)
router.register(r"field_definitions", oldviews.FieldDefinitionViewSet)
router.register(r"deals", newviews.DealViewSet)
router.register(r"dealversions", newviews.DealVersionViewSet)
router.register(r"investors", newviews.InvestorViewSet)
router.register(r"investorversions", newviews.InvestorVersionViewSet)
router.register(r"messages", MessageViewSet)
router.register(r"blog_categories", BlogCategoryViewSet)
router.register(r"blog_pages", BlogPageViewSet)

urlpatterns = [
    path("schema.yaml", SpectacularYAMLAPIView.as_view(), name="schema.yaml"),
    path("schema.json", SpectacularJSONAPIView.as_view(), name="schema.json"),
    path("schema/", RedirectView.as_view(url="/api/schema.yaml")),
    path(
        "schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema.yaml"),
        name="swagger-ui",
    ),
    path(
        "schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema.yaml"),
        name="redoc",
    ),
    # account/user
    path("user/", include("apps.accounts.urls")),
    # base data
    path("chart_descriptions/", api_views.chart_descriptions),
    # path("blog_categories/", api_views.blog_categories),
    path("field_choices/", newviews.FieldChoicesView.as_view()),
    # misc
    path("csrf_token/", api_views.get_csrf),
    path("upload_datasource_file/", upload_datasource_file),
    path(
        "workflow_info/<str:wfitype>/<int:pk>/add_reply/",
        api_views.workflow_info_add_reply,
    ),
    path(
        "workflow_info/<str:wfitype>/<int:pk>/resolve/",
        api_views.workflow_info_resolve,
    ),
    path("legacy_export/", data_download),
    path("gis_export/locations/", gis_export_locations),
    path("gis_export/areas/", gis_export_areas),
    # management / case
    path("management/", management_views.Management.as_view()),
    path("case_statistics/", management_views.CaseStatistics.as_view()),
    # special stuff
    path("quick_search/", api_views.quick_search),
    path("investor_search/", api_views.investor_search),
    # charts
    path(
        "charts/country_investments_and_rankings/",
        api_views.country_investments_and_rankings,
    ),
    path("charts/deal_aggregations/", api_views.deal_aggregations),
    path(
        "charts/web_of_transnational_deals/", api_views.get_web_of_transnational_deals
    ),
    path("charts/global_map_of_investments/", api_views.global_map_of_investments),
    # DRF
    path("", include(router.urls)),
]
