from io import BytesIO

from django.contrib.auth.models import AnonymousUser
from django.test import override_settings, tag
from django.urls import reverse
from openpyxl import load_workbook

from apps.editor.views import (
    ApproveInvestorChangeView,
    ManageForUserView,
    ManageUpdatesView,
)
from apps.grid.tests.views.base import BaseInvestorTestCase
from apps.grid.views.export import ExportView
from apps.grid.views.investor import InvestorDetailView, InvestorUpdateView
from apps.landmatrix.models import HistoricalInvestor
from apps.landmatrix.tests.mixins import InvestorsFixtureMixin


@tag("integration")
class TestInvestorUpdate(InvestorsFixtureMixin, BaseInvestorTestCase):

    inv_fixtures = [
        {"id": 1, "investor_identifier": 1, "name": "Test Investor #1"},
        {"id": 2, "investor_identifier": 2, "name": "Test Investor #2"},
        {
            "id": 3,
            "investor_identifier": 2,
            "fk_status_id": 1,
            "name": "Test Investor #2",
        },
    ]

    @override_settings(
        ELASTICSEARCH_INDEX_NAME="landmatrix_test", CELERY_ALWAYS_EAGER=True
    )
    def assert_investor_updated(self, investor, user):
        # Check if investor is public
        url = reverse(
            "investor_detail", kwargs={"investor_id": investor.investor_identifier}
        )
        request = self.mock_request("get", url, AnonymousUser())
        response = InvestorDetailView.as_view()(
            request, investor_id=investor.investor_identifier
        )
        self.assertEqual(
            200,
            response.status_code,
            msg="Investor is not public after approval of Administrator",
        )

        # Check if investor is in latest changed log
        # FIXME: Check with concept
        # url = reverse('log_modified')
        # request = self.mock_request('get', url, user)
        # response = LogModifiedView.as_view()(request)
        # self.assertEqual(200, response.status_code, msg='Latest Modified Log does not work')
        # self.assert_investor_in_list(response, investor)

        # Check if investor is in elasticsearch/export
        self.run_commit_hooks()
        url = reverse("export", kwargs={"format": "xls"})
        request = self.mock_request("get", url, AnonymousUser())
        response = ExportView.as_view()(request, format="xls")
        self.assertEqual(200, response.status_code, msg="Export does not work")
        wb = load_workbook(BytesIO(response.content), read_only=True)
        ws = wb["Investors"]
        investor_identifiers = [row[0].value for row in ws.rows]
        # FIXME
        # if '#%s' % str(investor.investor_identifier) not in investor_identifiers:
        #    self.fail('Investor does not appear in export (checked XLS only)')

    @override_settings(
        ELASTICSEARCH_INDEX_NAME="landmatrix_test", CELERY_ALWAYS_EAGER=True
    )
    def test_reporter(self):
        # Change investor as reporter
        investor = HistoricalInvestor.objects.latest_only().public().latest()
        data = self.INVESTOR_DATA.copy()
        data.update(
            {
                # Action comment
                "action_comment": "Test change investor"
            }
        )
        url = reverse(
            "investor_update", kwargs={"investor_id": investor.investor_identifier}
        )
        request = self.mock_request("post", url, "reporter", data=data)
        response = InvestorUpdateView.as_view()(
            request, investor_id=investor.investor_identifier
        )
        self.assertEqual(
            302, response.status_code, msg="Change investor does not redirect"
        )

        investor = HistoricalInvestor.objects.latest_only().pending().latest()

        # Check if investor appears in my investors section of reporter
        url = reverse("manage_for_user")
        request = self.mock_request("get", url, "reporter")
        response = ManageForUserView.as_view()(request)
        self.assertEqual(
            200,
            response.status_code,
            msg="Manage My Deals/Investors of Reporter does not work",
        )
        self.assert_investor_in_list(response, investor)

        # Check if investor appears in manage section of administrator
        url = reverse("manage_pending_updates")
        # Administrator without country/region
        request = self.mock_request("get", url, "administrator")
        response = ManageUpdatesView.as_view()(request)
        self.assertEqual(
            200,
            response.status_code,
            msg="Manage Pending Updates of Administrator does not work",
        )
        self.assert_investor_in_list(response, investor)
        # Administrator with country
        request = self.mock_request("get", url, "administrator-myanmar")
        response = ManageUpdatesView.as_view()(request)
        self.assertEqual(
            200,
            response.status_code,
            msg="Manage Pending Deletes of Administrator does not work",
        )
        self.assert_investor_in_list(response, investor, role="reporter")
        # Administrator with region
        request = self.mock_request("get", url, "administrator-asia")
        response = ManageUpdatesView.as_view()(request)
        self.assertEqual(
            200,
            response.status_code,
            msg="Manage Pending Deletes of Administrator does not work",
        )
        self.assert_investor_in_list(response, investor, role="reporter")

        # Check if investor appears in manage section of editor
        url = reverse("manage_pending_updates")
        # Editor without country/region
        request = self.mock_request("get", url, "editor")
        response = ManageUpdatesView.as_view()(request)
        self.assertEqual(
            200,
            response.status_code,
            msg="Manage Pending Updates of Editor does not work",
        )
        self.assert_investor_in_list(response, investor)
        # Editor with country
        request = self.mock_request("get", url, "editor-myanmar")
        response = ManageUpdatesView.as_view()(request)
        self.assertEqual(
            200,
            response.status_code,
            msg="Manage Pending Deletes of Editor does not work",
        )
        self.assert_investor_in_list(response, investor, role="reporter")
        # Editor with region
        request = self.mock_request("get", url, "editor-asia")
        response = ManageUpdatesView.as_view()(request)
        self.assertEqual(
            200,
            response.status_code,
            msg="Manage Pending Deletes of Editor does not work",
        )
        self.assert_investor_in_list(response, investor, role="reporter")

        # Approve investor as editor
        data = {
            # Action comment
            "tg_action_comment": "Test approve by Editor"
        }
        url = reverse("manage_approve_change_investor", kwargs={"id": investor.id})
        request = self.mock_request("post", url, "editor", data=data)
        response = ApproveInvestorChangeView.as_view()(request, id=investor.id)
        self.assertEqual(
            302,
            response.status_code,
            msg="Approve investor by Editor does not redirect",
        )

        # Check if investor appears in manage section of administrator
        url = reverse("manage_pending_updates")
        # Administrator without country/region
        request = self.mock_request("get", url, "administrator")
        response = ManageUpdatesView.as_view()(request)
        self.assertEqual(
            200,
            response.status_code,
            msg="Manage Pending Updates of Administrator does not work",
        )
        self.assert_investor_in_list(response, investor)
        # Administrator with country
        request = self.mock_request("get", url, "administrator-myanmar")
        response = ManageUpdatesView.as_view()(request)
        self.assertEqual(
            200,
            response.status_code,
            msg="Manage Pending Deletes of Administrator does not work",
        )
        self.assert_investor_in_list(response, investor, role="reporter")
        # Administrator with region
        request = self.mock_request("get", url, "administrator-asia")
        response = ManageUpdatesView.as_view()(request)
        self.assertEqual(
            200,
            response.status_code,
            msg="Manage Pending Deletes of Administrator does not work",
        )
        self.assert_investor_in_list(response, investor, role="reporter")

        # Approve investor as administrator
        data = {
            # Action comment
            "tg_action_comment": "Test approve by Administrator"
        }
        url = reverse("manage_approve_change_investor", kwargs={"id": investor.id})
        request = self.mock_request("post", url, "administrator", data=data)
        response = ApproveInvestorChangeView.as_view()(request, id=investor.id)
        self.assertEqual(
            302,
            response.status_code,
            msg="Approve investor by Administrator does not redirect",
        )

        self.assert_investor_updated(investor, self.users["reporter"])

    @override_settings(
        ELASTICSEARCH_INDEX_NAME="landmatrix_test", CELERY_ALWAYS_EAGER=True
    )
    def test_editor(self):
        # Change investor as editor
        investor = HistoricalInvestor.objects.latest_only().public().latest()
        data = self.INVESTOR_DATA.copy()
        data.update(
            {
                # Action comment
                "action_comment": "Test change investor"
            }
        )
        url = reverse(
            "investor_update", kwargs={"investor_id": investor.investor_identifier}
        )
        request = self.mock_request("post", url, "editor", data=data)
        response = InvestorUpdateView.as_view()(
            request, investor_id=investor.investor_identifier
        )
        self.assertEqual(
            302, response.status_code, msg="Change investor does not redirect"
        )

        investor = HistoricalInvestor.objects.latest_only().pending().latest()

        # Check if investor appears in manage section of administrator
        url = reverse("manage_pending_updates")
        # Administrator without country/region
        request = self.mock_request("get", url, "administrator")
        response = ManageUpdatesView.as_view()(request)
        self.assertEqual(
            200,
            response.status_code,
            msg="Manage Pending Updates of Administrator does not work",
        )
        self.assert_investor_in_list(response, investor)
        # Administrator with country
        request = self.mock_request("get", url, "administrator-myanmar")
        response = ManageUpdatesView.as_view()(request)
        self.assertEqual(
            200,
            response.status_code,
            msg="Manage Pending Deletes of Administrator does not work",
        )
        self.assert_investor_in_list(response, investor, role="editor")
        # Administrator with region
        request = self.mock_request("get", url, "administrator-asia")
        response = ManageUpdatesView.as_view()(request)
        self.assertEqual(
            200,
            response.status_code,
            msg="Manage Pending Deletes of Administrator does not work",
        )
        self.assert_investor_in_list(response, investor, role="editor")

        # Approve investor as administrator
        data = {
            # Action comment
            "tg_action_comment": "Test approve by Administrator"
        }
        url = reverse("manage_approve_change_investor", kwargs={"id": investor.id})
        request = self.mock_request("post", url, "administrator", data=data)
        response = ApproveInvestorChangeView.as_view()(request, id=investor.id)
        # if response.status_code == 200:
        #    # For debugging purposes
        #    errors = list(filter(None, [form.errors or None for form in response.context_data['forms']]))
        #    self.assertEqual([], errors)
        self.assertEqual(
            302,
            response.status_code,
            msg="Approve investor by Administrator does not redirect",
        )

        self.assert_investor_updated(investor, self.users["editor"])

    @override_settings(
        ELASTICSEARCH_INDEX_NAME="landmatrix_test", CELERY_ALWAYS_EAGER=True
    )
    def test_administrator(self):
        # Change investor as administrator
        investor = HistoricalInvestor.objects.latest_only().public().latest()
        data = self.INVESTOR_DATA.copy()
        data.update(
            {
                # Action comment
                "action_comment": "Test change investor",
                "approve_btn": True,
            }
        )
        url = reverse(
            "investor_update", kwargs={"investor_id": investor.investor_identifier}
        )
        request = self.mock_request("post", url, "administrator", data=data)
        response = InvestorUpdateView.as_view()(
            request, investor_id=investor.investor_identifier
        )
        self.assertEqual(
            302, response.status_code, msg="Change investor does not redirect"
        )

        investor = HistoricalInvestor.objects.latest_only().public().latest()

        self.assert_investor_updated(investor, self.users["administrator"])
