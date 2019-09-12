from django.core.management import call_command
from django.test import TestCase, override_settings

from apps.landmatrix.tasks import *


class TasksTestCase(TestCase):

    @classmethod
    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def setUpClass(cls):
        super().setUpClass()

        fixtures = [
            'countries_and_regions',
            'users_and_groups',
            'status',
            'crops',
            'animals',
            'minerals',
            'investors',
            'activities',
            'activity_involvements',
            'venture_involvements',
        ]
        for fixture in fixtures:
            call_command('loaddata', fixture)
        es_save.create_index(delete=True)
        es_save.index_activity_documents()
        es_save.index_investor_documents()
        es_save.refresh_index()

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_index_activity(self):
        task = index_activity.s(1).apply()
        self.assertEqual('SUCCESS', task.status)

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_delete_activity(self):
        task = delete_activity.s(2).apply()
        self.assertEqual('SUCCESS', task.status)

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_index_investor(self):
        task = index_investor.s(1).apply()
        self.assertEqual('SUCCESS', task.status)

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_delete_investor(self):
        task = delete_investor.s(2).apply()
        self.assertEqual('SUCCESS', task.status)
