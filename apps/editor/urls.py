from django.urls import path

from . import views

urlpatterns = [
    path("", views.DashboardView.as_view(), name="editor"),
    path(
        "manage/feedback/", views.ManageFeedbackView.as_view(), name="manage_feedback"
    ),
    path("manage/my/", views.ManageForUserView.as_view(), name="manage_for_user"),
    path(
        "manage/pending_deletes/",
        views.ManageDeletesView.as_view(),
        name="manage_pending_deletes",
    ),
    path(
        "manage/pending_adds/",
        views.ManageAddsView.as_view(),
        name="manage_pending_adds",
    ),
    path(
        "manage/pending_updates/",
        views.ManageUpdatesView.as_view(),
        name="manage_pending_updates",
    ),
    path(
        "manage/rejected/", views.ManageRejectedView.as_view(), name="manage_rejected"
    ),
    path(
        "manage/deal/approve_change/<int:id>/",
        views.ApproveActivityChangeView.as_view(),
        name="manage_approve_change_deal",
    ),
    path(
        "manage/deal/reject_change/<int:id>/",
        views.RejectActivityChangeView.as_view(),
        name="manage_reject_change_deal",
    ),
    path(
        "manage/deal/approve_delete/<int:id>/",
        views.ApproveActivityDeleteView.as_view(),
        name="manage_approve_delete_deal",
    ),
    path(
        "manage/deal/reject_delete/<int:id>/",
        views.RejectActivityDeleteView.as_view(),
        name="manage_reject_delete_deal",
    ),
    path(
        "manage/investor/approve_change/<int:id>/",
        views.ApproveInvestorChangeView.as_view(),
        name="manage_approve_change_historicalinvestor",
    ),
    path(
        "manage/investor/reject_change/<int:id>/",
        views.RejectInvestorChangeView.as_view(),
        name="manage_reject_change_historicalinvestor",
    ),
    path(
        "manage/investor/approve_delete/<int:id>/",
        views.ApproveInvestorDeleteView.as_view(),
        name="manage_approve_delete_historicalinvestor",
    ),
    path(
        "manage/investor/reject_delete/<int:id>/",
        views.RejectInvestorDeleteView.as_view(),
        name="manage_reject_delete_historicalinvestor",
    ),
    path("manage/", views.ManageRootView.as_view(), name="manage"),
    path("log/latest_added/", views.LogAddedView.as_view(), name="log_added"),
    path("log/latest_modified/", views.LogModifiedView.as_view(), name="log_modified"),
    path("log/latest_deleted/", views.LogDeletedView.as_view(), name="log_deleted"),
    path(
        "log/",
        views.login_required(
            views.RedirectView.as_view(pattern_name="log_added", permanent=False)
        ),
        name="log",
    ),
]
