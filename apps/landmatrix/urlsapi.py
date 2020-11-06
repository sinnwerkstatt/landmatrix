from django.urls import path

from apps.landmatrix.export import DataDownload
from apps.landmatrix.views.greennewdeal import old_api_latest_changes


def data_download(request):
    return DataDownload(request).get_response()


urlpatterns = [
    path("test.xlsx", data_download),
    # path("deals.json", old_api_deals_json),
    # path("latest_changes.json", old_api_latest_changes),
    # path("country_deals.json", old_api_country_deals_json),
]
