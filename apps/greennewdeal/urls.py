from django.urls import path, re_path

from apps.greennewdeal.views import (
    api_deal_list,
    api_deal_map,
    vuedeal,
)

urlpatterns = [
    path("api/deals/", api_deal_list),
    path("api/map/", api_deal_map),
    re_path(r"^(?P<path>.*)/$", vuedeal),
    path("", vuedeal),
]
