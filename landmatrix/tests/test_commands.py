from django.test import TestCase
from django.core.management import call_command


class PopulateActivitiesCommandTestCase(TestCase):

    fixtures = [
        'countries_and_regions',
        'users_and_groups',
        'status',
        'investors',
        'activities',
        'activity_involvements',
        'venture_involvements',
    ]

    def setUp(self):
        pass

    def test(self):
        args = []
        opts = {}
        #call_command('populate_activities', *args, **opts)
        #FIXME: Check activity attributes


class SearchIndexCommandTestCase(TestCase):

    fixtures = [
        'countries_and_regions',
        'users_and_groups',
        'status',
        'investors',
        'activities',
        'activity_involvements',
        'venture_involvements',
    ]

    def setUp(self):
        pass

    def test(self):
        args = []
        opts = {}
        #call_command('search_index', *args, **opts)
        #FIXME: Check elasticsearch
