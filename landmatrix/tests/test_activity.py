from django.test import TestCase
from django.utils import timezone
from landmatrix.models import Activity

__author__ = 'lene'


class TestActivity(TestCase):

    def test_gets_created_with_params(self):
        activity = Activity(activity_identifier=1, version=1, availability=0.5, fully_updated=timezone.now())
        self.assertIsInstance(activity, Activity)
        self.assertEqual(1, activity.activity_identifier)
        self.assertEqual(1, activity.version)
        self.assertEqual(0.5, activity.availability)

    def test_gets_saved(self):
        Activity(activity_identifier=1, version=1, availability=0.5, fully_updated=timezone.now()).save()
        activity = Activity.objects.last()
        self.assertIsInstance(activity, Activity)
        self.assertEqual(1, activity.activity_identifier)
        self.assertEqual(1, activity.version)
        self.assertEqual(0.5, activity.availability)