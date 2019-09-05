from io import BytesIO

from django.contrib.auth.models import AnonymousUser
from django.http import Http404
from django.test import override_settings, tag
from django.urls import reverse
from openpyxl import load_workbook

from apps.editor.views import ApproveInvestorDeleteView, ManageDeletesView, ManageForUserView
from apps.grid.tests.views.base import BaseInvestorTestCase
from apps.grid.views.export import ExportView
from apps.grid.views.investor import DeleteInvestorView, InvestorDetailView
from apps.landmatrix.models import HistoricalInvestor


@tag('integration')
class TestInvestorDelete(BaseInvestorTestCase):
    
    fixtures = [
        'countries_and_regions',
        'users_and_groups',
        'status',
        'investors',
        'activities',
        'activity_involvements',
        'venture_involvements',
    ]

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test', CELERY_ALWAYS_EAGER=True)
    def assert_investor_deleted(self, investor, user=None):
        # Check if investor is NOT public
        url = reverse('investor_detail', kwargs={'investor_id': investor.investor_identifier})
        request = self.mock_request('get', url, AnonymousUser())
        try:
            response = InvestorDetailView.as_view()(request, investor_id=investor.investor_identifier)
        except Http404:
            pass
        else:
            self.fail("Investor still exists after deletion")

        # Check if investor is in latest deleted log
        #FIXME: Check with concept
        #url = reverse('log_deleted')
        #request = self.mock_request('get', url, user)
        #response = LogDeletedView.as_view()(request)
        #self.assertEqual(200, response.status_code, msg='Latest Deleted Log does not work')
        #self.assert_investor_in_list(response, investor)

        # Check if investor is NOT in elasticsearch/export
        self.run_commit_hooks()
        url = reverse('export', kwargs={'format': 'xls'})
        request = self.mock_request('get', url, AnonymousUser())
        response = ExportView.as_view()(request, format='xls')
        self.assertEqual(200, response.status_code, msg='Export does not work')
        wb = load_workbook(BytesIO(response.content), read_only=True)
        ws = wb['Investors']
        investor_identifiers = [row[0].value for row in ws.rows]
        # FIXME
        #if '#%s' % str(investor.investor_identifier) in investor_identifiers:
        #    self.fail('Investor still appears in export after deletion (checked XLS only)')

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test', CELERY_ALWAYS_EAGER=True)
    def test_reporter(self):
        # Delete investor as reporter
        investor = HistoricalInvestor.objects.latest_only().public().latest()
        data = {
            # Action comment
            "tg_action_comment": "Test delete investor",
        }
        url = reverse('investor_delete', kwargs={'investor_id': investor.investor_identifier})
        request = self.mock_request('post', url, 'reporter', data=data)
        response = DeleteInvestorView.as_view()(request, investor_id=investor.investor_identifier)
        #if response.status_code == 200:
        #    # For debugging purposes
        #    errors = list(filter(None, [form.errors or None for form in response.context_data['forms']]))
        #    self.assertEqual([], errors)
        self.assertEqual(302, response.status_code, msg='Delete investor by Reporter does not redirect')

        investor = HistoricalInvestor.objects.latest_only().to_delete().latest()

        # Check if investor appears in my investors section of reporter
        url = reverse('manage_for_user')
        request = self.mock_request('get', url, 'reporter')
        response = ManageForUserView.as_view()(request)
        self.assertEqual(200, response.status_code, msg='Manage My Deals/Investors of Reporter does not work')
        self.assert_investor_in_list(response, investor)

        # Check if investor appears in manage section of administrator
        url = reverse('manage_pending_deletes')
        # Admin without country/region
        request = self.mock_request('get', url, 'administrator')
        response = ManageDeletesView.as_view()(request)
        self.assertEqual(200, response.status_code, msg='Manage Pending Deletes of Administrator does not work')
        self.assert_investor_in_list(response, investor)
        # Admin with country
        request = self.mock_request('get', url, 'administrator-myanmar')
        response = ManageDeletesView.as_view()(request)
        self.assertEqual(200, response.status_code, msg='Manage Pending Deletes of Administrator does not work')
        self.assert_investor_in_list(response, investor)
        # Admin with region
        request = self.mock_request('get', url, 'administrator-asia')
        response = ManageDeletesView.as_view()(request)
        self.assertEqual(200, response.status_code, msg='Manage Pending Deletes of Administrator does not work')
        self.assert_investor_in_list(response, investor)

        # Check if investor appears in manage section of editor
        url = reverse('manage_pending_deletes')
        # Editor without country/region
        request = self.mock_request('get', url, 'editor')
        response = ManageDeletesView.as_view()(request)
        self.assertEqual(200, response.status_code, msg='Manage Pending Deletes of Editor does not work')
        self.assert_investor_in_list(response, investor)
        # Editor with country
        request = self.mock_request('get', url, 'editor-myanmar')
        response = ManageDeletesView.as_view()(request)
        self.assertEqual(200, response.status_code, msg='Manage Pending Deletes of Editor does not work')
        self.assert_investor_in_list(response, investor, role='reporter')
        # Editor with region
        request = self.mock_request('get', url, 'editor-asia')
        response = ManageDeletesView.as_view()(request)
        self.assertEqual(200, response.status_code, msg='Manage Pending Deletes of Editor does not work')
        self.assert_investor_in_list(response, investor, role='reporter')

        # Approve investor as editor
        data = {
            # Action comment
            "tg_action_comment": "Test approve by Editor",
        }
        url = reverse('manage_approve_delete_investor', kwargs={'id': investor.id})
        request = self.mock_request('post', url, 'editor', data=data)
        response = ApproveInvestorDeleteView.as_view()(request, id=investor.id)
        #if response.status_code == 200:
        #    # For debugging purposes
        #    errors = list(filter(None, [form.errors or None for form in response.context_data['forms']]))
        #    self.assertEqual([], errors)
        self.assertEqual(302, response.status_code, msg='Approve investor by Editor does not redirect')

        # Check if investor appears in manage section of administrator
        url = reverse('manage_pending_deletes')
        # Administrator without country/region
        request = self.mock_request('get', url, 'administrator')
        response = ManageDeletesView.as_view()(request)
        self.assertEqual(200, response.status_code, msg='Manage Pending Deletes of Administrator does not work')
        self.assert_investor_in_list(response, investor)
        # Administrator with country
        request = self.mock_request('get', url, 'administrator-myanmar')
        response = ManageDeletesView.as_view()(request)
        self.assertEqual(200, response.status_code, msg='Manage Pending Deletes of Administrator does not work')
        self.assert_investor_in_list(response, investor, role='reporter')
        # Administrator with region
        request = self.mock_request('get', url, 'administrator-asia')
        response = ManageDeletesView.as_view()(request)
        self.assertEqual(200, response.status_code, msg='Manage Pending Deletes of Administrator does not work')
        self.assert_investor_in_list(response, investor, role='reporter')

        # Approve investor as administrator
        data = {
            # Action comment
            "tg_action_comment": "Test approve by Administrator",
        }
        url = reverse('manage_approve_delete_investor', kwargs={'id': investor.id})
        request = self.mock_request('post', url, 'administrator', data=data)
        response = ApproveInvestorDeleteView.as_view()(request, id=investor.id)
        #if response.status_code == 200:
        #    # For debugging purposes
        #    errors = list(filter(None, [form.errors or None for form in response.context_data['forms']]))
        #    self.assertEqual([], errors)
        self.assertEqual(302, response.status_code, msg='Approve investor by Administrator does not redirect')

        self.assert_investor_deleted(investor, self.users['reporter'])

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test', CELERY_ALWAYS_EAGER=True)
    def test_editor(self):
        # Delete investor as editor
        investor = HistoricalInvestor.objects.latest_only().public().latest()
        data = {
            # Action comment
            "tg_action_comment": "Test delete investor",
        }
        url = reverse('investor_delete', kwargs={'investor_id': investor.investor_identifier})
        request = self.mock_request('post', url, 'editor', data=data)
        response = DeleteInvestorView.as_view()(request, investor_id=investor.investor_identifier)
        #if response.status_code == 200:
        #    # For debugging purposes
        #    errors = list(filter(None, [form.errors or None for form in response.context_data['forms']]))
        #    self.assertEqual([], errors)
        self.assertEqual(302, response.status_code, msg='Delete investor does not redirect')

        investor = HistoricalInvestor.objects.latest_only().to_delete().latest()

        # Check if investor appears in manage section of administrator
        url = reverse('manage_pending_deletes')
        request = self.mock_request('get', url, 'administrator')
        response = ManageDeletesView.as_view()(request)
        self.assertEqual(200, response.status_code, msg='Manage Pending Deletes of Administrator does not work')
        self.assert_investor_in_list(response, investor)
        # Administrator with country
        request = self.mock_request('get', url, 'administrator-myanmar')
        response = ManageDeletesView.as_view()(request)
        self.assertEqual(200, response.status_code, msg='Manage Pending Deletes of Administrator does not work')
        self.assert_investor_in_list(response, investor, role='editor')
        # Administrator with region
        request = self.mock_request('get', url, 'administrator-asia')
        response = ManageDeletesView.as_view()(request)
        self.assertEqual(200, response.status_code, msg='Manage Pending Deletes of Administrator does not work')
        self.assert_investor_in_list(response, investor, role='editor')

        # Approve investor as administrator
        data = {
            # Action comment
            "tg_action_comment": "Test approve by Administrator",
        }
        url = reverse('manage_approve_delete_investor', kwargs={'id': investor.id})
        request = self.mock_request('post', url, 'administrator', data=data)
        response = ApproveInvestorDeleteView.as_view()(request, id=investor.id)
        #if response.status_code == 200:
        #    # For debugging purposes
        #    errors = list(filter(None, [form.errors or None for form in response.context_data['forms']]))
        #    self.assertEqual([], errors)
        self.assertEqual(302, response.status_code, msg='Approve investor does not redirect')

        self.assert_investor_deleted(investor, self.users['editor'])

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test', CELERY_ALWAYS_EAGER=True)
    def test_administrator(self):
        # Delete investor as administrator
        investor = HistoricalInvestor.objects.latest_only().public().latest()
        data = {
            # Action comment
            "tg_action_comment": "Test delete investor",
        }
        url = reverse('investor_delete', kwargs={'investor_id': investor.investor_identifier})
        request = self.mock_request('post', url, 'administrator', data=data)
        response = DeleteInvestorView.as_view()(request, investor_id=investor.investor_identifier)
        #if response.status_code == 200:
        #    # For debugging purposes
        #    errors = list(filter(None, [form.errors or None for form in response.context_data['forms']]))
        #    self.assertEqual([], errors)
        self.assertEqual(302, response.status_code, msg='Delete investor does not redirect')
        investor = HistoricalInvestor.objects.latest_only().deleted().latest()

        self.assert_investor_deleted(investor, self.users['administrator'])
