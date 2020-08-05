import re

from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import path

from apps.grid.views.deal import DealDetailView
from apps.grid.views.investor import InvestorDetailView
from apps.landmatrix.views.greennewdeal import vuebase

oldroutes = [
    (r"/deal/(?P<deal_id>\d*)/$", DealDetailView.as_view()),
    (r"/deal/(?P<deal_id>\d*)/(?P<history_id>\d+)/$", DealDetailView.as_view()),
    (r"/investor/(?P<investor_id>\d*)/$", InvestorDetailView.as_view()),
    (
        r"/investor/(?P<investor_id>\d*)/(?P<history_id>\d+)/$",
        InvestorDetailView.as_view(),
    ),
]


def gnd_switch(request, *args, **kwargs):
    gnd_toggle = request.COOKIES.get("gnd_toggle") or "off"

    if gnd_toggle == "on":
        return vuebase(request)
    else:
        print(request.path)
        for route, target in oldroutes:
            if re.match(route, request.path):
                return target(request, *args, **kwargs)


def toggle_gnd(request):
    gnd_toggle = request.COOKIES.get("gnd_toggle") or "off"
    response = HttpResponseRedirect(redirect_to=request.GET.get("next") or "/")
    response.set_cookie("gnd_toggle", "on" if gnd_toggle == "off" else "off")
    return response


urlpatterns = [
    path("toggle_gnd/", toggle_gnd),
    # re_path(r"^(?P<path>.*)/$", vuebase), path("", vuebase),
    path("deal/<int:deal_id>/", gnd_switch, name="deal_detail"),
    path("deal/<int:deal_id>/<int:history_id>/", gnd_switch, name="deal_detail"),
    path("investor/<int:investor_id>/", gnd_switch, name="investor_detail"),
    path(
        "investor/<int:investor_id>/<int:history_id>/",
        gnd_switch,
        name="investor_detail",
    ),
]
