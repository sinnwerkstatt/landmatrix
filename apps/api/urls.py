from django.urls import include, path
from rest_framework import routers

from apps.accounts.views import UserViewSet
from apps.api import views as api_views
from apps.landmatrix import newviews
from apps.landmatrix import views as oldviews
from .export import DataDownload
from .gis_export import gis_export


def data_download(request):
    return DataDownload(request).get_response()


router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"currencies", oldviews.CurrencyViewSet)
router.register(r"countries", oldviews.CountryViewSet)
router.register(r"regions", oldviews.RegionViewSet)
router.register(r"field_definitions", oldviews.FieldDefinitionViewSet)
router.register(r"deals", newviews.Deal2ViewSet)
router.register(r"dealversions", newviews.DealVersionViewSet)
router.register(r"investors", newviews.Investor2ViewSet)
router.register(r"investorversions", newviews.InvestorVersionViewSet)

urlpatterns = [
    path("legacy_export/", data_download),
    path("newdeal_legacy/messages/", api_views.messages_json),
    path("gis_export/", gis_export),
    path("management/", api_views.Management.as_view()),
    path("case_statistics/", api_views.CaseStatistics.as_view()),
    path("investor_search/", api_views.investor_search),
    path("chart_descriptions/", api_views.chart_descriptions),
    path("blog_categories/", api_views.blog_categories),
    path("blog_pages/", api_views.blog_pages),
    path("legacy_formfields/", api_views.legacy_formfields),
    path("csrf_token/", api_views.get_csrf),
    path("field_choices/", newviews.field_choices),
    path("", include(router.urls)),
]
