from django.core.exceptions import ValidationError
from django.test import TestCase

from global_app.forms.investor_formset import InvestorFormSet
from global_app.forms.operational_stakeholder_form import OperationalStakeholderForm
from landmatrix.models.investor import Investor

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class TestInvestorFormset(TestCase):

    def test_investor_formset_instantiates(self):
        self._test_form_instantiates(InvestorFormSet)

    def test_investor_formset_management_form_invalid(self):
        formset = InvestorFormSet({'form-0-investor': 'nonsense'})
        with self.assertRaises(ValidationError):
            print(formset.errors)

    def test_investor_formset_management_form(self):
        formset = self._make_formset(InvestorFormSet)
        self.assertFalse(formset.is_valid())

    def test_investor_formset_data(self):
        self._test_data_source_formset(InvestorFormSet, {'form-0-investor_name': 'something'})

    def test_investor_formset_data_invalid_format(self):
        formset = self._make_formset(InvestorFormSet, {'investor_name': 'something'})
        self.assertFalse(formset.is_valid())

    def _test_data_source_formset(self, formset_class, data=None):
        formset = self._make_formset(formset_class, data)
        if formset.errors and formset.errors[0]:
            print('errors', formset.errors)
        self.assertTrue(formset.is_valid())

    def _make_formset(self, formset_class, data=None):
        form_data = {"form-TOTAL_FORMS": 1, "form-INITIAL_FORMS": 0, "form-MAX_NUM_FORMS": 1000}
        if data:
            form_data.update(data)
        formset = formset_class(form_data)
        return formset

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