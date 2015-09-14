from api.views.json_view import JSONView
from api.api import *

from django.conf.urls import include, url, patterns
from tastypie.api import Api

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

urlpatterns = patterns('')

api = Api(api_name='')
for klass in filter(lambda c: c.__module__.startswith('api.'), ModelResource.__subclasses__()):
    api.register(klass())

urlpatterns.append(
    url(r'^(?P<type>.*\.json)', JSONView.as_view(), name='landmatrix_api')
)
urlpatterns.append(url(r'^api', include(api.urls)))

