from io import BytesIO

from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.storage.fallback import FallbackStorage
from django.urls import reverse
from django.http import Http404
from openpyxl import load_workbook

from editor.views import LogDeletedView, ManageForUserView, ManageDeletesView, ApproveInvestorDeleteView
from grid.views.investor import InvestorDetailView, DeleteInvestorView
from grid.views.export import ExportView
from landmatrix.models import HistoricalInvestor
from landmatrix.tests.base import TestInvestorBase


class TestInvestorDelete(TestInvestorBase):
    
    fixtures = [
        'countries_and_regions',
        'users_and_groups',
        'status',
        'investors',
        'activities',
        'activity_involvements',
        'venture_involvements',
    ]

    def assert_investor_deleted(self, investor, user=None):
        # Check if investor is NOT public
        request = self.factory.get(reverse('investor_detail', kwargs={'investor_id': investor.investor_identifier}))
        request.user = AnonymousUser()
        try:
            response = InvestorDetailView.as_view()(request, investor_id=investor.investor_identifier)
        except Http404:
            pass
        else:
            self.fail("Investor still exists after deletion")

        # Check if investor is in latest deleted log
        request = self.factory.get(reverse('log_deleted'))
        request.user = user
        response = LogDeletedView.as_view()(request)
        self.assertEqual(response.status_code, 200, msg='Latest Deleted Log does not work')
        self.assert_investor_in_list(response, investor)

        # Check if investor is NOT in elasticsearch/export
        self.run_commit_hooks()
        request = self.factory.get(reverse('export', kwargs={'format': 'xls'}))
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = AnonymousUser()
        response = ExportView.as_view()(request, format='xls')
        self.assertEqual(response.status_code, 200, msg='Export does not work')
        wb = load_workbook(BytesIO(response.content), read_only=True)
        ws = wb['Investors']
        investor_identifiers = [row[0].value for row in ws.rows]
        # FIXME
        #if '#%s' % str(investor.investor_identifier) in investor_identifiers:
        #    self.fail('Investor still appears in export after deletion (checked XLS only)')

    def test_reporter(self):
        # Delete investor as reporter
        investor = HistoricalInvestor.objects.latest_only().public().latest()
        data = {
            # Action comment
            "tg_action_comment": "Test delete investor",
        }
        request = self.factory.post(reverse('investor_delete', kwargs={'investor_id': investor.investor_identifier}), data)
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['reporter']
        response = DeleteInvestorView.as_view()(request, investor_id=investor.investor_identifier)
        #if response.status_code == 200:
        #    # For debugging purposes
        #    errors = list(filter(None, [form.errors or None for form in response.context_data['forms']]))
        #    self.assertEqual(errors, [])
        self.assertEqual(response.status_code, 302, msg='Delete investor by Reporter does not redirect')

        investor = HistoricalInvestor.objects.latest_only().to_delete().latest()

        # Check if investor appears in my investors section of reporter
        request = self.factory.get(reverse('manage_for_user'))
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['reporter']
        response = ManageForUserView.as_view()(request)
        self.assertEqual(response.status_code, 200, msg='Manage My Deals/Investors of Reporter does not work')
        self.assert_investor_in_list(response, investor)

        # Check if investor appears in manage section of administrator
        request = self.factory.get(reverse('manage_pending_deletes'))
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['administrator']
        response = ManageDeletesView.as_view()(request)
        self.assertEqual(response.status_code, 200, msg='Manage Pending Deletes of Administrator does not work')
        self.assert_investor_in_list(response, investor)

        # Check if investor appears in manage section of editor
        request = self.factory.get(reverse('manage_pending_deletes'))
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['editor']
        response = ManageDeletesView.as_view()(request)
        self.assertEqual(response.status_code, 200, msg='Manage Pending Deletes of Editor does not work')
        self.assert_investor_in_list(response, investor, role='reporter')

        # Approve investor as editor
        data = {
            # Action comment
            "tg_action_comment": "Test approve by Editor",
        }
        request = self.factory.post(reverse('manage_approve_delete_investor', kwargs={'id': investor.id}), data)
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['editor']
        response = ApproveInvestorDeleteView.as_view()(request, id=investor.id)
        #if response.status_code == 200:
        #    # For debugging purposes
        #    errors = list(filter(None, [form.errors or None for form in response.context_data['forms']]))
        #    self.assertEqual(errors, [])
        self.assertEqual(response.status_code, 302, msg='Approve investor by Editor does not redirect')

        # Check if investor appears in manage section of administrator
        request = self.factory.get(reverse('manage_pending_deletes'))
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['administrator']
        response = ManageDeletesView.as_view()(request)
        self.assertEqual(response.status_code, 200, msg='Manage Pending Deletes of Administrator does not work')
        self.assert_investor_in_list(response, investor, role='reporter')

        # Approve investor as administrator
        data = {
            # Action comment
            "tg_action_comment": "Test approve by Administrator",
        }
        request = self.factory.post(reverse('manage_approve_delete_investor', kwargs={'id': investor.id}), data)
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['administrator']
        response = ApproveInvestorDeleteView.as_view()(request, id=investor.id)
        #if response.status_code == 200:
        #    # For debugging purposes
        #    errors = list(filter(None, [form.errors or None for form in response.context_data['forms']]))
        #    self.assertEqual(errors, [])
        self.assertEqual(response.status_code, 302, msg='Approve investor by Administrator does not redirect')

        self.assert_investor_deleted(investor, self.users['reporter'])

    def test_editor(self):
        # Delete investor as editor
        investor = HistoricalInvestor.objects.latest_only().public().latest()
        data = {
            # Action comment
            "tg_action_comment": "Test delete investor",
        }
        request = self.factory.post(reverse('investor_delete', kwargs={'investor_id': investor.investor_identifier}), data)
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['editor']
        response = DeleteInvestorView.as_view()(request, investor_id=investor.investor_identifier)
        #if response.status_code == 200:
        #    # For debugging purposes
        #    errors = list(filter(None, [form.errors or None for form in response.context_data['forms']]))
        #    self.assertEqual(errors, [])
        self.assertEqual(response.status_code, 302, msg='Delete investor does not redirect')

        investor = HistoricalInvestor.objects.latest_only().to_delete().latest()

        # Check if investor appears in manage section of administrator
        request = self.factory.get(reverse('manage_pending_deletes'))
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['administrator']
        response = ManageDeletesView.as_view()(request)
        self.assertEqual(response.status_code, 200, msg='Manage Pending Deletes of Administrator does not work')
        self.assert_investor_in_list(response, investor, role='editor')

        # Approve investor as administrator
        data = {
            # Action comment
            "tg_action_comment": "Test approve by Administrator",
        }
        request = self.factory.post(reverse('manage_approve_delete_investor', kwargs={'id': investor.id}), data)
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['administrator']
        response = ApproveInvestorDeleteView.as_view()(request, id=investor.id)
        #if response.status_code == 200:
        #    # For debugging purposes
        #    errors = list(filter(None, [form.errors or None for form in response.context_data['forms']]))
        #    self.assertEqual(errors, [])
        self.assertEqual(response.status_code, 302, msg='Approve investor does not redirect')

        self.assert_investor_deleted(investor, self.users['editor'])

    def test_administrator(self):
        # Delete investor as administrator
        investor = HistoricalInvestor.objects.latest_only().public().latest()
        data = {
            # Action comment
            "tg_action_comment": "Test delete investor",
        }
        request = self.factory.post(reverse('investor_delete', kwargs={'investor_id': investor.investor_identifier}), data)
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['administrator']
        response = DeleteInvestorView.as_view()(request, investor_id=investor.investor_identifier)
        #if response.status_code == 200:
        #    # For debugging purposes
        #    errors = list(filter(None, [form.errors or None for form in response.context_data['forms']]))
        #    self.assertEqual(errors, [])
        self.assertEqual(response.status_code, 302, msg='Delete investor does not redirect')
        investor = HistoricalInvestor.objects.latest_only().deleted().latest()

        self.assert_investor_deleted(investor, self.users['administrator'])
