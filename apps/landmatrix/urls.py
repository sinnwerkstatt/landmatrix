from django.urls import path, re_path

from apps.landmatrix.views.greennewdeal import vuebase

urlpatterns = [re_path(r"^(?P<path>.*)/$", vuebase), path("", vuebase)]
