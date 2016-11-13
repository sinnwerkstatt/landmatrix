from django.conf.urls import url, patterns

from api.decorators import save_filter_query_params

from .views import *



urlpatterns = patterns('map.views',
    url(r'^$', save_filter_query_params()(MapView.as_view()), name='map'),
)