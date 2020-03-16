from django.urls import path, re_path

from apps.greennewdeal.views import vuedeal

urlpatterns = [re_path(r"^(?P<path>.*)/$", vuedeal), path("", vuedeal)]
