__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django.conf.urls import include, url
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'involvement', views.InvolvementViewSet)
router.register(r'activity', views.ActivityViewSet)
router.register(r'stakeholder', views.StakeholderViewSet)
router.register(r'primary_investors', views.PrimaryInvestorViewSet)
router.register(r'status', views.StatusViewSet)
router.register(r'statistics', views.stats, base_name='statistics')
print(router.__dict__)
urlpatterns = [
    url(r'^', include(router.urls))
]
