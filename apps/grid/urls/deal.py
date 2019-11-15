from django.urls import path

from apps.feeds.views import ActivityChangesFeed
from apps.grid.views.deal import (
    DealCreateView,
    DealDeleteView,
    DealDetailView,
    DealListView,
    DealRecoverView,
    DealUpdateView,
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
    path("<int:deal_id>/changes.rss", ActivityChangesFeed(), name="deal_changes_feed"),
    path(
        "<int:deal_id>/<int:history_id>/", DealDetailView.as_view(), name="deal_detail"
    ),
    path(
        "<int:deal_id>/<int:history_id>.pdf",
        DealDetailView.as_view(),
        {"format": "PDF"},
        name="deal_detail_pdf",
    ),
    path("edit/<int:deal_id>/", DealUpdateView.as_view(), name="change_deal"),
    path(
        "edit/<int:deal_id>/<int:history_id>/",
        DealUpdateView.as_view(),
        name="change_deal",
    ),
    path("add/", DealCreateView.as_view(), name="add_deal"),
    path("delete/<int:deal_id>/", DealDeleteView.as_view(), name="delete_deal"),
    path("recover/<int:deal_id>/", DealRecoverView.as_view(), name="recover_deal"),
    path("", DealListView.as_view(), name="deals"),
]
