from django.core.exceptions import ValidationError
from django.test import TestCase

from global_app.forms.investor_formset import InvestorFormSet
from global_app.forms.operational_stakeholder_form import OperationalStakeholderForm
from landmatrix.models.investor import Investor

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class TestInvestorFormset(TestCase):

    def setUp(self):
        Investor.objects.create(investor_identifier=1, name='Test-Stakeholder', classification=10, fk_status_id=2)
        self.operational_stakeholder_id = Investor.objects.last().id

    def _test_form_instantiates(self, form_class):
        form = form_class()
        self.assertFalse(form.is_valid())

    def test_operational_stakeholder_initializes(self):
        self._test_form_instantiates(OperationalStakeholderForm)

    def test_operational_stakeholder_data(self):
        form = OperationalStakeholderForm({'operational_stakeholder': self.operational_stakeholder_id})
        self.skipTest('Does not work yet with select2-Widget')
        self.assertTrue(form.is_valid())

    def test_operational_stakeholder_data_present(self):
        form = OperationalStakeholderForm({'operational_stakeholder': self.operational_stakeholder_id})
        self.skipTest('Does not work yet with select2-Widget')
        self.assertTrue(form.is_valid())
        self.assertIn('operational_stakeholder', form.cleaned_data)

    def test_operational_stakeholder_data_bad(self):
        form = OperationalStakeholderForm({'operational_stakeholder': 1})
        self.assertFalse(form.is_valid())