from django.urls import path

from apps.editor.views import *

urlpatterns = [
    path("", DashboardView.as_view(), name="editor"),
    path("manage/feedback/", ManageFeedbackView.as_view(), name="manage_feedback"),
    path("manage/my/", ManageForUserView.as_view(), name="manage_for_user"),
    path(
        "manage/pending_deletes/",
        ManageDeletesView.as_view(),
        name="manage_pending_deletes",
    ),
    path("manage/pending_adds/", ManageAddsView.as_view(), name="manage_pending_adds"),
    path(
        "manage/pending_updates/",
        ManageUpdatesView.as_view(),
        name="manage_pending_updates",
    ),
    path("manage/rejected/", ManageRejectedView.as_view(), name="manage_rejected"),
    path(
        "manage/deal/approve_change/<int:id>/",
        ApproveActivityChangeView.as_view(),
        name="manage_approve_change_deal",
    ),
    path(
        "manage/deal/reject_change/<int:id>/",
        RejectActivityChangeView.as_view(),
        name="manage_reject_change_deal",
    ),
    path(
        "manage/deal/approve_delete/<int:id>/",
        ApproveActivityDeleteView.as_view(),
        name="manage_approve_delete_deal",
    ),
    path(
        "manage/deal/reject_delete/<int:id>/",
        RejectActivityDeleteView.as_view(),
        name="manage_reject_delete_deal",
    ),
    path(
        "manage/investor/approve_change/<int:id>/",
        ApproveInvestorChangeView.as_view(),
        name="manage_approve_change_investor",
    ),
    path(
        "manage/investor/reject_change/<int:id>/",
        RejectInvestorChangeView.as_view(),
        name="manage_reject_change_investor",
    ),
    path(
        "manage/investor/approve_delete/<int:id>/",
        ApproveInvestorDeleteView.as_view(),
        name="manage_approve_delete_investor",
    ),
    path(
        "manage/investor/reject_delete/<int:id>/",
        RejectInvestorDeleteView.as_view(),
        name="manage_reject_delete_investor",
    ),
    path("manage/", ManageRootView.as_view(), name="manage"),
    path("log/latest_added/", LogAddedView.as_view(), name="log_added"),
    path("log/latest_modified/", LogModifiedView.as_view(), name="log_modified"),
    path("log/latest_deleted/", LogDeletedView.as_view(), name="log_deleted"),
    path(
        "log/",
        login_required(RedirectView.as_view(pattern_name="log_added", permanent=False)),
        name="log",
    ),
]
