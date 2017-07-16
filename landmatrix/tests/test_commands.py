from django.test import TestCase
from django.core.management import call_command


class TestPopulateActivities(TestCase):
    fixtures = [
        'countries_and_regions',
        'users_and_groups',
        'status',
        'activities',
    ]

    def setUp(self):
        pass

    def test(self):
        args = []
        opts = {}
        call_command('populate_activities', *args, **opts)
        #FIXME: Check activity attributes


class TestUpdateElasticSearch(TestCase):
    fixtures = [
        'countries_and_regions',
        'users_and_groups',
        'status',
        'activities',
    ]

    def setUp(self):
        pass

    def test(self):
        args = []
        opts = {}
        call_command('update_elasticsearch', *args, **opts)
        #FIXME: Check elasticsearch
