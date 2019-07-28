from django.contrib.auth import get_user_model
from django.contrib.messages.storage.fallback import FallbackStorage
from django.core.management import call_command
from django.http import QueryDict
from django.test import TestCase, override_settings, RequestFactory
from django.urls import reverse

from api.elasticsearch import es_save
from landmatrix.models import HistoricalInvestor
from .base import BaseInvestorTestCase, PermissionsTestCaseMixin
from grid.views.investor import *


class InvestorListViewTestCase(PermissionsTestCaseMixin,
                               TestCase):

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
        self.assertGreater(len(items), 0)
        self.assertEqual([1], items[0].get('investor_identifier'))
        self.assertEqual(['Test Investor #1'], items[0].get('name'))
        self.assertEqual(['Cambodia'], items[0].get('fk_country'))
        self.assertEqual(['Private company'], items[0].get('classification'))
        self.assertGreater(items[0].get('deal_count')[0], 0)

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_with_group_fk_country(self):
        response = self.client.get(reverse('investor_list', kwargs={'group': 'fk_country'}))
        self.assertEqual(200, response.status_code)
        self.assertEqual('fk_country', response.context.get('group_slug'))
        items = response.context.get('data', {}).get('items')
        self.assertGreater(len(items), 0)
        expected = {'display': 'Andorra', 'value': '20'}
        self.assertEqual(expected, items[0].get('fk_country'))
        self.assertGreater(items[0].get('investor_count')[0], 0)

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_with_group_role(self):
        response = self.client.get(reverse('investor_list', kwargs={'group': 'role'}))
        self.assertEqual(200, response.status_code)
        self.assertEqual('role', response.context.get('group_slug'))
        items = response.context.get('data', {}).get('items')
        self.assertGreater(len(items), 0)
        expected = {r[1] for r in InvestorBase.ROLE_CHOICES}
        self.assertEqual(expected, set(i.get('roles', {}).get('display') for i in items))

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_with_group_value(self):
        response = self.client.get(reverse('investor_list', kwargs={'group': 'fk_country',
                                                                    'group_value': 'cambodia'}))
        self.assertEqual(200, response.status_code)
        self.assertEqual('fk_country', response.context.get('group_slug'))
        self.assertEqual('cambodia', response.context.get('group_value'))
        items = response.context.get('data', {}).get('items')
        self.assertGreater(len(items), 0)
        self.assertEqual([1], items[0].get('investor_identifier'))
        self.assertEqual(['Test Investor #1'], items[0].get('name'))
        self.assertEqual(['Cambodia'], items[0].get('fk_country'))
        self.assertEqual(['Private company'], items[0].get('classification'))

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_with_admin(self):
        self.client.login(username='administrator', password='test')
        response = self.client.get(reverse('investor_list'))
        self.client.logout()
        self.assertEqual(200, response.status_code)
        self.assertEqual('all', response.context.get('group'))
        items = response.context.get('data', {}).get('items')
        self.assertGreater(len(items), 0)

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_with_parent_filters(self):
        request = RequestFactory().get(reverse('investor_list'))
        request.user = get_user_model().objects.get(username='reporter')
        request.session = {
            'investor:filters': {
                "filter_1": {
                    "name": "filter_1",
                    "variable": "parent_stakeholder_name",
                    "operator": "is",
                    "value": "Test investor #3",
                    "label": "Parent company Name",
                    "key": None,
                    "display_value": "Test investor #3"
                },
                "filter_2": {
                    "name": "filter_2",
                    "variable": "tertiary_investor_name",
                    "operator": "is",
                    "value": "Test investor #10",
                    "label": "Tertiary investor Name",
                    "key": None,
                    "display_value": "Test investor #10"
                }
            }
        }
        response = InvestorListView.as_view()(request)
        response = response.render()
        self.assertEqual(200, response.status_code)
        self.assertEqual('all', response.context_data.get('group'))
        items = response.context_data.get('data', {}).get('items')
        self.assertGreater(len(items), 0)
        self.assertEqual([1], items[0].get('investor_identifier'))
        self.assertEqual(['Test Investor #1'], items[0].get('name'))
        self.assertEqual(['Cambodia'], items[0].get('fk_country'))
        self.assertEqual(['Private company'], items[0].get('classification'))
        self.assertGreater(items[0].get('deal_count')[0], 0)

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_with_status_filter(self):
        request = RequestFactory().get(reverse('investor_list'))
        request.user = get_user_model().objects.get(username='administrator')
        request.session = {}
        request.GET = QueryDict('status=1&status=2&status=3')
        response = InvestorListView.as_view()(request)
        response = response.render()
        self.assertEqual(200, response.status_code)
        self.assertEqual('all', response.context_data.get('group'))
        items = response.context_data.get('data', {}).get('items')
        self.assertGreater(len(items), 0)
        self.assertEqual([1], items[0].get('investor_identifier'))
        self.assertEqual(['Test Investor #1'], items[0].get('name'))
        self.assertEqual(['Cambodia'], items[0].get('fk_country'))
        self.assertEqual(['Private company'], items[0].get('classification'))
        self.assertGreater(items[0].get('deal_count')[0], 0)


