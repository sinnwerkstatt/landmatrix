from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView

from grid.views.activity_protocol import ActivityQuerySet
from api.query_sets.latest_changes_query_set import LatestChangesQuerySet
from api.query_sets.statistics_query_set import StatisticsQuerySet
from api.serializers import UserSerializer
from api.views.base import FakeQuerySetListView


__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'
User = get_user_model()


class UserListView(ListAPIView):
    queryset = User.objects.all().order_by('first_name')
    serializer_class = UserSerializer


class StatisticsListView(FakeQuerySetListView):
    fake_queryset_class = StatisticsQuerySet


class ActivityListView(FakeQuerySetListView):
    fake_queryset_class = ActivityQuerySet


class LatestChangesListView(FakeQuerySetListView):
    '''
    Lists recent changes to the database (add, change, delete or comment)
    '''
    fake_queryset_class = LatestChangesQuerySet
