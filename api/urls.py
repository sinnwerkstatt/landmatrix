__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django.conf.urls import include, url
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'involvement', views.InvolvementViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]
