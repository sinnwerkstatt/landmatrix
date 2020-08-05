from django.conf import settings
from django.urls import path

from apps.landmatrix.views.greennewdeal import vuebase

urlpatterns = []
if settings.GND_ENABLED:
    urlpatterns += [
        # re_path(r"^(?P<path>.*)/$", vuebase), path("", vuebase),
        path("deal/<int:deal_id>/", vuebase, name="deal_detail"),
        path("deal/<int:deal_id>/<int:history_id>/", vuebase, name="deal_detail"),
    ]
