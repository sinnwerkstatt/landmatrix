from io import BytesIO

from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.storage.fallback import FallbackStorage
from django.core.urlresolvers import reverse
from openpyxl import load_workbook

from editor.views import LogAddedView, ManageForUserView, ManageAddsView, ApproveInvestorChangeView
from grid.views.investor import InvestorDetailView, InvestorCreateView
from grid.views.export import ExportView
from landmatrix.models import HistoricalInvestor
from landmatrix.tests.base import TestInvestorBase


class TestInvestorCreate(TestInvestorBase):

    def is_investor_added(self, investor, user):
        # Check if investor is public
        request = self.factory.get(reverse('investor_detail', kwargs={'investor_id': investor.investor_identifier}))
        request.user = AnonymousUser()
        response = InvestorDetailView.as_view()(request, investor_id=investor.investor_identifier)
        self.assertEqual(response.status_code, 200, msg='Investor is not public after approval of Administrator')

        # Check if investor is in latest added log
        request = self.factory.get(reverse('log_added'))
        request.user = user
        response = LogAddedView.as_view()(request)
        self.assertEqual(response.status_code, 200, msg='Latest Added Log does not work')
        items = list(response.context_data['items'])
        self.assertGreaterEqual(len(items), 1, msg='Wrong list of investors in Latest Added Log of Reporter')
        self.assertEqual(items[0]['history_id'], investor.id, msg='Investor does not appear in Latest Added Log')

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
        # Add investor as reporter
        data = self.INVESTOR_DATA.copy()
        data.update({
            # Action comment
            "action_comment": "Test add investor",
        })
        request = self.factory.post(reverse('investor_add'), data)
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['reporter']
        response = InvestorCreateView.as_view()(request)
        self.assertEqual(response.status_code, 302, msg='Add investor does not redirect')

        investor = HistoricalInvestor.objects.pending().latest()

        # Check if investor appears in my deals/investors section of reporter
        request = self.factory.get(reverse('manage_for_user'))
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['reporter']
        response = ManageForUserView.as_view()(request)
        self.assertEqual(response.status_code, 200, msg='Manage My Deals/Investors of Reporter does not work')
        items = list(response.context_data['items'])
        self.assertEqual(len(items), 1, msg='Wrong list of investors in Manage My Deals/Investors of Reporter')
        self.assertEqual(items[0]['history_id'], investor.id,
                         msg='Investor does not appear in Manage My Deals/Investors of Reporter')

        # Check if investor appears in manage section of administrator
        request = self.factory.get(reverse('manage_pending_adds'))
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['administrator']
        response = ManageAddsView.as_view()(request)
        self.assertEqual(response.status_code, 200, msg='Manage Pending Deals/Investors of Administrator does not work')
        items = list(response.context_data['items'])
        self.assertEqual(len(items), 1, msg='Manage Pending Deals/Investors of Administrator should be empty')

        # Check if investor appears in manage section of editor
        request = self.factory.get(reverse('manage_pending_adds'))
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['editor']
        response = ManageAddsView.as_view()(request)
        self.assertEqual(response.status_code, 200, msg='Manage Pending Additions of Editor does not work')
        items = list(response.context_data['items'])
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]['history_id'], investor.id,
                         msg='Investor does not appear in Manage Pending Deals/Investors of Editor')
        self.assertEqual(items[0]['user'], self.get_username_and_role('reporter'),
                         msg='Investor has wrong user in Manage Pending Deals/Investors of Editor')

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
        request = self.factory.get(reverse('manage_pending_adds'))
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['administrator']
        response = ManageAddsView.as_view()(request)
        self.assertEqual(response.status_code, 200, msg='Manage Pending Additions of Administrator does not work')
        items = list(response.context_data['items'])
        self.assertEqual(len(items), 1, msg='Wrong list of investor in Manage Pending Additions of Administrator')
        self.assertEqual(items[0]['history_id'], investor.id, msg='Investor does not appear in Manage Pending Additions of Administrator')
        self.assertEqual(items[0]['user'], self.get_username_and_role('reporter'), msg='Investor has wrong user in Manage Pending Additions of Administrator')

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

        self.is_investor_added(investor, self.users['reporter'])

    def test_editor(self):
        # Add investor as editor
        data = self.INVESTOR_DATA.copy()
        data.update({
            # Action comment
            "action_comment": "Test add investor",
        })
        request = self.factory.post(reverse('investor_add'), data)
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['editor']
        response = InvestorCreateView.as_view()(request)
        self.assertEqual(response.status_code, 302, msg='Add investor does not redirect')
        investor = HistoricalInvestor.objects.pending().latest()

        # Check if investor appears in manage section of administrator
        request = self.factory.get(reverse('manage_pending_adds'))
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['administrator']
        response = ManageAddsView.as_view()(request)
        self.assertEqual(response.status_code, 200, msg='Manage Pending Additions of Administrator does not work')
        items = list(response.context_data['items'])
        self.assertEqual(len(items), 1, msg='Wrong list of investors in Manage Pending Additions of Administrator')
        self.assertEqual(items[0]['history_id'], investor.id, msg='Investor does not appear in Manage Pending Additions of Administrator')
        self.assertEqual(items[0]['user'], self.get_username_and_role('editor'), msg='Investor has wrong user in Manage Pending Additions of Administrator')

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

        self.is_investor_added(investor, self.users['editor'])

    def test_administrator(self):
        # Add investor as administrator
        data = self.INVESTOR_DATA.copy()
        data.update({
            # Action comment
            "action_comment": "Test add investor",
            "approve_btn": True
        })
        request = self.factory.post(reverse('investor_add'), data)
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['administrator']
        response = InvestorCreateView.as_view()(request)
        self.assertEqual(response.status_code, 302, msg='Add investor does not redirect')

        investor = HistoricalInvestor.objects.public().latest()

        self.is_investor_added(investor, self.users['administrator'])
