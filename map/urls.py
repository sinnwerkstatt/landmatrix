from django.conf.urls import url, patterns
from django.views.decorators.cache import cache_page

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

CACHE_TIMEOUT = 24*3600

urlpatterns = patterns('map.views',
    url(r'^global/map/$', cache_page(CACHE_TIMEOUT)(MapView.as_view()), name='map'),
}