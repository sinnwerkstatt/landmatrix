from io import BytesIO

from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import override_settings, tag
from django.urls import reverse
from openpyxl import load_workbook

from apps.editor.views import ApproveInvestorChangeView, LogAddedView, ManageAddsView, ManageForUserView
from apps.grid.tests.views.base import BaseInvestorTestCase
from apps.grid.views.export import ExportView
from apps.grid.views.investor import InvestorCreateView, InvestorDetailView
from apps.landmatrix.models import HistoricalInvestor


@tag('integration')
class TestInvestorCreate(BaseInvestorTestCase):

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test', CELERY_ALWAYS_EAGER=True)
    def assert_investor_created(self, investor, user):
        # Check if investor is public
        request = self.factory.get(reverse('investor_detail', kwargs={'investor_id': investor.investor_identifier}))
        request.user = AnonymousUser()
        response = InvestorDetailView.as_view()(request, investor_id=investor.investor_identifier)
        self.assertEqual(200, response.status_code, msg='Investor is not public after approval of Administrator')

        # Check if investor is in latest added log
        request = self.factory.get(reverse('log_added'))
        request.user = user
        response = LogAddedView.as_view()(request)
        self.assertEqual(200, response.status_code, msg='Latest Added Log does not work')
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
        self.assertEqual(200, response.status_code, msg='Export does not work')
        wb = load_workbook(BytesIO(response.content), read_only=True)
        ws = wb['Investors']
        investor_identifiers = [row[0].value for row in ws.rows]
        # FIXME
        #if '#%s' % str(investor.investor_identifier) not in investor_identifiers:
        #    self.fail('Investor does not appear in export (checked XLS only)')

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test', CELERY_ALWAYS_EAGER=True)
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
        self.assertEqual(302, response.status_code, msg='Add investor does not redirect')

        investor = HistoricalInvestor.objects.latest_only().pending().latest()

        # Check if investor appears in my deals/investors section of reporter
        request = self.factory.get(reverse('manage_for_user'))
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['reporter']
        response = ManageForUserView.as_view()(request)
        self.assertEqual(200, response.status_code, msg='Manage My Deals/Investors of Reporter does not work')
        self.assert_investor_in_list(response, investor)

        # Check if investor appears in manage section of administrator
        request = self.factory.get(reverse('manage_pending_adds'))
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['administrator']
        response = ManageAddsView.as_view()(request)
        self.assertEqual(200, response.status_code, msg='Manage Pending Deals/Investors of Administrator does not work')
        self.assert_investor_in_list(response, investor)

        # Check if investor appears in manage section of editor
        request = self.factory.get(reverse('manage_pending_adds'))
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['editor']
        response = ManageAddsView.as_view()(request)
        self.assertEqual(200, response.status_code, msg='Manage Pending Additions of Editor does not work')
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
        self.assertEqual(302, response.status_code, msg='Approve investor by Editor does not redirect')

        # Check if investor appears in manage section of administrator
        request = self.factory.get(reverse('manage_pending_adds'))
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['administrator']
        response = ManageAddsView.as_view()(request)
        self.assertEqual(200, response.status_code, msg='Manage Pending Additions of Administrator does not work')
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
        self.assertEqual(302, response.status_code, msg='Approve investor by Administrator does not redirect')

        self.assert_investor_created(investor, self.users['reporter'])

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test', CELERY_ALWAYS_EAGER=True)
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
        self.assertEqual(302, response.status_code, msg='Add investor does not redirect')
        investor = HistoricalInvestor.objects.latest_only().pending().latest()

        # Check if investor appears in manage section of administrator
        request = self.factory.get(reverse('manage_pending_adds'))
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['administrator']
        response = ManageAddsView.as_view()(request)
        self.assertEqual(200, response.status_code, msg='Manage Pending Additions of Administrator does not work')
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
        self.assertEqual(302, response.status_code, msg='Approve investor by Administrator does not redirect')

        self.assert_investor_created(investor, self.users['editor'])

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test', CELERY_ALWAYS_EAGER=True)
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
        self.assertEqual(302, response.status_code, msg='Add investor does not redirect')

        investor = HistoricalInvestor.objects.latest_only().public().latest()

        self.assert_investor_created(investor, self.users['administrator'])
