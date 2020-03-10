from django.urls import path

from apps.greennewdeal.views import deal_detail, api_deal_map, api_deal_detail

urlpatterns = [
    path("<int:deal_id>/", deal_detail),
    path("<int:deal_id>.pdf", deal_detail, {"format": "PDF"}),
    path("api/map", api_deal_map),
    path("api/deal/<int:deal_id>/", api_deal_detail),
]
