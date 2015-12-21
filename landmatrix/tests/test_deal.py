from datetime import datetime
from landmatrix.models.activity_attribute_group import ActivityAttributeGroup
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

    def DEACTIVATED_test_gets_created_witout_activities(self):
        deal = Deal(1)

    def test_all_without_activities(self):
        self.assertEqual([], list(Deal.objects.all()))

    def DEACTIVATED_test_all_with_one_activity(self):
        length = 1
        for act_id in range(1, length+1):
            self._create_activity(act_id)
        deals = Deal.objects.all()
        self._check_is_deal_list(deals, 1)

    def DEACTIVATED_test_all_with_several_activities(self):
        length = self.NUM_ACTIVITIES
        for act_id in range(1, length+1):
            self._create_activity(act_id)
        deals = Deal.objects.all()
        self._check_is_deal_list(deals, self.NUM_ACTIVITIES)

    def DEACTIVATED_test_all_is_indexable(self):
        length = self.NUM_ACTIVITIES
        for act_id in range(1, length+1):
            self._create_activity(act_id)
        deals = Deal.objects.all()
        self.assertIsInstance(deals[0], Deal)
        self.assertIsInstance(deals[self.NUM_ACTIVITIES-1], Deal)

    def DEACTIVATED_test_all_index_out_of_range(self):
        length = self.NUM_ACTIVITIES
        for act_id in range(1, length+1):
            self._create_activity(act_id)
        deals = Deal.objects.all()
        with self.assertRaises(IndexError):
            deals[self.NUM_ACTIVITIES]

    def DEACTIVATED_test_single_set_of_attributes(self):
        self._create_activity(1)
        self._create_attributes(1, {'some_attribute': 'some_value'})
        deal = Deal(1)
        self.assertDictEqual(deal.attributes, {'some_attribute': 'some_value'})

    def DEACTIVATED_test_multiple_attributes(self):
        self._create_activity(1)
        self._create_attributes(1, {'some_attribute': 'some_value'})
        self._create_attributes(1, {'some_other_attribute': 'some_other_value'})
        deal = Deal(1)

        self.assertDictEqual(deal.attributes, {'some_attribute': 'some_value', 'some_other_attribute': 'some_other_value'})

    def DEACTIVATED_test_attribute_groups(self):
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

    def DEACTIVATED_test_same_attribute_multiple_values(self):
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
        Activity(
            activity_identifier=act_id, version=1, availability=0.5, fully_updated=timezone.now(),
            fk_status_id=2
        ).save()

    def _create_attributes(self, act_id, attributes):
        act = Activity.objects.filter(activity_identifier=act_id).first()
        ActivityAttributeGroup(fk_activity=act, attributes=attributes, fk_language=self.language, date=datetime.now()).save()