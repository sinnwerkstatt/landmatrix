__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django.test import TestCase
from landmatrix.models import Stakeholder, Status

class TestStakeholder(TestCase):

    def setUp(self):
        self.status = Status.objects.get(id=1)

    def test_gets_saved(self):
        Stakeholder(stakeholder_identifier=1, version=2, fk_status=self.status).save()
        stakeholder = Stakeholder.objects.last()
        self.assertIsInstance(stakeholder, Stakeholder)
        self.assertEqual(1, stakeholder.stakeholder_identifier)
        self.assertEqual(2, stakeholder.version)