from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse

from api.elasticsearch import es_save
from landmatrix.models import HistoricalActivity
from .base import BaseDealTestCase
from grid.views.deal import *


class DealListViewTestCase(TestCase):

    @classmethod
    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def setUpClass(cls):
        super().setUpClass()

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
        for fixture in fixtures:
            call_command('loaddata', fixture)
        es_save.create_index(delete=True)
        es_save.index_activity_documents()
        es_save.index_investor_documents()
        es_save.refresh_index()

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_without_group(self):
        response = self.client.get(reverse('data'))
        self.assertEqual(200, response.status_code)
        self.assertEqual('all', response.context.get('group'))
        items = response.context.get('data', {}).get('items')
        self.assertEqual(3, len(items))
        self.assertEqual([1], items[0].get('activity_identifier'))
        self.assertEqual(['Myanmar'], items[0].get('target_country'))
        self.assertEqual([{'id': '1', 'name': 'Test Investor 1'}], items[0].get('top_investors', []))
        self.assertEqual(3, len(items[0].get('intention', [None])[0]))
        self.assertEqual([1000], items[0].get('deal_size'))

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_with_group(self):
        response = self.client.get(reverse('deal_list', kwargs={'group': 'target_country'}))
        self.assertEqual(200, response.status_code)
        self.assertEqual('target_country', response.context.get('group'))
        items = response.context.get('data', {}).get('items')
        self.assertEqual(1, len(items))
        self.assertEqual('Myanmar', items[0].get('target_country', {}).get('display'))
        self.assertEqual(['Asia'], items[0].get('target_region'))
        self.assertEqual(2, len(items[0].get('intention', [])))
        self.assertEqual([3], items[0].get('deal_count'))
        self.assertEqual([3000], items[0].get('deal_size'))

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_with_group_value(self):
        response = self.client.get(reverse('deal_list', kwargs={'group': 'target_country',
                                                                'group_value': 'myanmar'}))
        self.assertEqual(200, response.status_code)
        self.assertEqual('target_country', response.context.get('group'))
        self.assertEqual('myanmar', response.context.get('group_value'))
        items = response.context.get('data', {}).get('items')
        self.assertEqual(3, len(items))
        self.assertEqual([1], items[0].get('activity_identifier'))
        self.assertEqual(['Myanmar'], items[0].get('target_country'))
        self.assertEqual([{'id': '1', 'name': 'Test Investor 1'}], items[0].get('top_investors', []))
        self.assertEqual(3, len(items[0].get('intention', [None])[0]))
        self.assertEqual([1000], items[0].get('deal_size'))


class DealCreateViewTestCase(BaseDealTestCase):

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_reporter(self):
        data = self.DEAL_DATA.copy()
        data.update({
            "tg_action_comment": "Test add deal",
        })
        self.client.login(username='reporter', password='test')
        response = self.client.post(reverse('add_deal'), data)
        self.client.logout()
        self.assertEqual(302, response.status_code, msg='Add deal does not redirect')
        activity = HistoricalActivity.objects.latest_only().pending().latest()
        self.assertEqual(1, activity.activity_identifier)
        self.assertEqual('Test add deal', activity.comment)
        self.assertEqual(HistoricalActivity.STATUS_PENDING, activity.fk_status_id)

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_editor(self):
        data = self.DEAL_DATA.copy()
        data.update({
            "tg_action_comment": "Test add deal",
        })
        self.client.login(username='editor', password='test')
        response = self.client.post(reverse('add_deal'), data)
        self.client.logout()
        self.assertEqual(302, response.status_code, msg='Add deal does not redirect')
        activity = HistoricalActivity.objects.latest_only().pending().latest()
        self.assertEqual(1, activity.activity_identifier)
        self.assertEqual('Test add deal', activity.comment)
        self.assertEqual(HistoricalActivity.STATUS_PENDING, activity.fk_status_id)

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_administrator(self):
        data = self.DEAL_DATA.copy()
        data.update({
            "operational_stakeholder": self.INVESTOR_CREATED,
            "tg_action_comment": "Test add deal",
            "approve_btn": True
        })
        self.client.login(username='administrator', password='test')
        response = self.client.post(reverse('add_deal'), data)
        self.client.logout()
        self.assertEqual(302, response.status_code, msg='Add deal does not redirect')
        activity = HistoricalActivity.objects.latest_only().public().latest()
        self.assertEqual(1, activity.activity_identifier)
        self.assertEqual('Test add deal', activity.comment)
        self.assertEqual(HistoricalActivity.STATUS_ACTIVE, activity.fk_status_id)


