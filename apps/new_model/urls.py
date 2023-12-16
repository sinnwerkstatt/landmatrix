from django.urls import path, include

from rest_framework import routers

from .views import Deal2ViewSet, Investor2ViewSet, field_choices, DealVersionViewSet

router = routers.DefaultRouter()

router.register(r"deals", Deal2ViewSet)
router.register(r"dealversions", DealVersionViewSet)
router.register(r"investors", Investor2ViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("field_choices/", field_choices),
    # path("deal/<int:id>/", deal_detail),
    # path("deals/", deal_list),
]
