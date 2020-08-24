from django.core.management import call_command
from django.test import TestCase, override_settings

from apps.landmatrix.tasks import (
    es_save,
    index_activity,
    index_investor,
    delete_historicalactivity,
    delete_historicalinvestor,
)


class TasksTestCase(TestCase):
    @classmethod
    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def setUpClass(cls):
        super().setUpClass()

        fixtures = [
            "countries_and_regions",
            "users_and_groups",
            "status",
            "crops",
            "animals",
            "minerals",
        ]
        for fixture in fixtures:
            call_command("loaddata", fixture, **{"verbosity": 0})
        es_save.create_index(delete=True)
        es_save.index_activity_documents()
        es_save.index_investor_documents()
        es_save.refresh_index()

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_index_activity(self):
        task = index_activity.s(1).apply()
        self.assertEqual("SUCCESS", task.status)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_delete_historicalactivity(self):
        task = delete_historicalactivity.s(2).apply()
        self.assertEqual("SUCCESS", task.status)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_index_investor(self):
        task = index_investor.s(1).apply()
        self.assertEqual("SUCCESS", task.status)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_delete_historicalinvestor(self):
        task = delete_historicalinvestor.s(2).apply()
        self.assertEqual("SUCCESS", task.status)
