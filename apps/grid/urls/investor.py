from django.urls import path, re_path

from apps.grid.views.investor import (
    DeleteInvestorView,
    InvestorCreateView,
    InvestorDetailView,
    InvestorUpdateView,
    RecoverInvestorView,
)

urlpatterns = [
    # dont' just refactor these two without checking apps.grids.views.investor.InvestorUpdateView.dispatch()
    # it's quite the ugly code.
    re_path(
        r"^(?P<investor_id>\d*)/$", InvestorDetailView.as_view(), name="investor_detail"
    ),
    re_path(
        r"^(?P<investor_id>\d*)/(?P<history_id>\d+)/$",
        InvestorDetailView.as_view(),
        name="investor_detail",
    ),
    path("add/", InvestorCreateView.as_view(), name="investor_add"),
    path(
        "delete/<int:investor_id>/",
        DeleteInvestorView.as_view(),
        name="investor_delete",
    ),
    path(
        "recover/<int:investor_id>/",
        RecoverInvestorView.as_view(),
        name="investor_recover",
    ),
    path(
        "edit/<int:investor_id>/", InvestorUpdateView.as_view(), name="investor_update"
    ),
    path(
        "edit/<int:investor_id>/<int:history_id>/",
        InvestorUpdateView.as_view(),
        name="investor_update",
    ),
]
