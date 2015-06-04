from django.test import TestCase

from .models import Involvement, Activity, Stakeholder

class InvolvementTest(TestCase):

    DUMMY_INVESTMENT_RATIO = 1.23

    def test_gets_created(self):
        involvement = Involvement()
        self.assertIsInstance(involvement, Involvement)

    def test_accepts_investment_ratio(self):
        involvement = Involvement(investment_ratio=self.DUMMY_INVESTMENT_RATIO)
        self.assertEqual(self.DUMMY_INVESTMENT_RATIO, involvement.investment_ratio)

    def test_str(self):
        involvement = Involvement(investment_ratio=self.DUMMY_INVESTMENT_RATIO)
        self.assertTrue(str(self.DUMMY_INVESTMENT_RATIO) in str(involvement))

    def test_save(self):
        involvement = Involvement(investment_ratio=self.DUMMY_INVESTMENT_RATIO)
        old_count = Involvement.objects.count()
        involvement.save()
        self.assertEqual(old_count+1, Involvement.objects.count())
        self.assertEqual(self.DUMMY_INVESTMENT_RATIO, float(Involvement.objects.last().investment_ratio))

from django.utils import timezone

class ActivityTest(TestCase):

    def test_gets_created_with_params(self):
        activity = Activity(activity_identifier=1, version=1, availability=0.5, fully_updated=timezone.now())
        self.assertIsInstance(activity, Activity)
        self.assertEqual(1, activity.activity_identifier)
        self.assertEqual(1, activity.version)
        self.assertEqual(0.5, activity.availability)

    def test_gets_saved(self):
        Activity(activity_identifier=1, version=1, availability=0.5, fully_updated=timezone.now()).save()
        activity = Activity.objects.last()
        self.assertIsInstance(activity, Activity)
        self.assertEqual(1, activity.activity_identifier)
        self.assertEqual(1, activity.version)
        self.assertEqual(0.5, activity.availability)


class StakeholderTest(TestCase):

    def test_gets_saved(self):
        Stakeholder(stakeholder_identifier=1, version=2).save()
        stakeholder = Stakeholder.objects.last()
        self.assertIsInstance(stakeholder, Stakeholder)
        self.assertEqual(1, stakeholder.stakeholder_identifier)
        self.assertEqual(2, stakeholder.version)