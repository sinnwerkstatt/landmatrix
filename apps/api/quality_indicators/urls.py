from django.urls import path

from .views import deal_counts, deals, investor_counts, investors, specs, stats

urlpatterns = [
    path("", specs, name="qi-specs"),
    path("counts/deal/", deal_counts, name="qi-deal-counts"),
    path("counts/investor/", investor_counts, name="qi-investor-counts"),
    path("stats/", stats, name="qi-stats"),
    path("deal/", deals, name="qi-deals"),
    path("investor/", investors, name="qi-investors"),
]
