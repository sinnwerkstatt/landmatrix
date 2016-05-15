
from grid.views.activity_protocol import ActivityQuerySet
from api.query_sets.latest_changes_query_set import LatestChangesQuerySet
from api.query_sets.statistics_query_set import StatisticsQuerySet
from api.query_sets.users_query_set import UsersQuerySet
from api.views.base import FakeQuerySetListView

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class UserListView(FakeQuerySetListView):
    fake_queryset_class = UsersQuerySet


class StatisticsListView(FakeQuerySetListView):
    fake_queryset_class = StatisticsQuerySet


class ActivityListView(FakeQuerySetListView):
    fake_queryset_class = ActivityQuerySet


class LatestChangesListView(FakeQuerySetListView):
    '''
    Lists recent changes to the database (add, change, delete or comment)
    '''
    fake_queryset_class = LatestChangesQuerySet
