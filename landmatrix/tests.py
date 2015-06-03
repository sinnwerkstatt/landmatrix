from django.test import TestCase

from .models import Involvement

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
