from django.test import TestCase

from global_app.forms.investor_formset import InvestorFormSet

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class TestInvestorFormset(TestCase):

    def test_investor_formset_instantiates(self):
        formset = InvestorFormSet()