from django.urls import path

from apps.greennewdeal.views import old_api_deals_json, old_api_country_deals_json

urlpatterns = [
    path("deals.json", old_api_deals_json),
    # path("country_deals.json", old_api_country_deals_json),
]
