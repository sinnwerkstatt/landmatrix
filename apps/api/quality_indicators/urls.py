from django.urls import path

from .views import counts, deals, investors, specs, stats

urlpatterns = [
    path("", specs, name="qi-specs"),
    path("count/", counts, name="qi-counts"),
    path("stats/", stats, name="qi-stats"),
    path("deal/", deals, name="qi-deals"),
    path("investor/", investors, name="qi-investors"),
]
