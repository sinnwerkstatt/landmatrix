
from django.test import TestCase

from grid.forms.add_deal_action_comment_form import AddDealActionCommentForm
from grid.forms.add_deal_employment_form import AddDealEmploymentForm
from grid.forms.add_deal_general_form import AddDealGeneralForm
from grid.forms.add_deal_general_public_form import AddDealGeneralPublicForm
from grid.forms.add_deal_overall_comment_form import AddDealOverallCommentForm
from grid.forms.add_investor_form import AddInvestorForm
from grid.forms.add_primary_investor_form import AddPrimaryInvestorForm
from grid.forms.base_form import BaseForm
from grid.forms.change_deal_action_comment_form import ChangeDealActionCommentForm
from grid.forms.change_deal_employment_form import ChangeDealEmploymentForm
from grid.forms.change_deal_general_form import ChangeDealGeneralForm
from grid.forms.change_deal_overall_comment_form import ChangeDealOverallCommentForm
from grid.forms.change_investor_form import ChangeInvestorForm
from grid.forms.change_primary_investor_form import ChangePrimaryInvestorForm
from grid.forms.deal_data_source_form import AddDealDataSourceFormSet, ChangeDealDataSourceFormSet, \
    PublicViewDealDataSourceFormSet
from grid.forms.deal_former_use_form import DealFormerUseForm
from grid.forms.deal_gender_related_info_form import DealGenderRelatedInfoForm
from grid.forms.deal_history_form import DealHistoryForm
from grid.forms.deal_local_communities_form import DealLocalCommunitiesForm
from grid.forms.deal_primary_investor_form import DealPrimaryInvestorForm
from grid.forms.deal_produce_info_form import DealProduceInfoForm
from landmatrix.models.crop import Crop

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class TestForms(TestCase):

    def test_base_form_instantiates(self):
        form = BaseForm()

    def test_empty_base_form_invalid(self):
        self._test_form_instantiates(BaseForm)

    def _test_form_instantiates(self, form_class):
        form = form_class()
        self.assertFalse(form.is_valid())

    def test_add_deal_action_comment_form_instantiates(self):
        self._test_form_instantiates(AddDealActionCommentForm)

    def test_add_deal_employment_form_instantiates(self):
        self._test_form_instantiates(AddDealEmploymentForm)

    def test_add_deal_employment_form_data(self):
        self._test_employment_form(AddDealEmploymentForm)

    def _test_employment_form(self, form_class):
        form = form_class({'total_jobs_created': False})
        self.assertTrue(form.is_valid())
        form = form_class({'total_jobs_created': True})
        self.assertTrue(form.is_valid())

    def test_add_deal_general_form_instantiates(self):
        self._test_form_instantiates(AddDealGeneralForm)

    def test_add_deal_general_form_data(self):
        self._test_general_form(AddDealGeneralForm)

    def _test_general_form(self, form_class):
        form = form_class({'intended_size': 1})
        self.assertTrue(form.is_valid())
        form = form_class({'contract_size': 1})
        self.assertTrue(form.is_valid())
        form = form_class({'production_size': 1})
        self.assertTrue(form.is_valid())
        form = form_class({'nature': (10,)})
        self.assertTrue(form.is_valid())
        form = form_class({'intention': (10,)})
        self.assertTrue(form.is_valid())

    def test_add_deal_general_public_form_instantiates(self):
        self._test_form_instantiates(AddDealGeneralPublicForm)

    def test_add_deal_overall_comment_form_instantiates(self):
        self._test_form_instantiates(AddDealOverallCommentForm)

    def test_add_investor_form_instantiates(self):
        self._test_form_instantiates(AddInvestorForm)

    def test_add_investor_form_data(self):
        self._test_investor_form(AddInvestorForm)

    def _test_investor_form(self, form_class):
        form = form_class({'investor_name': '', 'country': '', 'classification': ''})
        self.assertTrue(form.is_valid())

    def test_add_primaryinvestor_form_instantiates(self):
        self._test_form_instantiates(AddPrimaryInvestorForm)

    def test_add_primaryinvestor_form_data(self):
        self.skipTest('primary investor form obsolete and not yet rewritten')
        self._test_primary_investor_form(AddPrimaryInvestorForm)

    def _test_primary_investor_form(self, form_class):
        form = form_class({'primary_investor_name': 'horst'})
        if form.errors: print(form.errors)
        self.assertTrue(form.is_valid())

    def test_change_deal_action_comment_form_instantiates(self):
        self._test_form_instantiates(ChangeDealActionCommentForm)

    def test_change_deal_employment_form_instantiates(self):
        self._test_form_instantiates(ChangeDealEmploymentForm)

    def test_change_deal_employment_form_data(self):
        self._test_employment_form(ChangeDealEmploymentForm)

    def test_change_deal_general_form_instantiates(self):
        self._test_form_instantiates(ChangeDealGeneralForm)

    def test_change_deal_general_form_data(self):
        self._test_employment_form(ChangeDealGeneralForm)

    def test_change_deal_overall_comment_form_instantiates(self):
        self._test_form_instantiates(ChangeDealOverallCommentForm)

    def test_change_investor_form_instantiates(self):
        self._test_form_instantiates(ChangeInvestorForm)

    def test_change_investor_form_data(self):
        self._test_investor_form(ChangeInvestorForm)

    def test_change_primary_investor_form_instantiates(self):
        self._test_form_instantiates(ChangePrimaryInvestorForm)

    def test_change_primary_investor_form_data(self):
        self._test_primary_investor_form(ChangePrimaryInvestorForm)

    def test_add_deal_data_source_form_instantiates(self):
        self._test_form_instantiates(AddDealDataSourceFormSet)

    def test_add_deal_data_source_form_data(self):
        self._test_data_source_formset(AddDealDataSourceFormSet)

    def _test_data_source_formset(self, formset_class):
        formset = formset_class({
            "form-TOTAL_FORMS": 1, "form-INITIAL_FORMS": 0, "form-MAX_NUM_FORMS": 1000,
            'form-0-type': 10, 'form-0-url': 'http://lmgtfy.com/?q=what+is+the+internet'
        })
        # print(formset.errors)
        self.assertTrue(formset.is_valid())

    def test_change_deal_data_source_form_data(self):
        self._test_data_source_formset(ChangeDealDataSourceFormSet)

    def test_public_view_data_source_form_data(self):
        self._test_data_source_formset(PublicViewDealDataSourceFormSet)

    def test_deal_former_use_form_instantiates(self):
        self._test_form_instantiates(DealFormerUseForm)

    def test_deal_former_use_form_data(self):
        form = DealFormerUseForm({'land_owner': (10,)})
        self.assertTrue(form.is_valid())

    def test_deal_gender_related_info_form_instantiates(self):
        self._test_form_instantiates(DealGenderRelatedInfoForm)

    def test_deal_history_form_instantiates(self):
        self._test_form_instantiates(DealHistoryForm)

    def test_deal_local_communities_form_instantiates(self):
        self._test_form_instantiates(DealLocalCommunitiesForm)

    def test_deal_local_communities_form_data(self):
        form = DealLocalCommunitiesForm({'community_reaction': 10})
        self.assertTrue(form.is_valid())

    def test_deal_primary_investor_form_instantiates(self):
        self._test_form_instantiates(DealPrimaryInvestorForm)

    def test_deal_primary_investor_form_data(self):
        form = DealPrimaryInvestorForm({'project_name': 'blah', 'primary_investor': 10})
        self.assertTrue(form.is_valid())

    def test_deal_produce_info_form_instantiates(self):
        self._test_form_instantiates(DealProduceInfoForm)

    def test_deal_produce_info_form_data(self):
        Crop(code='BLA', name='Blah', slug='blah').save()
        id = Crop.objects.first().pk
        form = DealProduceInfoForm({'crops': (id,)})
        self.assertTrue(form.is_valid())




