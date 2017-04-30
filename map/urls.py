from django.conf.urls import url

from api.decorators import save_filter_query_params

from .views import *


urlpatterns = [
    url(r'^$', save_filter_query_params()(MapView.as_view()), name='map'),
]