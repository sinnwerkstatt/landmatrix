from django.urls import path

from apps.landmatrix.export import DataDownload
from apps.message.views import messages_json


def data_download(request):
    return DataDownload(request).get_response()


urlpatterns = [
    path("legacy_export/", data_download),
    path("newdeal_legacy/messages/", messages_json),
    # path("deals.json", old_api_deals_json),
    # path("latest_changes.json", old_api_latest_changes),
    # path("country_deals.json", old_api_country_deals_json),
]
