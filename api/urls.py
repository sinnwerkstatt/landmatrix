__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django.conf.urls import include, url, patterns
from api.api import *
from tastypie.api import Api

from rest_framework import routers
from api import views

USE_TASTY = True
USE_REST = True

urlpatterns = patterns('')

if USE_TASTY:

    api = Api(api_name='')
    for klass in filter(lambda c: c.__module__.startswith('api.'), ModelResource.__subclasses__()):
        api.register(klass())

    urlpatterns.append(
        url(r'^(?P<type>.*\.json)', views.stats, name='landmatrix_api')
    )
    urlpatterns.append(url(r'^api', include(api.urls)))

if USE_REST:

    router = routers.DefaultRouter()
    router.register(r'involvement', views.InvolvementViewSet)
    router.register(r'activity', views.ActivityViewSet)
    router.register(r'stakeholder', views.StakeholderViewSet)
    router.register(r'primary_investor', views.PrimaryInvestorViewSet)
    router.register(r'status', views.StatusViewSet)
    router.register(r'activity_attribute_group', views.ActivityAttributeGroupViewSet)
    router.register(r'statistics', views.stats, base_name='statistics')

    urlpatterns.append(
        url(r'^(?P<type>.*\.json)', views.stats, name='landmatrix_api')
    )

    urlpatterns.append(url(r'^', include(router.urls)))

