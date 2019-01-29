from io import BytesIO

from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.storage.fallback import FallbackStorage
from django.core.urlresolvers import reverse
from openpyxl import load_workbook

from editor.views import LogModifiedView, ManageForUserView, ManageUpdatesView, ApproveInvestorChangeView
from grid.views.investor import InvestorDetailView, InvestorUpdateView
from grid.views.export import ExportView
from landmatrix.models import HistoricalInvestor
from landmatrix.tests.base import TestInvestorBase


class TestInvestorUpdate(TestInvestorBase):

    fixtures = [
        'countries_and_regions',
        'users_and_groups',
        'status',
        'investors',
        'activities',
        'activity_involvements',
        'venture_involvements',
    ]

    def assert_investor_updated(self, investor, user):
        # Check if investor is public
        request = self.factory.get(reverse('investor_detail', kwargs={'investor_id': investor.investor_identifier}))
        request.user = AnonymousUser()
        response = InvestorDetailView.as_view()(request, investor_id=investor.investor_identifier)
        self.assertEqual(response.status_code, 200, msg='Investor is not public after approval of Administrator')

        # Check if investor is in latest changed log
        request = self.factory.get(reverse('log_modified'))
        request.user = user
        response = LogModifiedView.as_view()(request)
        self.assertEqual(response.status_code, 200, msg='Latest Modified Log does not work')
        self.assert_investor_in_list(response, investor)

        # Check if investor is in elasticsearch/export
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
        #if '#%s' % str(investor.investor_identifier) not in investor_identifiers:
        #    self.fail('Investor does not appear in export (checked XLS only)')

    def test_reporter(self):
        # Change investor as reporter
        investor = HistoricalInvestor.objects.latest_only().public().latest()
        data = self.INVESTOR_DATA.copy()
        data.update({
            # Action comment
            "action_comment": "Test change investor",
        })
        request = self.factory.post(reverse('investor_update', kwargs={'investor_id': investor.investor_identifier}), data)
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['reporter']
        response = InvestorUpdateView.as_view()(request, investor_id=investor.investor_identifier)
        self.assertEqual(response.status_code, 302, msg='Change investor does not redirect')

        investor = HistoricalInvestor.objects.latest_only().pending().latest()

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
        request = self.factory.get(reverse('manage_pending_updates'))
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['administrator']
        response = ManageUpdatesView.as_view()(request)
        self.assertEqual(response.status_code, 200, msg='Manage Pending Updates of Administrator does not work')
        self.assert_investor_in_list(response, investor)

        # Check if investor appears in manage section of editor
        request = self.factory.get(reverse('manage_pending_updates'))
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['editor']
        response = ManageUpdatesView.as_view()(request)
        self.assertEqual(response.status_code, 200, msg='Manage Pending Updates of Editor does not work')
        self.assert_investor_in_list(response, investor, role='reporter')

        # Approve investor as editor
        data = {
            # Action comment
            "tg_action_comment": "Test approve by Editor",
        }
        request = self.factory.post(reverse('manage_approve_change_investor', kwargs={'id': investor.id}), data)
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['editor']
        response = ApproveInvestorChangeView.as_view()(request, id=investor.id)
        self.assertEqual(response.status_code, 302, msg='Approve investor by Editor does not redirect')

        # Check if investor appears in manage section of administrator
        request = self.factory.get(reverse('manage_pending_updates'))
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['administrator']
        response = ManageUpdatesView.as_view()(request)
        self.assertEqual(response.status_code, 200, msg='Manage Pending Updates of Administrator does not work')
        self.assert_investor_in_list(response, investor, role='reporter')

        # Approve investor as administrator
        data = {
            # Action comment
            "tg_action_comment": "Test approve by Administrator",
        }
        request = self.factory.post(reverse('manage_approve_change_investor', kwargs={'id': investor.id}), data)
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['administrator']
        response = ApproveInvestorChangeView.as_view()(request, id=investor.id)
        self.assertEqual(response.status_code, 302, msg='Approve investor by Administrator does not redirect')

        self.assert_investor_updated(investor, self.users['reporter'])

    def test_editor(self):
        # Change investor as editor
        investor = HistoricalInvestor.objects.latest_only().public().latest()
        data = self.INVESTOR_DATA.copy()
        data.update({
            # Action comment
            "action_comment": "Test change investor",
        })
        request = self.factory.post(reverse('investor_update', kwargs={'investor_id': investor.investor_identifier}), data)
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['editor']
        response = InvestorUpdateView.as_view()(request, investor_id=investor.investor_identifier)
        self.assertEqual(response.status_code, 302, msg='Change investor does not redirect')

        investor = HistoricalInvestor.objects.latest_only().pending().latest()

        # Check if investor appears in manage section of administrator
        request = self.factory.get(reverse('manage_pending_updates'))
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['administrator']
        response = ManageUpdatesView.as_view()(request)
        self.assertEqual(response.status_code, 200, msg='Manage Pending Updates of Administrator does not work')
        self.assert_investor_in_list(response, investor, role='editor')

        # Approve investor as administrator
        data = {
            # Action comment
            "tg_action_comment": "Test approve by Administrator",
        }
        request = self.factory.post(reverse('manage_approve_change_investor', kwargs={'id': investor.id}), data)
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['administrator']
        response = ApproveInvestorChangeView.as_view()(request, id=investor.id)
        #if response.status_code == 200:
        #    # For debugging purposes
        #    errors = list(filter(None, [form.errors or None for form in response.context_data['forms']]))
        #    self.assertEqual(errors, [])
        self.assertEqual(response.status_code, 302, msg='Approve investor by Administrator does not redirect')

        self.assert_investor_updated(investor, self.users['editor'])

    def test_administrator(self):
        # Change investor as administrator
        investor = HistoricalInvestor.objects.latest_only().public().latest()
        data = self.INVESTOR_DATA.copy()
        data.update({
            # Action comment
            "action_comment": "Test change investor",
            "approve_btn": True
        })
        request = self.factory.post(reverse('investor_update', kwargs={'investor_id': investor.investor_identifier}), data)
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['administrator']
        response = InvestorUpdateView.as_view()(request, investor_id=investor.investor_identifier)
        self.assertEqual(response.status_code, 302, msg='Change investor does not redirect')

        investor = HistoricalInvestor.objects.latest_only().public().latest()

        self.assert_investor_updated(investor, self.users['administrator'])
