from datetime import datetime

import pytz
from django.test import TestCase

from apps.feeds.activity_changes import ActivityChangesList
from apps.landmatrix.models import HistoricalInvestor
from apps.landmatrix.tests.mixins import (
    ActivitiesFixtureMixin,
    InvestorsFixtureMixin,
    InvestorActivityInvolvementsFixtureMixin,
)


class FeedsActivityChangesTestCase(
    ActivitiesFixtureMixin,
    InvestorsFixtureMixin,
    InvestorActivityInvolvementsFixtureMixin,
    TestCase,
):

    act_fixtures = [
        {"id": 10, "activity_identifier": 1, "fully_updated": True, "attributes": {}},
        {"id": 20, "activity_identifier": 2, "attributes": {}},
        {
            "id": 21,
            "activity_identifier": 2,
            "history_date": datetime(2000, 1, 2, 0, 0, tzinfo=pytz.utc),
            "fk_status_id": 1,
            "attributes": {"production_size": {"value": 200}},
        },
    ]
    inv_fixtures = [
        {"id": 10, "investor_identifier": 1, "name": "Test Investor #1"},
        {"id": 20, "investor_identifier": 2, "name": "Test Investor #2"},
    ]
    act_inv_fixtures = {"10": "10", "20": "20"}

    def setUp(self):
        super().setUp()
        self.changes = ActivityChangesList(2)

    def test_iter(self):
        iterator = iter(self.changes)
        self.assertEqual(1, iterator.index)
        self.assertEqual(20, iterator.earlier_activity.id)
        self.assertEqual(21, iterator.later_activity.id)

    def test_iter_without_earlier(self):
        self.changes.history = self.changes.history[:1]
        iterator = iter(self.changes)
        self.assertEqual(1, iterator.index)
        self.assertEqual(None, iterator.earlier_activity)
        self.assertEqual(21, iterator.later_activity.id)

    def test_iter_without_later(self):
        self.changes.history = []
        iterator = iter(self.changes)
        self.assertEqual(1, iterator.index)
        self.assertEqual(None, iterator.earlier_activity)
        self.assertEqual(None, iterator.later_activity)

    def test_compare_deals(self):
        self.changes.earlier_activity = self.changes.history[1]
        later_activity = self.changes.history[0]
        self.changes.later_activity = later_activity
        changes = self.changes.compare_deals()
        sort_key = lambda i: i[1]
        changes.sort(key=sort_key)

        expected = [
            (1, "production_size", "200", "3"),
            (
                None,
                "operational_stakeholder",
                None,
                HistoricalInvestor.objects.get(id=20),
            ),
        ]
        expected.sort(key=sort_key)
        self.assertEqual(expected, changes)

    def test_compare_deals_without_later(self):
        self.changes.earlier_activity = self.changes.history[0]
        self.changes.later_activity = None
        self.assertEqual([], self.changes.compare_deals())

    def test_next(self):
        self.changes.index = 1
        self.changes.earlier_activity = self.changes.history[1]
        self.changes.later_activity = self.changes.history[0]
        history_date, activity, changes = next(self.changes)
        self.assertEqual(datetime(2000, 1, 1, 0, 0, tzinfo=pytz.utc), history_date)
        self.assertEqual(20, activity.id)
        self.assertGreater(len(changes), 0)
