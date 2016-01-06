from django.core.exceptions import ValidationError
from django.test import TestCase

from global_app.forms.investor_formset import InvestorFormSet

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class TestInvestorFormset(TestCase):

    def test_investor_formset_instantiates(self):
        formset = InvestorFormSet()
        self.assertFalse(formset.is_valid())

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
