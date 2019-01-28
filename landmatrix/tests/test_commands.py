from django.test import TestCase
from django.core.management import call_command


#class TestCommandPopulateActivities(TestCase):
#    fixtures = [
#        'countries_and_regions',
#        'users_and_groups',
#        'status',
#        'activities',
#        'involvements',
#    ]
#
#    def setUp(self):
#        pass
#
#    def test(self):
#        args = []
#        opts = {}
#        call_command('populate_activities', *args, **opts)
#        #FIXME: Check activity attributes
#
#
#class TestCommandSearchIndex(TestCase):
#    fixtures = [
#        'countries_and_regions',
#        'users_and_groups',
#        'status',
#        'activities',
#        'involvements',
#    ]
#
#    def setUp(self):
#        pass
#
#    def test(self):
#        args = []
#        opts = {}
#        call_command('search_index', *args, **opts)
#        #FIXME: Check elasticsearch
#