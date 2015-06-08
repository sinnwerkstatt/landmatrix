__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from landmatrix.models import Stakeholder
from landmatrix.tests.with_status import WithStatus

class TestStakeholder(WithStatus):

    def test_gets_saved(self):
        Stakeholder(stakeholder_identifier=1, version=2, fk_status=self.status).save()
        stakeholder = Stakeholder.objects.last()
        self.assertIsInstance(stakeholder, Stakeholder)
        self.assertEqual(1, stakeholder.stakeholder_identifier)
        self.assertEqual(2, stakeholder.version)