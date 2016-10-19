from django.conf.urls import url, patterns

from api.decorators import save_filter_query_params

from .views import *

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


urlpatterns = patterns('map.views',
    url(r'^$', save_filter_query_params()(MapView.as_view()), name='map'),
)