class DealUpdateViewTestCase(BaseDealTestCase):

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
        data = self.DEAL_DATA.copy()
        data.update({
            "tg_action_comment": "Test change deal",
        })
        self.client.login(username='reporter', password='test')
        response = self.client.post(reverse('change_deal', kwargs={'deal_id': 1}), data)
        self.client.logout()
        self.assertEqual(302, response.status_code, msg='Change deal does not redirect')
        activity = HistoricalActivity.objects.latest_only().pending().latest()
        self.assertEqual(1, activity.activity_identifier)
        self.assertEqual('Test change deal', activity.comment)
        self.assertEqual(HistoricalActivity.STATUS_PENDING, activity.fk_status_id)

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_editor(self):
        data = self.DEAL_DATA.copy()
        data.update({
            "tg_action_comment": "Test change deal",
        })
        self.client.login(username='editor', password='test')
        response = self.client.post(reverse('change_deal', kwargs={'deal_id': 1}), data)
        self.client.logout()
        self.assertEqual(302, response.status_code, msg='Change deal does not redirect')
        activity = HistoricalActivity.objects.latest_only().pending().latest()
        self.assertEqual(1, activity.activity_identifier)
        self.assertEqual('Test change deal', activity.comment)
        self.assertEqual(HistoricalActivity.STATUS_PENDING, activity.fk_status_id)

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_administrator(self):
        data = self.DEAL_DATA.copy()
        data.update({
            "operational_stakeholder": self.INVESTOR_CREATED,
            "tg_action_comment": "Test change deal",
            "approve_btn": True
        })
        self.client.login(username='administrator', password='test')
        response = self.client.post(reverse('change_deal', kwargs={'deal_id': 1}), data)
        self.client.logout()
        self.assertEqual(302, response.status_code, msg='Change deal does not redirect')
        activity = HistoricalActivity.objects.latest_only().public().latest()
        self.assertEqual(1, activity.activity_identifier)
        self.assertEqual('Test change deal', activity.comment)
        self.assertEqual(HistoricalActivity.STATUS_OVERWRITTEN, activity.fk_status_id)


class DealDetailViewTestCase(BaseDealTestCase):

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
        response = self.client.get(reverse('deal_detail', kwargs={'deal_id': 1}))
        self.client.logout()
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response.context.get('activity').activity_identifier)


class DealDeleteViewTestCase(BaseDealTestCase):

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
        data = self.DEAL_DATA.copy()
        data.update({
            "tg_action_comment": "Test delete deal",
        })
        self.client.login(username='reporter', password='test')
        response = self.client.post(reverse('delete_deal', kwargs={'deal_id': 1}), data)
        self.client.logout()
        self.assertEqual(302, response.status_code, msg='Delete deal does not redirect')
        activity = HistoricalActivity.objects.latest_only().to_delete().latest()
        self.assertEqual(1, activity.activity_identifier)
        #self.assertEqual('Test delete deal', activity.comment)
        self.assertEqual(HistoricalActivity.STATUS_TO_DELETE, activity.fk_status_id)

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_editor(self):
        data = self.DEAL_DATA.copy()
        data.update({
            "tg_action_comment": "Test delete deal",
        })
        self.client.login(username='editor', password='test')
        response = self.client.post(reverse('delete_deal', kwargs={'deal_id': 1}), data)
        self.client.logout()
        self.assertEqual(302, response.status_code, msg='Delete deal does not redirect')
        activity = HistoricalActivity.objects.latest_only().to_delete().latest()
        self.assertEqual(1, activity.activity_identifier)
        #self.assertEqual('Test delete deal', activity.comment)
        self.assertEqual(HistoricalActivity.STATUS_TO_DELETE, activity.fk_status_id)

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_administrator(self):
        data = self.DEAL_DATA.copy()
        data.update({
            "tg_action_comment": "Test delete deal",
            "approve_btn": True
        })
        self.client.login(username='administrator', password='test')
        response = self.client.post(reverse('delete_deal', kwargs={'deal_id': 1}), data)
        self.client.logout()
        self.assertEqual(302, response.status_code, msg='Delete deal does not redirect')
        activity = HistoricalActivity.objects.latest_only().deleted().latest()
        self.assertEqual(1, activity.activity_identifier)
        #self.assertEqual('Test delete deal', activity.comment)
        self.assertEqual(HistoricalActivity.STATUS_DELETED, activity.fk_status_id)


class DealRecoverViewTestCase(BaseDealTestCase):

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
        data = self.DEAL_DATA.copy()
        data.update({
            "tg_action_comment": "Test recover deal",
        })
        self.client.login(username='editor', password='test')
        response = self.client.post(reverse('recover_deal', kwargs={'deal_id': 4}), data)
        self.client.logout()
        self.assertEqual(302, response.status_code, msg='Recover deal does not redirect')
        self.assertEqual(0, HistoricalActivity.objects.filter(comment="Test recover deal").count())

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_administrator(self):
        data = self.DEAL_DATA.copy()
        data.update({
            "tg_action_comment": "Test recover deal",
            "approve_btn": True
        })
        self.client.login(username='administrator', password='test')
        response = self.client.post(reverse('recover_deal', kwargs={'deal_id': 4}), data)
        self.client.logout()
        self.assertEqual(302, response.status_code, msg='Recover deal does not redirect')
        activity = HistoricalActivity.objects.latest_only().public().latest()
        self.assertEqual(4, activity.activity_identifier)
        #self.assertEqual('Test recover deal', activity.comment)
        self.assertEqual(HistoricalActivity.STATUS_OVERWRITTEN, activity.fk_status_id)


class DealTestCase(TestCase):

    fixtures = [
        'countries_and_regions',
        'users_and_groups',
        'status',
        'investors',
        'activities',
        'activity_involvements',
        'venture_involvements',
    ]

    def test_get_forms(self):
        activity = HistoricalActivity.objects.latest_only().public().latest()
        user = get_user_model().objects.get(username='reporter')
        forms = get_forms(activity, user)
        self.assertEqual(14, len(forms))

    def test_get_form(self):
        activity = HistoricalActivity.objects.latest_only().public().latest()
        form_tuple = (DealActionCommentForm.Meta.name, DealActionCommentForm)
        form = get_form(activity, form_tuple)
        self.assertIsInstance(form, DealActionCommentForm)
        self.assertEqual({'tg_action_comment': ['']}, form.initial)
