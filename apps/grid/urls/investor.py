from django.urls import re_path, path

from apps.grid.views.base import not_avail
from apps.grid.views.investor import InvestorDetailView

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
    path("add/", not_avail, name="investor_add"),
    path("delete/<int:investor_id>/", not_avail, name="investor_delete"),
    path("recover/<int:investor_id>/", not_avail, name="investor_recover"),
    path("edit/<int:investor_id>/", not_avail, name="investor_update"),
    path("edit/<int:investor_id>/<int:history_id>/", not_avail, name="investor_update"),
]
