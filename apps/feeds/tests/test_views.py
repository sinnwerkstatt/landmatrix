from datetime import datetime

import pytz
from django.test import TestCase
from django.urls import reverse

from apps.landmatrix.models import HistoricalActivity
from apps.landmatrix.tests.mixins import ActivitiesFixtureMixin


class FeedsViewsTestCase(ActivitiesFixtureMixin, TestCase):

    act_fixtures = [
        {"id": 1, "activity_identifier": 1, "attributes": {}},
        {
            "id": 2,
            "activity_identifier": 1,
            "history_date": datetime(2000, 1, 2, 0, 0, tzinfo=pytz.utc),
            "attributes": {"production_size": {"value": "300"}},
        },
    ]

    def test_activity_changes_feed(self):
        response = self.client.get(reverse("deal_changes_feed", kwargs={"deal_id": 1}))
        self.assertEqual(200, response.status_code)

    def test_activity_changes_feed_without_user(self):
        activity = HistoricalActivity.objects.get(id=1)
        activity.history_user = None
        activity.save()
        response = self.client.get(reverse("deal_changes_feed", kwargs={"deal_id": 1}))
        self.assertEqual(200, response.status_code)
