from django.urls import path

from rest_framework import routers

from .views import deal_detail, deal_list

router = routers.DefaultRouter()

# router.register(r"deal", DealViewSet)

urlpatterns = [
    # path("rest/", include(router.urls)),
    path("deal/<int:id>/", deal_detail),
    path("deals/", deal_list),
]
