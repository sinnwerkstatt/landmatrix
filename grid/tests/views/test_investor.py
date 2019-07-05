from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse

from api.elasticsearch import es_save
from landmatrix.models import HistoricalInvestor
from .base import BaseInvestorTestCase
from grid.views.investor import *


class InvestorListViewTestCase(TestCase):

    @classmethod
    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def setUpClass(cls):
        super().setUpClass()

        fixtures = [
            'countries_and_regions',
            'users_and_groups',
            'status',
            'crops',
            'minerals',
            'animals',
            'investors',
            'activities',
            'activity_involvements',
            'venture_involvements',
        ]
        for fixture in fixtures:
            call_command('loaddata', fixture)
        es_save.create_index(delete=True)
        es_save.index_activity_documents()
        es_save.index_investor_documents()
        es_save.refresh_index()

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_without_group(self):
        response = self.client.get(reverse('investor_list'))
        self.assertEqual(200, response.status_code)
        self.assertEqual('all', response.context.get('group'))
        items = response.context.get('data', {}).get('items')
        self.assertEqual(4, len(items))
        self.assertEqual([1], items[0].get('investor_identifier'))
        self.assertEqual(['Test Investor #1'], items[0].get('name'))
        self.assertEqual(['Cambodia'], items[0].get('fk_country'))
        self.assertEqual(['Private company'], items[0].get('classification'))
        self.assertEqual([3], items[0].get('deal_count'))

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_with_group(self):
        response = self.client.get(reverse('investor_list', kwargs={'group': 'fk_country'}))
        self.assertEqual(200, response.status_code)
        self.assertEqual('fk_country', response.context.get('group_slug'))
        items = response.context.get('data', {}).get('items')
        self.assertEqual(1, len(items))
        expected = {'display': 'Cambodia', 'value': '116'}
        self.assertEqual(expected, items[0].get('fk_country'))
        self.assertEqual([4], items[0].get('investor_count'))

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_with_group_value(self):
        response = self.client.get(reverse('investor_list', kwargs={'group': 'fk_country',
                                                                    'group_value': 'cambodia'}))
        self.assertEqual(200, response.status_code)
        self.assertEqual('fk_country', response.context.get('group_slug'))
        self.assertEqual('cambodia', response.context.get('group_value'))
        items = response.context.get('data', {}).get('items')
        self.assertEqual(4, len(items))
        self.assertEqual([1], items[0].get('investor_identifier'))
        self.assertEqual(['Test Investor #1'], items[0].get('name'))
        self.assertEqual(['Cambodia'], items[0].get('fk_country'))
        self.assertEqual(['Private company'], items[0].get('classification'))


class InvestorCreateViewTestCase(BaseInvestorTestCase):

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_reporter(self):
        data = self.INVESTOR_DATA.copy()
        data.update({
            "action_comment": "Test add investor",
        })
        self.client.login(username='reporter', password='test')
        response = self.client.post(reverse('investor_add'), data)
        self.client.logout()
        self.assertEqual(302, response.status_code, msg='Add investor does not redirect')
        investor = HistoricalInvestor.objects.latest_only().pending().latest()
        self.assertEqual(10, investor.investor_identifier)
        self.assertEqual('Test add investor', investor.action_comment)
        self.assertEqual(HistoricalInvestor.STATUS_PENDING, investor.fk_status_id)

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_editor(self):
        data = self.INVESTOR_DATA.copy()
        data.update({
            "action_comment": "Test add investor",
        })
        self.client.login(username='editor', password='test')
        response = self.client.post(reverse('investor_add'), data)
        self.client.logout()
        self.assertEqual(302, response.status_code, msg='Add investor does not redirect')
        investor = HistoricalInvestor.objects.latest_only().pending().latest()
        self.assertEqual(10, investor.investor_identifier)
        self.assertEqual('Test add investor', investor.action_comment)
        self.assertEqual(HistoricalInvestor.STATUS_PENDING, investor.fk_status_id)

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_administrator(self):
        data = self.INVESTOR_DATA.copy()
        data.update({
            "action_comment": "Test add investor",
            "approve_btn": True
        })
        self.client.login(username='administrator', password='test')
        response = self.client.post(reverse('investor_add'), data)
        self.client.logout()
        self.assertEqual(302, response.status_code, msg='Add investor does not redirect')
        investor = HistoricalInvestor.objects.latest_only().public().latest()
        self.assertEqual(10, investor.investor_identifier)
        self.assertEqual('Test add investor', investor.action_comment)
        self.assertEqual(HistoricalInvestor.STATUS_ACTIVE, investor.fk_status_id)


