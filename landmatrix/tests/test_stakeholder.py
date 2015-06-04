from django.test import TestCase
from landmatrix.models import Stakeholder

__author__ = 'lene'


class TestStakeholder(TestCase):

    def test_gets_saved(self):
        Stakeholder(stakeholder_identifier=1, version=2).save()
        stakeholder = Stakeholder.objects.last()
        self.assertIsInstance(stakeholder, Stakeholder)
        self.assertEqual(1, stakeholder.stakeholder_identifier)
        self.assertEqual(2, stakeholder.version)