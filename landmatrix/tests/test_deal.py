from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist

from landmatrix.models.activity_attribute_group import ActivityAttributeGroup
from landmatrix.models.investor import Investor, InvestorActivityInvolvement
from landmatrix.models.language import Language
from landmatrix.tests.with_status import WithStatus

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from landmatrix.models import Deal, Activity

from django.test import TestCase
from django.utils import timezone
from django.db.models import Max


class TestDeal(WithStatus):

    NUM_ACTIVITIES = 10

    def setUp(self):
        WithStatus.setUp(self)
        Language(english_name='English', local_name='English', locale='en').save()
        self.language = Language.objects.last()

    def test_gets_created_witout_activities(self):
        with self.assertRaises(ObjectDoesNotExist):
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
        self._assert_is_n_deals(deals, length)

    SUBSET_LENGTH = 4
    def test_filter_activity_identifier(self):
        length = self.NUM_ACTIVITIES
        for act_id in range(1, length+1):
            self._create_activity(act_id)
        deals = Deal.objects.filter(activity_identifier__lt=self.SUBSET_LENGTH+1)
        self._assert_is_n_deals(deals, self.SUBSET_LENGTH)
        for deal in deals:
            self.assertLess(self.SUBSET_LENGTH+1, deal.activity_identifier)

    def test_filter_attributes(self):
        length = self.NUM_ACTIVITIES
        for act_id in range(1, length+1):
            self._create_activity(act_id)
            self._create_attributes(act_id, {'some_attribute': act_id})



    def _assert_is_n_deals(self, deals, length):
        for i in range(0, length):
            self.assertIsInstance(deals[i], Deal)
        with self.assertRaises(IndexError):
            deals[length]

    def test_single_set_of_attributes(self):
        self._create_activity(1)
        self._create_attributes(1, {'some_attribute': 'some_value'})
        deal = Deal(1)
        self.assertDictEqual(deal.attributes, {'some_attribute': 'some_value'})

    def test_multiple_attributes(self):
        self._create_activity(1)
        self._create_attributes(1, {'some_attribute': 'some_value'})
        self._create_attributes(1, {'some_other_attribute': 'some_other_value'})
        deal = Deal(1)

        self.assertDictEqual(deal.attributes, {'some_attribute': 'some_value', 'some_other_attribute': 'some_other_value'})

    def test_attribute_groups(self):
        self._create_activity(1)
        self._create_attributes(1, {'some_attribute': 'some_value'})
        self._create_attributes(1, {'some_other_attribute': 'some_other_value'})
        deal = Deal(1)
        self.assertEqual(2, len(deal.attribute_groups()))
        for group in deal.attribute_groups():
            # Whoever thought it a good idea to deprecate assertDictIsSubset() deserves to step on Legos!
            self.assertTrue(
                set(group.attributes.items()).issubset(set({'some_attribute': 'some_value', 'some_other_attribute': 'some_other_value'}.items()))
            )

    def test_same_attribute_multiple_values(self):
        self._create_activity(1)
        self._create_attributes(1, {'the_same_attribute': 'some_value'})
        self._create_attributes(1, {'the_same_attribute': 'some_other_value'})
        deal = Deal(1)
        self.assertEqual(2, len(deal.attribute_groups()))
        values = map(lambda g: g.attributes['the_same_attribute'], deal.attribute_groups())
        self.assertEqual(['some_other_value', 'some_value'], sorted(values))

    def _check_is_deal_list(self, deals, length):
        self.assertEqual(length, len(list(deals)))
        self._check_all_are_deals(deals)

    def _check_all_are_deals(self, deals):
        for deal in deals:
            self.assertIsInstance(deal, Deal)

    def _create_activity(self, act_id):
        act = Activity(
            activity_identifier=act_id, availability=0.5, fully_updated=timezone.now(),
            fk_status_id=2
        )
        act.save()
        self._create_investor(act)

    def _create_attributes(self, act_id, attributes):
        act = Activity.objects.filter(activity_identifier=act_id).first()
        ActivityAttributeGroup(fk_activity=act, attributes=attributes, fk_language=self.language, date=datetime.now()).save()

    def _create_investor(self, activity, inv_id=None):
        if not inv_id:
            inv_id = activity.activity_identifier
        inv = Investor(investor_identifier=inv_id, name='Investor '+str(inv_id), fk_status_id=2)
        inv.save()
        InvestorActivityInvolvement(fk_activity=activity, fk_investor=inv, percentage=50, fk_status_id=2).save()