from django.urls import path

from .export import DataDownload
from .views import gis_export, messages_json, Management, CaseStatistics


def data_download(request):
    return DataDownload(request).get_response()


urlpatterns = [
    path("legacy_export/", data_download),
    path("newdeal_legacy/messages/", messages_json),
    path("data.geojson", gis_export),
    path("management/", Management.as_view()),
    path("case_statistics/", CaseStatistics.as_view()),
]
