__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django.test import TestCase
from landmatrix.models import PrimaryInvestor

class TestPrimaryInvestor(TestCase):

    def test_gets_saved(self):
        PrimaryInvestor(primary_investor_identifier=1, name='A Silly Name', version=2).save()
        investor = PrimaryInvestor.objects.last()
        self.assertIsInstance(investor, PrimaryInvestor)
        self.assertEqual(1, investor.primary_investor_identifier)
        self.assertEqual('A Silly Name', investor.name)
        self.assertEqual(2, investor.version)