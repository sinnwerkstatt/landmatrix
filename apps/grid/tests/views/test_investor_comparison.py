from django.test import TestCase
from django.urls import reverse

from apps.grid.views.investor_comparison import *
from apps.landmatrix.models import HistoricalInvestor


class InvestorComparisonViewTestCase(TestCase):

    fixtures = [
        'countries_and_regions',
        'users_and_groups',
        'status',
        'investors',
        'activities',
        'activity_involvements',
        'venture_involvements',
    ]

    def assert_comparison(self, context_data):
        investors = context_data.get('investors', [])
        self.assertEqual(2, len(investors))
        self.assertEqual(31, investors[0].pk)
        self.assertEqual(30, investors[1].pk)
        forms = context_data.get('forms', [])
        self.assertEqual(False, forms[0][2])
        self.assertEqual(False, forms[1][2])
        self.assertEqual(True, forms[2][2])

    def test_with_one_investor(self):
        self.client.login(username='reporter', password='test')
        response = self.client.get(reverse('compare_investors', kwargs={'investor_1': '31'}))
        self.client.logout()
        self.assertEqual(200, response.status_code)
        self.assert_comparison(response.context_data)

    def test_with_reporter(self):
        self.client.login(username='reporter', password='test')
        response = self.client.get(reverse('compare_investors', kwargs={'investor_1': '31', 'investor_2': '30'}))
        self.client.logout()
        self.assertEqual(200, response.status_code)
        self.assert_comparison(response.context_data)

    def test_with_editor(self):
        self.client.login(username='editor', password='test')
        response = self.client.get(reverse('compare_investors', kwargs={'investor_1': '31', 'investor_2': '30'}))
        self.client.logout()
        self.assertEqual(200, response.status_code)
        self.assert_comparison(response.context_data)

    def test_with_administrator(self):
        self.client.login(username='administrator', password='test')
        response = self.client.get(reverse('compare_investors', kwargs={'investor_1': '31', 'investor_2': '30'}))
        self.client.logout()
        self.assertEqual(200, response.status_code)
        self.assert_comparison(response.context_data)


class GridInvestorComparisonViewTestCase(TestCase):

    fixtures = [
        'countries_and_regions',
        'users_and_groups',
        'status',
        'investors',
    ]

    def test_get_comparison(self):
        investor_1 = HistoricalInvestor.objects.get(id=30)
        investor_2 = HistoricalInvestor.objects.get(id=31)
        forms = get_comparison(investor_1, investor_2)
        self.assertEqual(False, forms[0][2])
        self.assertEqual(True, forms[1][2])

    def test_is_equal_with_formset_changed(self):
        form_1 = ParentCompanyFormSet(data={
            'parent-company-TOTAL_FORMS': 1,
            'parent-company-INITIAL_FORMS': 0,
            'parent-company-MIN_NUM_FORMS': 1,
            'parent-company-MAX_NUM_FORMS': 1,
            'parent-company-0-fk_investor': 10,
        }, prefix='parent-company')
        form_2 = ParentCompanyFormSet(data={
            'parent-company-TOTAL_FORMS': 1,
            'parent-company-INITIAL_FORMS': 0,
            'parent-company-MIN_NUM_FORMS': 1,
            'parent-company-MAX_NUM_FORMS': 1,
            'parent-company-0-fk_investor': 20,
        }, prefix='parent-company')
        self.assertEqual(False, is_equal(form_1, form_2))

    def test_is_equal_with_formset_not_changed(self):
        form_1 = ParentCompanyFormSet(data={
            'parent-company-TOTAL_FORMS': 1,
            'parent-company-INITIAL_FORMS': 0,
            'parent-company-MIN_NUM_FORMS': 1,
            'parent-company-MAX_NUM_FORMS': 1,
            'parent-company-0-fk_investor': 10,
        }, prefix='parent-company')
        form_2 = ParentCompanyFormSet(data={
            'parent-company-TOTAL_FORMS': 1,
            'parent-company-INITIAL_FORMS': 0,
            'parent-company-MIN_NUM_FORMS': 1,
            'parent-company-MAX_NUM_FORMS': 1,
            'parent-company-0-fk_investor': 10,
        }, prefix='parent-company')
        self.assertEqual(True, is_equal(form_1, form_2))

    def test_is_equal_with_form_changed(self):
        form_1 = BaseInvestorForm(data={
            'name': 'Test investor #1'
        })
        form_2 = BaseInvestorForm(data={
            'name': 'Test investor #2'
        })
        self.assertEqual(False, is_equal(form_1, form_2))

    def test_is_equal_with_form_not_changed(self):
        form_1 = BaseInvestorForm(data={
            'name': 'Test investor #1'
        })
        form_2 = BaseInvestorForm(data={
            'name': 'Test investor #1'
        })
        self.assertEqual(True, is_equal(form_1, form_2))

    def test_is_equal_with_formset_diff_count(self):
        form_1 = ParentCompanyFormSet(data={
            'parent-company-TOTAL_FORMS': 1,
            'parent-company-INITIAL_FORMS': 0,
            'parent-company-MIN_NUM_FORMS': 1,
            'parent-company-MAX_NUM_FORMS': 1,
            'parent-company-0-id': 1,
            'parent-company-0-fk_investor': 10,
        }, prefix='parent-company')
        form_2 = ParentCompanyFormSet(data={
            'parent-company-TOTAL_FORMS': 2,
            'parent-company-INITIAL_FORMS': 0,
            'parent-company-MIN_NUM_FORMS': 2,
            'parent-company-MAX_NUM_FORMS': 2,
            'parent-company-0-id': 1,
            'parent-company-0-fk_investor': 20,
            'parent-company-1-fk_investor': 20,
        }, prefix='parent-company')
        self.assertEqual(False, is_equal(form_1, form_2))

    def test_is_equal_with_invalid_form(self):
        form_1 = BaseInvestorForm(data={
            'classification': '99'
        })
        form_2 = BaseInvestorForm(data={
            'classification': '10'
        })
        self.assertEqual(False, is_equal(form_1, form_2))
