from django.test import TestCase

from landmatrix.models import Activity


class ActivityTestCase(TestCase):
    def setUp(self):
        Activity.objects.create(
            activity_identifier=1,
            availability=0.0,
            fully_updated=True,
            fk_status=1,
        )

    def test_activity(self):
        """Animals that can speak are correctly identified"""
        activity = Activity.objects.get(activity_identifier=1)
        self.assertEqual(activity.is_public, None)
        self.assertEqual(activity.deal_scope, None)
        self.assertEqual(activity.negotiation_status, None)
        self.assertEqual(activity.implementation_status, None)
        self.assertEqual(activity.deal_size, None)
        self.assertEqual(activity.init_date, None)