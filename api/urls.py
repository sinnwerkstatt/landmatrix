from api.views.json_view import JSONView

from django.conf.urls import include, url, patterns

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

urlpatterns = patterns('')

urlpatterns.append(
    url(r'^(?P<type>.*\.json)', JSONView.as_view(), name='landmatrix_api')
)

