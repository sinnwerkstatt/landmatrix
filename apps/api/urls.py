from django.urls import include, path
from rest_framework import routers

import apps.landmatrix.views.management as management_views
from apps.accounts import views as user_views
from apps.api import views as api_views
from apps.landmatrix.views import newviews
from apps.landmatrix import views as oldviews
from apps.message.views import MessageViewSet
from .export import DataDownload
from .gis_export import gis_export
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

urlpatterns = [
    # account/user
    path("user/register/", user_views.register),
    path("user/register_confirm/", user_views.register_confirm),
    path("user/login/", user_views.login),
    path("user/logout/", user_views.logout),
    path("user/password_reset/", user_views.password_reset),
    path("user/password_reset_confirm/", user_views.password_reset_confirm),
    # base data
    path("chart_descriptions/", api_views.chart_descriptions),
    path("blog_categories/", api_views.blog_categories),
    path("blog_pages/", api_views.blog_pages),
    path("legacy_formfields/", api_views.legacy_formfields),
    path("field_choices/", newviews.field_choices),
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
    path("gis_export/", gis_export),
    # management / case
    path("management/", management_views.Management.as_view()),
    path("case_statistics/", management_views.CaseStatistics.as_view()),
    # special stuff
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
