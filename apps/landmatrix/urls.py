from django.urls import re_path, path

from apps.landmatrix.views.greennewdeal import vuebase, gis_export

urlpatterns = [
    re_path(r"^(?P<path>.*)/$", vuebase),
    path("data.geojson", gis_export),
    path("", vuebase),
]
