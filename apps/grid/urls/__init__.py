from django.urls import path
from django.urls.converters import StringConverter, register_converter

from apps.grid.views.deal import DealListView
from apps.grid.views.export import ExportView
from apps.grid.views.investor import InvestorListView

CACHE_TIMEOUT = 24 * 3600


class FilenameSuffixMatch(StringConverter):
    regex = "csv|xml|xls"


register_converter(FilenameSuffixMatch, "suffix")

urlpatterns = [
    # please leave them here, commented out, for quick cache de-/activation when developing
    # path('', DealsView.as_view(), name='app_main'),
    # path('<group>/<list>/', DealListView.as_view(), name='deal_list'),
    path("", DealListView.as_view(), name="data"),
    path("all.<suffix:format>/", ExportView.as_view(), name="export"),
    path("<group>/<group_value>.<suffix:format>/", ExportView.as_view(), name="export"),
    path("<group>.<suffix:format>/", ExportView.as_view(), name="export"),
    path("investors/", InvestorListView.as_view(), name="investor_list"),
    path(
        "investors/<group>/<group_value>/",
        InvestorListView.as_view(),
        name="investor_list",
    ),
    path("investors/<group>/", InvestorListView.as_view(), name="investor_list"),
    # needs to come last, regexp catches all expressions
    path("<group>/<group_value>/", DealListView.as_view(), name="deal_list"),
    path("<group>/", DealListView.as_view(), name="deal_list"),
]
