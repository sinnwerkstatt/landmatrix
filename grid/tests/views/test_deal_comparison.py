from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse

from api.elasticsearch import es_save
from grid.forms.deal_general_form import DealGeneralForm
from grid.forms.deal_spatial_form import DealSpatialFormSet
from grid.views.deal_comparison import *
from landmatrix.models import HistoricalActivity


class GridDealComparisonViewTestCase(TestCase):

    fixtures = [
        'countries_and_regions',
        'users_and_groups',
        'status',
        'activities',
    ]

    def test_get_comparison(self):
        user = get_user_model().objects.get(username='reporter')
        deal_1 = HistoricalActivity.objects.get(id=20)
        deal_2 = HistoricalActivity.objects.get(id=21)
        forms = get_comparison(deal_1, deal_2, user=user)
        self.assertEqual(True, forms[0][2])
        self.assertEqual(False, forms[1][2])

    def test_is_equal_with_formset_changed(self):
        form_1 = DealSpatialFormSet(data={
            'location-TOTAL_FORMS': 1,
            'location-INITIAL_FORMS': 0,
            'location-MIN_NUM_FORMS': 1,
            'location-MAX_NUM_FORMS': 1,
            'location-0-target_country': 104,
        }, prefix='location')
        form_2 = DealSpatialFormSet(data={
            'location-TOTAL_FORMS': 1,
            'location-INITIAL_FORMS': 0,
            'location-MIN_NUM_FORMS': 1,
            'location-MAX_NUM_FORMS': 1,
            'location-0-target_country': 116,
        }, prefix='location')
        self.assertEqual(False, is_equal(form_1, form_2))

    def test_is_equal_with_formset_not_changed(self):
        form_1 = DealSpatialFormSet(data={
            'location-TOTAL_FORMS': 1,
            'location-INITIAL_FORMS': 0,
            'location-MIN_NUM_FORMS': 1,
            'location-MAX_NUM_FORMS': 1,
            'location-0-target_country': 104,
        }, prefix='location')
        form_2 = DealSpatialFormSet(data={
            'location-TOTAL_FORMS': 1,
            'location-INITIAL_FORMS': 0,
            'location-MIN_NUM_FORMS': 1,
            'location-MAX_NUM_FORMS': 1,
            'location-0-target_country': 104,
        }, prefix='location')
        self.assertEqual(True, is_equal(form_1, form_2))

    def test_is_equal_with_form_changed(self):
        form_1 = DealGeneralForm(data={
            'intended_size': '0.0'
        })
        form_2 = DealGeneralForm(data={
            'intended_size': '1.0'
        })
        self.assertEqual(False, is_equal(form_1, form_2))

    def test_is_equal_with_form_not_changed(self):
        form_1 = DealGeneralForm(data={
            'intended_size': '0.0'
        })
        form_2 = DealGeneralForm(data={
            'intended_size': '0.0'
        })
        self.assertEqual(True, is_equal(form_1, form_2))


class DealComparisonViewTestCase(TestCase):

    fixtures = [
        'countries_and_regions',
        'users_and_groups',
        'status',
        'crops',
        'animals',
        'minerals',
        'investors',
        'activities',
        'activity_involvements',
        'venture_involvements',
    ]

    def assert_comparison(self, context_data):
        deals = context_data.get('deals', [])
        self.assertEqual(2, len(deals))
        self.assertEqual(21, deals[0].pk)
        self.assertEqual(20, deals[1].pk)
        forms = context_data.get('forms', [])
        self.assertEqual(True, forms[0][2])
        self.assertEqual(False, forms[1][2])

    def test_with_one_activity(self):
        self.client.login(username='reporter', password='test')
        response = self.client.get(reverse('compare_deals', kwargs={'activity_1': '21'}))
        self.client.logout()
        self.assertEqual(200, response.status_code)
        self.assert_comparison(response.context_data)

    def test_with_reporter(self):
        self.client.login(username='reporter', password='test')
        response = self.client.get(reverse('compare_deals', kwargs={'activity_1': '21', 'activity_2': '20'}))
        self.client.logout()
        self.assertEqual(200, response.status_code)
        self.assert_comparison(response.context_data)

    def test_with_editor(self):
        self.client.login(username='editor', password='test')
        response = self.client.get(reverse('compare_deals', kwargs={'activity_1': '21', 'activity_2': '20'}))
        self.client.logout()
        self.assertEqual(200, response.status_code)
        self.assert_comparison(response.context_data)

    def test_with_administrator(self):
        self.client.login(username='administrator', password='test')
        response = self.client.get(reverse('compare_deals', kwargs={'activity_1': '21', 'activity_2': '20'}))
        self.client.logout()
        self.assertEqual(200, response.status_code)
        self.assert_comparison(response.context_data)
