from django.urls import path, include

from rest_framework import routers

from .views import Deal2ViewSet, Investor2ViewSet

router = routers.DefaultRouter()

router.register(r"deals", Deal2ViewSet)
router.register(r"investors", Investor2ViewSet)

urlpatterns = [
    path("", include(router.urls)),
    # path("deal/<int:id>/", deal_detail),
    # path("deals/", deal_list),
]
