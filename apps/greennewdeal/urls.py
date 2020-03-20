from django.urls import path, re_path
from django.views.generic import TemplateView

view = TemplateView.as_view(template_name="greennewdeal/vuebase.html")

urlpatterns = [re_path(r"^(?P<path>.*)/$", view), path("", view)]
