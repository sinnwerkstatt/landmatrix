from django.test import TestCase
from django.urls import reverse

from apps.landmatrix.models import HistoricalActivity


class FeedsViewsTestCase(TestCase):

    fixtures = ["countries_and_regions", "users_and_groups", "status", "activities"]

    def test_activity_changes_feed(self):
        response = self.client.get(reverse("deal_changes_feed", kwargs={"deal_id": 2}))
        self.assertEqual(200, response.status_code)

    def test_activity_changes_feed_without_user(self):
        activity = HistoricalActivity.objects.get(id=20)
        activity.history_user = None
        activity.save()
        response = self.client.get(reverse("deal_changes_feed", kwargs={"deal_id": 2}))
        self.assertEqual(200, response.status_code)
