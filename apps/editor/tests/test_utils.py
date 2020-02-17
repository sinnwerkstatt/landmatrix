from django.test import TestCase

from apps.editor.utils import *
from apps.landmatrix.models import (
    ActivityFeedback,
    HistoricalActivity,
    HistoricalInvestor,
    Status,
)


class EditorUtilsTestCase(TestCase):

    fixtures = [
        "countries_and_regions",
        "users_and_groups",
        "status",
    ]

    def test_activity_or_investor_to_template_with_activity(self):
        activity = HistoricalActivity.objects.get(id=10)
        template = activity_or_investor_to_template(activity)
        expected = {
            "id": 1,
            "history_id": 10,
            "user": "editor (Editor)",
            "timestamp": "2000-01-01 01:00:00",
            "status": Status.objects.get(id=2),
            "comment": None,
            "type": "activity",
        }
        self.assertEqual(expected, template)

    def test_activity_or_investor_to_template_with_investor(self):
        investor = HistoricalInvestor.objects.get(id=10)
        template = activity_or_investor_to_template(investor)
        expected = {
            "id": 1,
            "history_id": 10,
            "user": "editor (Editor)",
            "timestamp": "2000-01-01 01:00:00",
            "status": Status.objects.get(id=2),
            "comment": None,
            "type": "investor",
        }
        self.assertEqual(expected, template)

    def test_activity_or_investor_to_template_without_user(self):
        HistoricalActivity.objects.filter(id=10).update(history_user_id=None)
        activity = HistoricalActivity.objects.get(id=10)
        template = activity_or_investor_to_template(activity)
        expected = {
            "id": 1,
            "history_id": 10,
            "user": "Deleted user",
            "timestamp": "2000-01-01 01:00:00",
            "status": Status.objects.get(id=2),
            "comment": None,
            "type": "activity",
        }
        self.assertEqual(expected, template)

    def test_feedback_to_template(self):
        feedback = ActivityFeedback.objects.get(id=10)
        template = feedback_to_template(feedback)
        expected = {
            "id": 1,
            "history_id": 10,
            "from_user": "reporter",
            "comment": "Test feedback",
            "timestamp": "2000-01-01 01:00:00",
        }
        self.assertEqual(expected, template)
