from io import BytesIO

from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.storage.fallback import FallbackStorage
from django.urls import reverse
from django.test import tag, override_settings
from openpyxl import load_workbook

from editor.views import LogAddedView, ManageForUserView, ManageAddsView, ApproveActivityChangeView
from grid.views.deal import DealDetailView, DealCreateView
from grid.views.export import ExportView
from landmatrix.models import HistoricalActivity

from grid.tests.views.base import BaseDealTestCase


@tag('integration')
class TestDealCreate(BaseDealTestCase):

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test', CELERY_ALWAYS_EAGER=True)
    def assert_deal_created(self, activity, user):
        # Check if deal is public
        request = self.factory.get(reverse('deal_detail', kwargs={'deal_id': activity.activity_identifier}))
        request.user = AnonymousUser()
        response = DealDetailView.as_view()(request, deal_id=activity.activity_identifier)
        self.assertEqual(200, response.status_code, msg='Deal is not public after approval of Administrator')

        # Check if deal is in latest added log
        request = self.factory.get(reverse('log_added'))
        request.user = user
        response = LogAddedView.as_view()(request)
        self.assertEqual(200, response.status_code, msg='Latest Added Log does not work')
        self.assert_deal_in_list(response, activity)

        # Check if deal is in elasticsearch/export
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
        ws = wb['Deals']
        activity_identifiers = [row[0].value for row in ws.rows]
        # FIXME
        #if '#%s' % str(activity.activity_identifier) not in activity_identifiers:
        #    self.fail('Deal does not appear in export (checked XLS only)')

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test', CELERY_ALWAYS_EAGER=True)
    def test_reporter(self):
        # Add deal as reporter
        data = self.DEAL_DATA.copy()
        data.update({
            # Action comment
            "tg_action_comment": "Test add deal",
        })
        request = self.factory.post(reverse('add_deal'), data)
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['reporter']
        response = DealCreateView.as_view()(request)
        self.assertEqual(302, response.status_code, msg='Add deal does not redirect')

        activity = HistoricalActivity.objects.latest_only().pending().latest()

        # Check if deal appears in my deals section of reporter
        request = self.factory.get(reverse('manage_for_user'))
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['reporter']
        response = ManageForUserView.as_view()(request)
        self.assertEqual(200, response.status_code, msg='Manage My Deals/Investors of Reporter does not work')
        self.assert_deal_in_list(response, activity, role='reporter')

        # Check if deal appears in manage section of administrator
        request = self.factory.get(reverse('manage_pending_adds'))
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['administrator']
        response = ManageAddsView.as_view()(request)
        self.assertEqual(200, response.status_code, msg='Manage Pending Deals/Investors of Administrator does not work')
        self.assert_deal_in_list(response, activity)

        # Check if deal appears in manage section of editor
        request = self.factory.get(reverse('manage_pending_adds'))
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['editor']
        response = ManageAddsView.as_view()(request)
        self.assertEqual(200, response.status_code, msg='Manage Pending Additions of Editor does not work')
        self.assert_deal_in_list(response, activity, role='reporter')

        # Approve deal as editor
        data = {
            # Action comment
            "tg_action_comment": "Test approve by Editor",
        }
        request = self.factory.post(reverse('manage_approve_change_deal', kwargs={'id': activity.id}), data)
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['editor']
        response = ApproveActivityChangeView.as_view()(request, id=activity.id)
        self.assertEqual(302, response.status_code, msg='Approve deal by Editor does not redirect')

        # Check if deal appears in manage section of administrator
        request = self.factory.get(reverse('manage_pending_adds'))
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['administrator']
        response = ManageAddsView.as_view()(request)
        self.assertEqual(200, response.status_code, msg='Manage Pending Additions of Administrator does not work')
        self.assert_deal_in_list(response, activity, role='reporter')

        # Approve deal as administrator
        data = {
            # Action comment
            "tg_action_comment": "Test approve by Administrator",
        }
        request = self.factory.post(reverse('manage_approve_change_deal', kwargs={'id': activity.id}), data)
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['administrator']
        response = ApproveActivityChangeView.as_view()(request, id=activity.id)
        self.assertEqual(302, response.status_code, msg='Approve deal by Administrator does not redirect')

        self.assert_deal_created(activity, self.users['reporter'])

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test', CELERY_ALWAYS_EAGER=True)
    def test_editor(self):
        # Add deal as editor
        data = self.DEAL_DATA.copy()
        data.update({
            # Action comment
            "tg_action_comment": "Test add deal",
        })
        request = self.factory.post(reverse('add_deal'), data)
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['editor']
        response = DealCreateView.as_view()(request)
        self.assertEqual(302, response.status_code, msg='Add deal does not redirect')

        activity = HistoricalActivity.objects.latest_only().pending().latest()

        # Check if deal appears in manage section of administrator
        request = self.factory.get(reverse('manage_pending_adds'))
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['administrator']
        response = ManageAddsView.as_view()(request)
        self.assertEqual(200, response.status_code, msg='Manage Pending Additions of Administrator does not work')
        self.assert_deal_in_list(response, activity, role='editor')

        # Approve deal as administrator
        data = {
            # Action comment
            "tg_action_comment": "Test approve by Administrator",
        }
        request = self.factory.post(reverse('manage_approve_change_deal', kwargs={'id': activity.id}), data)
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['administrator']
        response = ApproveActivityChangeView.as_view()(request, id=activity.id)
        self.assertEqual(302, response.status_code, msg='Approve deal by Administrator does not redirect')

        self.assert_deal_created(activity, self.users['editor'])

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test', CELERY_ALWAYS_EAGER=True)
    def test_administrator_with_investor_create(self):
        """
        Test add deal as administrator
        with creating investor (1 pending investor version only)
        :return:
        """
        data = self.DEAL_DATA.copy()
        data.update({
            "operational_stakeholder": self.INVESTOR_CREATED,
            "tg_action_comment": "Test add deal",
            "approve_btn": True
        })
        request = self.factory.post(reverse('add_deal'), data)
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['administrator']
        response = DealCreateView.as_view()(request)
        self.assertEqual(302, response.status_code, msg='Add deal does not redirect')

        activity = HistoricalActivity.objects.latest_only().public().latest()

        self.assert_deal_created(activity, self.users['administrator'])
        self.assert_investors_approved(activity)

    def test_administrator_with_investor_update(self):
        """
        Test add deal as administrator
        with updating investor (1 pending but also other investor versions)
        :return:
        """
        data = self.DEAL_DATA.copy()
        data.update({
            "operational_stakeholder": self.INVESTOR_UPDATED,
            "tg_action_comment": "Test add deal",
            "approve_btn": True
        })
        request = self.factory.post(reverse('add_deal'), data)
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['administrator']
        response = DealCreateView.as_view()(request)
        self.assertEqual(302, response.status_code, msg='Add deal does not redirect')

        activity = HistoricalActivity.objects.latest_only().public().latest()

        self.assert_deal_created(activity, self.users['administrator'])
        self.assert_investors_not_approved(activity)