class InvestorCreateViewTestCase(BaseInvestorTestCase):

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_get(self):
        self.client.login(username='reporter', password='test')
        response = self.client.get(reverse('investor_add'))
        self.client.logout()
        self.assertEqual(200, response.status_code)

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
        self.assertEqual('Test add investor', investor.action_comment)
        self.assertEqual(HistoricalInvestor.STATUS_ACTIVE, investor.fk_status_id)

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_invalid(self):
        data = self.INVESTOR_DATA.copy()
        data['fk_country'] = '9999'
        self.client.login(username='reporter', password='test')
        response = self.client.post(reverse('investor_add'), data)
        self.client.logout()
        self.assertEqual(200, response.status_code)

        messages = list(response.context.get('messages'))
        self.assertGreater(len(messages), 0)
        self.assertEqual('Please correct the error below.', messages[-1].message)

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_popup(self):
        data = self.INVESTOR_DATA.copy()
        request = RequestFactory().post(reverse('investor_add'), data)
        request.user = get_user_model().objects.get(username='reporter')
        request.GET = QueryDict('popup=1')
        request.POST = data
        request.session = {}
        request._messages = FallbackStorage(request)
        response = InvestorCreateView.as_view()(request)
        self.assertEqual(200, response.status_code)
        self.assertIn(b'opener.dismissAddInvestorPopup', response.content)

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_with_parent_id(self):
        data = self.INVESTOR_DATA.copy()
        request = RequestFactory().post(reverse('investor_add'), data)
        request.user = get_user_model().objects.get(username='reporter')
        request.GET = QueryDict('parent_id=10')
        request.POST = data
        request.session = {}
        request._messages = FallbackStorage(request)
        response = InvestorCreateView.as_view()(request)
        self.assertEqual(302, response.status_code)

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_reject(self):
        data = self.INVESTOR_DATA.copy()
        data.update({
            "tg_action_comment": "Test add investor",
            "reject_btn": "on",
        })
        self.client.login(username='administrator', password='test')
        response = self.client.post(reverse('investor_add'), data)
        self.client.logout()
        self.assertEqual(302, response.status_code, msg='Add deal does not redirect')
        investor = HistoricalInvestor.objects.latest_only().rejected().latest()
        self.assertEqual('Test comment', investor.comment)
        self.assertEqual(HistoricalInvestor.STATUS_REJECTED, investor.fk_status_id)

    def test_parent_company_role(self):
        data = self.INVESTOR_DATA.copy()
        data.update({
            "tg_action_comment": "Test add investor",
        })
        request = RequestFactory().post(reverse('investor_add'), data)
        request.user = get_user_model().objects.get(username='reporter')
        request.GET = QueryDict('role=parent_company')
        request.POST = data
        request.session = {}
        request._messages = FallbackStorage(request)
        response = InvestorCreateView.as_view()(request)
        self.assertEqual(302, response.status_code)

    def test_tertiary_investor_lender_role(self):
        data = self.INVESTOR_DATA.copy()
        data.update({
            "tg_action_comment": "Test add investor",
        })
        request = RequestFactory().post(reverse('investor_add'), data)
        request.user = get_user_model().objects.get(username='reporter')
        request.GET = QueryDict('role=parent_investor')
        request.POST = data
        request.session = {}
        request._messages = FallbackStorage(request)
        response = InvestorCreateView.as_view()(request)
        self.assertEqual(302, response.status_code)


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
    def test_get(self):
        self.client.login(username='reporter', password='test')
        response = self.client.get(reverse('investor_update', kwargs={'investor_id': 1}))
        self.client.logout()
        self.assertEqual(200, response.status_code)

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
    def test_editor_reject(self):
        data = self.INVESTOR_DATA.copy()
        data.update({
            "action_comment": "Test change investor",
            "reject_btn": "on",
        })
        self.client.login(username='administrator', password='test')
        response = self.client.post(reverse('investor_update', kwargs={'investor_id': 3, 'history_id': 31}), data)
        self.client.logout()
        self.assertEqual(302, response.status_code, msg='Change investor does not redirect')
        investor = HistoricalInvestor.objects.get(id=31)
        self.assertEqual(3, investor.investor_identifier)
        self.assertEqual(HistoricalInvestor.STATUS_REJECTED, investor.fk_status_id)

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

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_invalid(self):
        data = self.INVESTOR_DATA.copy()
        data['fk_country'] = '9999'
        self.client.login(username='reporter', password='test')
        response = self.client.post(reverse('investor_update', kwargs={'investor_id': 1}), data)
        self.client.logout()
        self.assertEqual(200, response.status_code)

        messages = list(response.context.get('messages'))
        self.assertGreater(len(messages), 0)
        self.assertEqual('Please correct the error below.', messages[-1].message)

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_reporter_pending(self):
        data = self.INVESTOR_DATA.copy()
        data.update({
            "action_comment": "Test change investor",
        })
        self.client.login(username='reporter', password='test')
        response = self.client.post(reverse('investor_update', kwargs={'investor_id': 2, 'history_id': 20}), data)
        self.client.logout()
        self.assertEqual(302, response.status_code)
        self.assertEqual('/investor/2/20/', response.url)

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_does_not_exist(self):
        self.client.login(username='editor', password='test')
        response = self.client.get(reverse('investor_update', kwargs={'investor_id': 123}))
        self.client.logout()
        self.assertEqual(404, response.status_code)

    def test_with_history_id(self):
        data = self.INVESTOR_DATA.copy()
        data.update({
            "action_comment": "Test change investor",
        })
        self.client.login(username='editor', password='test')
        response = self.client.post(reverse('investor_update', kwargs={'investor_id': 1, 'history_id': 10}), data)
        self.client.logout()
        self.assertEqual(302, response.status_code, msg='Change investor does not redirect')
        investor = HistoricalInvestor.objects.latest_only().pending().latest()
        self.assertEqual(1, investor.investor_identifier)
        self.assertEqual('Test change investor', investor.action_comment)
        self.assertEqual(HistoricalInvestor.STATUS_PENDING, investor.fk_status_id)

    def test_not_editable(self):
        self.client.login(username='editor', password='test')
        response = self.client.get(reverse('investor_update', kwargs={'investor_id': 3, 'history_id': 30}))
        self.client.logout()
        self.assertEqual(302, response.status_code)

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_popup(self):
        data = self.INVESTOR_DATA.copy()
        data.update({
            "action_comment": "Test change investor",
        })
        request = RequestFactory().post(reverse('investor_update', kwargs={'investor_id': 1}), data)
        request.user = get_user_model().objects.get(username='reporter')
        request.GET = QueryDict('popup=1')
        request.POST = data
        request.session = {}
        request._messages = FallbackStorage(request)
        response = InvestorUpdateView.as_view()(request, investor_id=1)
        self.assertEqual(200, response.status_code)
        self.assertIn(b'opener.dismissChangeInvestorPopup', response.content)


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

    def test_with_anonymous(self):
        response = self.client.get(reverse('investor_detail', kwargs={'investor_id': 1}))
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response.context.get('investor').investor_identifier)

    def test_with_anonymous_not_public(self):
        response = self.client.get(reverse('investor_detail', kwargs={'investor_id': 4}))
        self.assertEqual(404, response.status_code)

    def test_reporter(self):
        self.client.login(username='reporter', password='test')
        response = self.client.get(reverse('investor_detail', kwargs={'investor_id': 1}))
        self.client.logout()
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response.context.get('investor').investor_identifier)

    def test_deleted(self):
        self.client.login(username='editor', password='test')
        response = self.client.get(reverse('investor_detail', kwargs={'investor_id': 4}))
        self.client.logout()
        self.assertEqual(404, response.status_code)

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_does_not_exist(self):
        self.client.login(username='editor', password='test')
        response = self.client.get(reverse('investor_detail', kwargs={'investor_id': 123}))
        self.client.logout()
        self.assertEqual(404, response.status_code)

    def test_with_history_id(self):
        self.client.login(username='editor', password='test')
        response = self.client.get(reverse('investor_detail', kwargs={'investor_id': 1, 'history_id': 10}))
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
    def test_get(self):
        self.client.login(username='editor', password='test')
        response = self.client.get(reverse('investor_delete', kwargs={'investor_id': 1}))
        self.client.logout()
        self.assertEqual(302, response.status_code)

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

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_does_not_exist(self):
        data = self.INVESTOR_DATA.copy()
        data.update({
            "action_comment": "Test delete investor",
        })
        self.client.login(username='editor', password='test')
        response = self.client.post(reverse('investor_delete', kwargs={'investor_id': 123}))
        self.client.logout()
        self.assertEqual(404, response.status_code)

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_already_deleted(self):
        data = self.INVESTOR_DATA.copy()
        data.update({
            "action_comment": "Test delete investor",
        })
        self.client.login(username='editor', password='test')
        response = self.client.post(reverse('investor_delete', kwargs={'investor_id': 4}), data)
        self.client.logout()
        self.assertEqual(404, response.status_code)


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
    def test_get(self):
        self.client.login(username='editor', password='test')
        response = self.client.get(reverse('investor_recover', kwargs={'investor_id': 4}))
        self.client.logout()
        self.assertEqual(302, response.status_code)

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

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_does_not_exist(self):
        self.client.login(username='editor', password='test')
        response = self.client.get(reverse('investor_recover', kwargs={'investor_id': 123}))
        self.client.logout()
        self.assertEqual(404, response.status_code)

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_not_deleted(self):
        self.client.login(username='editor', password='test')
        response = self.client.get(reverse('investor_recover', kwargs={'investor_id': 1}))
        self.client.logout()
        self.assertEqual(404, response.status_code)