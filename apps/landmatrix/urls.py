from django.urls import re_path, path

from apps.landmatrix.views.greennewdeal import vuebase

urlpatterns = [
    re_path(r"^(?P<path>.*)/$", vuebase),
    path("", vuebase),
]