class InvestorUpdateViewTestCase(BaseInvestorTestCase):

    fixtures = [
        'languages',
        'countries_and_regions',
        'users_and_groups',
        'status',
        'investors',
        'activities',
        'activity_involvements',
        'venture_involvements',
    ]

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_reporter(self):
        data = self.INVESTOR_DATA.copy()
        data.update({
            "action_comment": "Test change investor",
        })
        self.client.login(username='reporter', password='test')
        response = self.client.post(reverse('investor_update', kwargs={'investor_id': 1}), data)
        self.client.logout()
        self.assertEqual(302, response.status_code, msg='Change investor does not redirect')
        investor = HistoricalInvestor.objects.latest_only().pending().latest()
        self.assertEqual(1, investor.investor_identifier)
        self.assertEqual('Test change investor', investor.action_comment)
        self.assertEqual(HistoricalInvestor.STATUS_PENDING, investor.fk_status_id)

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_editor(self):
        data = self.INVESTOR_DATA.copy()
        data.update({
            "action_comment": "Test change investor",
        })
        self.client.login(username='editor', password='test')
        response = self.client.post(reverse('investor_update', kwargs={'investor_id': 1}), data)
        self.client.logout()
        self.assertEqual(302, response.status_code, msg='Change investor does not redirect')
        investor = HistoricalInvestor.objects.latest_only().pending().latest()
        self.assertEqual(1, investor.investor_identifier)
        self.assertEqual('Test change investor', investor.action_comment)
        self.assertEqual(HistoricalInvestor.STATUS_PENDING, investor.fk_status_id)

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_administrator(self):
        data = self.INVESTOR_DATA.copy()
        data.update({
            "action_comment": "Test change investor",
            "approve_btn": True
        })
        self.client.login(username='administrator', password='test')
        response = self.client.post(reverse('investor_update', kwargs={'investor_id': 1}), data)
        self.client.logout()
        self.assertEqual(302, response.status_code, msg='Change investor does not redirect')
        investor = HistoricalInvestor.objects.latest_only().public().latest()
        self.assertEqual(1, investor.investor_identifier)
        self.assertEqual('Test change investor', investor.action_comment)
        self.assertEqual(HistoricalInvestor.STATUS_OVERWRITTEN, investor.fk_status_id)


class InvestorDetailViewTestCase(BaseInvestorTestCase):

    fixtures = [
        'languages',
        'countries_and_regions',
        'users_and_groups',
        'status',
        'investors',
        'activities',
        'activity_involvements',
        'venture_involvements',
    ]

    def test_reporter(self):
        self.client.login(usernamer='reporter', password='test')
        response = self.client.get(reverse('investor_detail', kwargs={'investor_id': 1}))
        self.client.logout()
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response.context.get('investor').investor_identifier)


class InvestorDeleteViewTestCase(BaseInvestorTestCase):

    fixtures = [
        'countries_and_regions',
        'users_and_groups',
        'status',
        'investors',
        'activities',
        'activity_involvements',
        'venture_involvements',
    ]

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_reporter(self):
        data = self.INVESTOR_DATA.copy()
        data.update({
            "action_comment": "Test delete investor",
        })
        self.client.login(username='reporter', password='test')
        response = self.client.post(reverse('investor_delete', kwargs={'investor_id': 1}), data)
        self.client.logout()
        self.assertEqual(302, response.status_code, msg='Delete investor does not redirect')
        investor = HistoricalInvestor.objects.latest_only().to_delete().latest()
        self.assertEqual(1, investor.investor_identifier)
        #self.assertEqual('Test delete investor', investor.action_comment)
        self.assertEqual(HistoricalInvestor.STATUS_TO_DELETE, investor.fk_status_id)

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_editor(self):
        data = self.INVESTOR_DATA.copy()
        data.update({
            "action_comment": "Test delete investor",
        })
        self.client.login(username='editor', password='test')
        response = self.client.post(reverse('investor_delete', kwargs={'investor_id': 1}), data)
        self.client.logout()
        self.assertEqual(302, response.status_code, msg='Delete investor does not redirect')
        investor = HistoricalInvestor.objects.latest_only().to_delete().latest()
        self.assertEqual(1, investor.investor_identifier)
        #self.assertEqual('Test delete investor', investor.action_comment)
        self.assertEqual(HistoricalInvestor.STATUS_TO_DELETE, investor.fk_status_id)

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_administrator(self):
        data = self.INVESTOR_DATA.copy()
        data.update({
            "action_comment": "Test delete investor",
            "approve_btn": True
        })
        self.client.login(username='administrator', password='test')
        response = self.client.post(reverse('investor_delete', kwargs={'investor_id': 1}), data)
        self.client.logout()
        self.assertEqual(302, response.status_code, msg='Delete investor does not redirect')
        investor = HistoricalInvestor.objects.latest_only().deleted().latest()
        self.assertEqual(1, investor.investor_identifier)
        #self.assertEqual('Test delete investor', investor.action_comment)
        self.assertEqual(HistoricalInvestor.STATUS_DELETED, investor.fk_status_id)


class InvestorRecoverViewTestCase(BaseInvestorTestCase):

    fixtures = [
        'countries_and_regions',
        'users_and_groups',
        'status',
        'investors',
        'activities',
        'activity_involvements',
        'venture_involvements',
    ]

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_editor(self):
        data = self.INVESTOR_DATA.copy()
        data.update({
            "action_comment": "Test recover investor",
        })
        self.client.login(username='editor', password='test')
        response = self.client.post(reverse('investor_recover', kwargs={'investor_id': 4}), data)
        self.client.logout()
        self.assertEqual(302, response.status_code, msg='Recover investor does not redirect')
        self.assertEqual(0, HistoricalInvestor.objects.filter(comment="Test recover investor").count())

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_administrator(self):
        data = self.INVESTOR_DATA.copy()
        data.update({
            "action_comment": "Test recover investor",
            "approve_btn": True
        })
        self.client.login(username='administrator', password='test')
        response = self.client.post(reverse('investor_recover', kwargs={'investor_id': 4}), data)
        self.client.logout()
        self.assertEqual(302, response.status_code, msg='Recover investor does not redirect')
        investor = HistoricalInvestor.objects.latest_only().public().latest()
        self.assertEqual(4, investor.investor_identifier)
        #self.assertEqual('Test recover investor', investor.action_comment)
        self.assertEqual(HistoricalInvestor.STATUS_OVERWRITTEN, investor.fk_status_id)
