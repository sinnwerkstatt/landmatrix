__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django.conf.urls import include, url, patterns
from api.api import *
from tastypie.api import Api

from api.views import JSONView

urlpatterns = patterns('')


api = Api(api_name='')
for klass in filter(lambda c: c.__module__.startswith('api.'), ModelResource.__subclasses__()):
    api.register(klass())

urlpatterns.append(
    url(r'^(?P<type>.*\.json)', JSONView.as_view(), name='landmatrix_api')
)
urlpatterns.append(url(r'^api', include(api.urls)))

