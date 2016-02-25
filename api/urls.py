from api.views.json_view import JSONView

from django.conf.urls import include, url, patterns
from django.views.decorators.cache import cache_page

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

CACHE_TIMEOUT = 24*3600

urlpatterns = patterns('')

urlpatterns.append(
    url(r'^(?P<type>.*\.json)', cache_page(CACHE_TIMEOUT)(JSONView.as_view()), name='landmatrix_api')
)

