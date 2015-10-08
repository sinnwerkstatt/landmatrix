__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from landmatrix.models import Deal, Activity

from django.test import TestCase
from django.utils import timezone
from django.db.models import Max


class TestDeal(TestCase):

    NUM_ACTIVITIES = 10

    def test_gets_created_witout_activities(self):
        deal = Deal(1)

    def test_all_without_activities(self):
        self.assertEqual([], list(Deal.objects.all()))

    def test_all_with_one_activity(self):
        length = 1
        for act_id in range(1, length+1):
            self._create_activity(act_id)
        deals = Deal.objects.all()
        self._check_is_deal_list(deals, 1)

    def test_all_with_several_activities(self):
        length = self.NUM_ACTIVITIES
        for act_id in range(1, length+1):
            self._create_activity(act_id)
        deals = Deal.objects.all()
        self._check_is_deal_list(deals, self.NUM_ACTIVITIES)

    def test_all_is_indexable(self):
        length = self.NUM_ACTIVITIES
        for act_id in range(1, length+1):
            self._create_activity(act_id)
        deals = Deal.objects.all()
        self.assertIsInstance(deals[0], Deal)
        self.assertIsInstance(deals[self.NUM_ACTIVITIES-1], Deal)

    def test_all_index_out_of_range(self):
        length = self.NUM_ACTIVITIES
        for act_id in range(1, length+1):
            self._create_activity(act_id)
        deals = Deal.objects.all()
        with self.assertRaises(IndexError):
            deals[self.NUM_ACTIVITIES]

    def _check_is_deal_list(self, deals, length):
        self.assertEqual(length, len(list(deals)))
        self._check_all_are_deals(deals)

    def _check_all_are_deals(self, deals):
        for deal in deals:
            self.assertIsInstance(deal, Deal)

    def _create_activity(self, act_id):
        Activity(
            activity_identifier=act_id, version=1, availability=0.5, fully_updated=timezone.now(),
            fk_status_id=2
        ).save()
