__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from landmatrix.models import Deal, Activity

from django.test import TestCase
from django.utils import timezone
from django.db.models import Max


class TestDeal(TestCase):

    def test_gets_created_witout_activities(self):
        deal = Deal(1)

    def test_all_without_activities(self):
        self.assertEqual([], Deal.objects.all())

    def test_all_with_activity(self):
        Activity(
            activity_identifier=1, version=1, availability=0.5, fully_updated=timezone.now(),
            fk_status_id=2
        ).save()
        print(Activity.objects.filter(activity_identifier=1))
        print(Activity.objects.filter(activity_identifier=1).values())
        print(Activity.objects.filter(activity_identifier=1).values()).aggregate(Max('version'))



        print(Deal.objects.all())