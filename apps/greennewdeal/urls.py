from django.urls import path, re_path

from apps.greennewdeal.views import vuebase

urlpatterns = [re_path(r"^(?P<path>.*)/$", vuebase), path("", vuebase)]
