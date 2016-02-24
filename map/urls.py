from django.conf.urls import url, patterns
from django.views.decorators.cache import cache_page

from .views import *

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

CACHE_TIMEOUT = 24*3600

urlpatterns = patterns('map.views',
    url(r'^$', cache_page(CACHE_TIMEOUT)(MapView.as_view()), name='map'),
)