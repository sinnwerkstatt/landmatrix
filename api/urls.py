__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django.conf.urls import include, url, patterns
from api.api import *
from tastypie.api import Api

from rest_framework import routers
from api.views import JSONView, InvolvementViewSet, ActivityViewSet, StakeholderViewSet, PrimaryInvestorViewSet, \
    StatusViewSet, ActivityAttributeGroupViewSet, stats

USE_TASTY = True
USE_REST = True

urlpatterns = patterns('')

if USE_TASTY:

    api = Api(api_name='')
    for klass in filter(lambda c: c.__module__.startswith('api.'), ModelResource.__subclasses__()):
        api.register(klass())

    urlpatterns.append(
        url(r'^(?P<type>.*\.json)', JSONView.as_view(), name='landmatrix_api')
    )
    urlpatterns.append(url(r'^api', include(api.urls)))

if USE_REST:

    router = routers.DefaultRouter()
    router.register(r'involvement', InvolvementViewSet)
    router.register(r'activity', ActivityViewSet)
    router.register(r'stakeholder', StakeholderViewSet)
    router.register(r'primary_investor', PrimaryInvestorViewSet)
    router.register(r'status', StatusViewSet)
    router.register(r'activity_attribute_group', ActivityAttributeGroupViewSet)
    router.register(r'statistics', stats, base_name='statistics')

    urlpatterns.append(
        url(r'^(?P<type>.*\.json)', JSONView.as_view(), name='landmatrix_api')
    )

    urlpatterns.append(url(r'^', include(router.urls)))

