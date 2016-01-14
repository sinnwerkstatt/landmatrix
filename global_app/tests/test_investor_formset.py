from django.core.exceptions import ValidationError
from django.test import TestCase

from global_app.forms.investor_formset import InvestorFormSet
from global_app.forms.operational_stakeholder_form import OperationalStakeholderForm
from landmatrix.models.investor import Investor

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class TestInvestorFormset(TestCase):

    def _test_form_instantiates(self, form_class):
        form = form_class()
        self.assertFalse(form.is_valid())

    def test_operational_stakeholder_initializes(self):
        self._test_form_instantiates(OperationalStakeholderForm)

    def test_operational_stakeholder_data(self):
        Investor(investor_identifier=1, name='invTESTor', classification=10, version=1, fk_status_id=2).save()
        id = Investor.objects.first().pk
        form = OperationalStakeholderForm({'operational_stakeholder': id})
        self.assertTrue(form.is_valid())

    def test_operational_stakeholder_data_present(self):
        Investor(investor_identifier=1, name='invTESTor', classification=10, version=1, fk_status_id=2).save()
        id = Investor.objects.first().pk
        form = OperationalStakeholderForm({'operational_stakeholder': id})
        self.assertTrue(form.is_valid())
        self.assertIn('operational_stakeholder', form.cleaned_data)

    def test_operational_stakeholder_data_bad(self):
        form = OperationalStakeholderForm({'operational_stakeholder': 1})
        self.assertFalse(form.is_valid())