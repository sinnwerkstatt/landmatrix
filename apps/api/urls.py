from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.urls import include, path
from django.views.decorators.http import require_GET
from rest_framework import routers

from apps.landmatrix.views import (
    FieldDefinitionViewSet,
    CurrencyViewSet,
    CountryViewSet,
)

from .export import DataDownload
from .gis_export import gis_export
from .views import (
    CaseStatistics,
    Management,
    investor_search,
    messages_json,
    chart_descriptions,
    blog_categories,
)
from apps.accounts.views import UserViewSet


def data_download(request):
    return DataDownload(request).get_response()


@require_GET
def get_csrf(request):
    return JsonResponse({"token": get_token(request)})


router = routers.DefaultRouter()
router.register(r"field_definitions", FieldDefinitionViewSet)
router.register(r"currencies", CurrencyViewSet)
router.register(r"countries", CountryViewSet)
router.register(r"users", UserViewSet)

urlpatterns = [
    path("legacy_export/", data_download),
    path("newdeal_legacy/messages/", messages_json),
    path("gis_export/", gis_export),
    path("management/", Management.as_view()),
    path("case_statistics/", CaseStatistics.as_view()),
    path("investor_search/", investor_search),
    path("chart_descriptions/", chart_descriptions),
    path("blog_categories/", blog_categories),
    path("csrf_token/", get_csrf),
    path("", include("apps.new_model.urls")),
    path("", include(router.urls)),
]
