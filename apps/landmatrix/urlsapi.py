from django.urls import path

from apps.landmatrix.export import DataDownload
from apps.landmatrix.views.greennewdeal import gis_export
from apps.message.views import messages_json


def data_download(request):
    return DataDownload(request).get_response()


urlpatterns = [
    path("legacy_export/", data_download),
    path("newdeal_legacy/messages/", messages_json),
    path("data.geojson", gis_export),
]
