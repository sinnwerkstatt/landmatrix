from django.test import TestCase

from landmatrix.models import Activity


class ActivityTestCase(TestCase):

    def test_activity(self):
        activity = Activity.objects.get(activity_identifier=1)
        self.assertEqual(activity.is_public, False)
        self.assertEqual(activity.deal_scope, None)
        self.assertEqual(activity.negotiation_status, None)
        self.assertEqual(activity.implementation_status, None)
        self.assertEqual(activity.deal_size, None)
        self.assertEqual(activity.init_date, None)

    def text_queryset(self):
        qs = Activity.objects.public()
        self.assertEqual([a.id for a in qs], [1])
        qs = Activity.objects.public_or_deleted()
        qs = Activity.objects.public_or_pending()
        qs = Activity.objects.pending()
        qs = Activity.objects.pending_only()
        qs = Activity.objects.active()
        qs = Activity.objects.overwritten()
        qs = Activity.objects.to_delete()
        qs = Activity.objects.deleted()
        qs = Activity.objects.rejected()
        qs = Activity.objects.activity_identifier_count()
        qs = Activity.objects.overall_activity_count()
        qs = Activity.objects.public_activity_count()