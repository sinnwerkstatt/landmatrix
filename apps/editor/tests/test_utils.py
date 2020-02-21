from datetime import datetime

import pytz
from django.test import TestCase

from apps.editor.utils import *
from apps.landmatrix.models import (
    ActivityFeedback,
    HistoricalActivity,
    HistoricalInvestor,
    Status,
)
from apps.landmatrix.tests.mixins import (
    ActivitiesFixtureMixin,
    InvestorsFixtureMixin,
    InvestorActivityInvolvementsFixtureMixin,
)


class EditorUtilsTestCase(
    ActivitiesFixtureMixin,
    InvestorsFixtureMixin,
    InvestorActivityInvolvementsFixtureMixin,
    TestCase,
):

    act_fixtures = [{"id": 10, "activity_identifier": 1, "attributes": {}}]
    inv_fixtures = [{"id": 10, "investor_identifier": 1, "name": "Test Investor #1"}]
    act_inv_fixtures = {"10": "10"}

    def test_activity_or_investor_to_template_with_activity(self):
        activity = HistoricalActivity.objects.get(id=10)
        template = activity_or_investor_to_template(activity)
        expected = {
            "id": 1,
            "history_id": 10,
            "user": "reporter (Reporter)",
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
            "user": "reporter (Reporter)",
            "timestamp": "2000-01-01 01:00:00",
            "status": Status.objects.get(id=2),
            "comment": "comment",
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
        feedback = ActivityFeedback.objects.create(
            id=10,
            fk_activity_id=10,
            fk_user_assigned_id=2,
            fk_user_created_id=1,
            comment="Test feedback",
            timestamp=datetime(2000, 1, 1, 0, 0, tzinfo=pytz.utc),
        )
        template = feedback_to_template(feedback)
        expected = {
            "id": 1,
            "history_id": 10,
            "from_user": "reporter",
            "comment": "Test feedback",
            "timestamp": "2000-01-01 01:00:00",
        }
        self.assertEqual(expected, template)
