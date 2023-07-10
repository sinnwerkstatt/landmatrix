from django.urls import path

from .export import DataDownload
from .gis_export import gis_export
from .views import CaseStatistics, Management, messages_json, investor_search


def data_download(request):
    return DataDownload(request).get_response()


urlpatterns = [
    path("legacy_export/", data_download),
    path("newdeal_legacy/messages/", messages_json),
    path("gis_export/", gis_export),
    path("management/", Management.as_view()),
    path("case_statistics/", CaseStatistics.as_view()),
    path("investor_search/", investor_search),
]
