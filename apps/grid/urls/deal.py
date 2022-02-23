from django.urls import path

from apps.grid.views.base import not_avail
from apps.grid.views.deal import (
    DealDetailView,
    DealListView,
)
from apps.grid.views.export import ExportView


urlpatterns = [
    path("<int:deal_id>/", DealDetailView.as_view(), name="deal_detail"),
    path(
        "<int:deal_id>.pdf",
        DealDetailView.as_view(),
        {"format": "PDF"},
        name="deal_detail_pdf",
    ),
    path("<int:deal_id>.<suffix:format>/", ExportView.as_view(), name="export"),
    path(
        "<int:deal_id>/<int:history_id>/", DealDetailView.as_view(), name="deal_detail"
    ),
    path(
        "<int:deal_id>/<int:history_id>.pdf",
        DealDetailView.as_view(),
        {"format": "PDF"},
        name="deal_detail_pdf",
    ),
    path("edit/<int:deal_id>/", not_avail, name="change_deal"),
    path("edit/<int:deal_id>/<int:history_id>/", not_avail, name="change_deal"),
    path("add/", not_avail, name="add_deal"),
    path("delete/<int:deal_id>/", not_avail, name="delete_deal"),
    path("recover/<int:deal_id>/", not_avail, name="recover_deal"),
    path("", DealListView.as_view(), name="deals"),
]
