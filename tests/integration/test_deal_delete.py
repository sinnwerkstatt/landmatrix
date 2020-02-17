from io import BytesIO

from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.storage.fallback import FallbackStorage
from django.http import Http404
from django.test import override_settings, tag
from django.urls import reverse
from openpyxl import load_workbook

from apps.editor.views import (
    ApproveActivityDeleteView,
    LogDeletedView,
    ManageDeletesView,
    ManageForUserView,
)
from apps.grid.tests.views.base import BaseDealTestCase
from apps.grid.views.deal import DealDeleteView, DealDetailView
from apps.grid.views.export import ExportView
from apps.landmatrix.models import HistoricalActivity


@tag("integration")
class TestDealDelete(BaseDealTestCase):

    fixtures = [
        "countries_and_regions",
        "users_and_groups",
        "status",
    ]

    @override_settings(
        ELASTICSEARCH_INDEX_NAME="landmatrix_test", CELERY_ALWAYS_EAGER=True
    )
    def assert_deal_deleted(self, activity, user=None):
        # Check if deal is NOT public
        request = self.factory.get(
            reverse("deal_detail", kwargs={"deal_id": activity.activity_identifier})
        )
        request.user = AnonymousUser()
        try:
            response = DealDetailView.as_view()(
                request, deal_id=activity.activity_identifier
            )
        except Http404:
            pass
        else:
            self.fail("Deal still exists after deletion")

        # Check if deal is in latest deleted log
        request = self.factory.get(reverse("log_deleted"))
        request.user = user
        response = LogDeletedView.as_view()(request)
        self.assertEqual(
            200, response.status_code, msg="Latest Deleted Log does not work"
        )
        self.assert_deal_in_list(response, activity)

        # Check if deal is NOT in elasticsearch/export
        self.run_commit_hooks()
        request = self.factory.get(reverse("export", kwargs={"format": "xls"}))
        # Mock messages framework (not available for unit tests)
        setattr(request, "session", {})
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        request.user = AnonymousUser()
        response = ExportView.as_view()(request, format="xls")
        self.assertEqual(200, response.status_code, msg="Export does not work")
        wb = load_workbook(BytesIO(response.content), read_only=True)
        ws = wb["Deals"]
        activity_identifiers = [row[0].value for row in ws.rows]
        # FIXME
        # if '#%s' % str(activity.activity_identifier) in activity_identifiers:
        #    self.fail('Deal still appears in export after deletion (checked XLS only)')

    @override_settings(
        ELASTICSEARCH_INDEX_NAME="landmatrix_test", CELERY_ALWAYS_EAGER=True
    )
    def test_reporter(self):
        # Delete deal as reporter
        activity = HistoricalActivity.objects.latest_only().public().latest()
        data = {
            # Action comment
            "tg_action_comment": "Test delete deal"
        }
        request = self.factory.post(
            reverse("delete_deal", kwargs={"deal_id": activity.activity_identifier}),
            data,
        )
        # Mock messages framework (not available for unit tests)
        setattr(request, "session", {})
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        request.user = self.users["reporter"]
        response = DealDeleteView.as_view()(
            request, deal_id=activity.activity_identifier
        )
        # if response.status_code == 200:
        #    # For debugging purposes
        #    errors = list(filter(None, [form.errors or None for form in response.context_data['forms']]))
        #    self.assertEqual([], errors)
        self.assertEqual(
            302, response.status_code, msg="Delete deal by Reporter does not redirect"
        )

        activity = HistoricalActivity.objects.latest_only().to_delete().latest()

        # Check if deal appears in my deals section of reporter
        request = self.factory.get(reverse("manage_for_user"))
        # Mock messages framework (not available for unit tests)
        setattr(request, "session", {})
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        request.user = self.users["reporter"]
        response = ManageForUserView.as_view()(request)
        self.assertEqual(
            200,
            response.status_code,
            msg="Manage My Deals/Investors of Reporter does not work",
        )
        self.assert_deal_in_list(response, activity)

        # Check if deal appears in manage section of administrator
        request = self.factory.get(reverse("manage_pending_deletes"))
        # Mock messages framework (not available for unit tests)
        setattr(request, "session", {})
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        request.user = self.users["administrator"]
        response = ManageDeletesView.as_view()(request)
        self.assertEqual(
            200,
            response.status_code,
            msg="Manage Pending Deletes of Administrator does not work",
        )
        self.assert_deal_in_list(response, activity)

        # Check if deal appears in manage section of editor
        request = self.factory.get(reverse("manage_pending_deletes"))
        # Mock messages framework (not available for unit tests)
        setattr(request, "session", {})
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        request.user = self.users["editor"]
        response = ManageDeletesView.as_view()(request)
        self.assertEqual(
            200,
            response.status_code,
            msg="Manage Pending Deletes of Editor does not work",
        )
        self.assert_deal_in_list(response, activity, role="reporter")

        # Approve deal as editor
        data = {
            # Action comment
            "tg_action_comment": "Test approve by Editor"
        }
        request = self.factory.post(
            reverse("manage_approve_delete_deal", kwargs={"id": activity.id}), data
        )
        # Mock messages framework (not available for unit tests)
        setattr(request, "session", {})
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        request.user = self.users["editor"]
        response = ApproveActivityDeleteView.as_view()(request, id=activity.id)
        # if response.status_code == 200:
        #    # For debugging purposes
        #    errors = list(filter(None, [form.errors or None for form in response.context_data['forms']]))
        #    self.assertEqual([], errors)
        self.assertEqual(
            302, response.status_code, msg="Approve deal by Editor does not redirect"
        )

        # Check if deal appears in manage section of administrator
        request = self.factory.get(reverse("manage_pending_deletes"))
        # Mock messages framework (not available for unit tests)
        setattr(request, "session", {})
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        request.user = self.users["administrator"]
        response = ManageDeletesView.as_view()(request)
        self.assertEqual(
            200,
            response.status_code,
            msg="Manage Pending Deletes of Administrator does not work",
        )
        self.assert_deal_in_list(response, activity, role="reporter")

        # Approve deal as administrator
        data = {
            # Action comment
            "tg_action_comment": "Test approve by Administrator"
        }
        request = self.factory.post(
            reverse("manage_approve_delete_deal", kwargs={"id": activity.id}), data
        )
        # Mock messages framework (not available for unit tests)
        setattr(request, "session", {})
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        request.user = self.users["administrator"]
        response = ApproveActivityDeleteView.as_view()(request, id=activity.id)
        # if response.status_code == 200:
        #    # For debugging purposes
        #    errors = list(filter(None, [form.errors or None for form in response.context_data['forms']]))
        #    self.assertEqual([], errors)
        self.assertEqual(
            302,
            response.status_code,
            msg="Approve deal by Administrator does not redirect",
        )

        self.assert_deal_deleted(activity, self.users["reporter"])

    @override_settings(
        ELASTICSEARCH_INDEX_NAME="landmatrix_test", CELERY_ALWAYS_EAGER=True
    )
    def test_editor(self):
        # Delete deal as editor
        activity = HistoricalActivity.objects.latest_only().public().latest()
        data = {
            # Action comment
            "tg_action_comment": "Test delete deal"
        }
        request = self.factory.post(
            reverse("delete_deal", kwargs={"deal_id": activity.activity_identifier}),
            data,
        )
        # Mock messages framework (not available for unit tests)
        setattr(request, "session", {})
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        request.user = self.users["editor"]
        response = DealDeleteView.as_view()(
            request, deal_id=activity.activity_identifier
        )
        # if response.status_code == 200:
        #    # For debugging purposes
        #    errors = list(filter(None, [form.errors or None for form in response.context_data['forms']]))
        #    self.assertEqual([], errors)
        self.assertEqual(response.status_code, 302, msg="Delete deal does not redirect")

        activity = HistoricalActivity.objects.latest_only().to_delete().latest()

        # Check if deal appears in manage section of administrator
        request = self.factory.get(reverse("manage_pending_deletes"))
        # Mock messages framework (not available for unit tests)
        setattr(request, "session", {})
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        request.user = self.users["administrator"]
        response = ManageDeletesView.as_view()(request)
        self.assertEqual(
            response.status_code,
            200,
            msg="Manage Pending Deletes of Administrator does not work",
        )
        self.assert_deal_in_list(response, activity, role="editor")

        # Approve deal as administrator
        data = {
            # Action comment
            "tg_action_comment": "Test approve by Administrator"
        }
        request = self.factory.post(
            reverse("manage_approve_delete_deal", kwargs={"id": activity.id}), data
        )
        # Mock messages framework (not available for unit tests)
        setattr(request, "session", {})
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        request.user = self.users["administrator"]
        response = ApproveActivityDeleteView.as_view()(request, id=activity.id)
        # if response.status_code == 200:
        #    # For debugging purposes
        #    errors = list(filter(None, [form.errors or None for form in response.context_data['forms']]))
        #    self.assertEqual(errors, [])
        self.assertEqual(
            response.status_code, 302, msg="Approve deal does not redirect"
        )

        self.assert_deal_deleted(activity, self.users["editor"])

    @override_settings(
        ELASTICSEARCH_INDEX_NAME="landmatrix_test", CELERY_ALWAYS_EAGER=True
    )
    def test_administrator(self):
        # Delete deal as administrator
        activity = HistoricalActivity.objects.latest_only().public().latest()
        data = {
            # Action comment
            "tg_action_comment": "Test delete deal"
        }
        request = self.factory.post(
            reverse("delete_deal", kwargs={"deal_id": activity.activity_identifier}),
            data,
        )
        # Mock messages framework (not available for unit tests)
        setattr(request, "session", {})
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        request.user = self.users["administrator"]
        response = DealDeleteView.as_view()(
            request, deal_id=activity.activity_identifier
        )
        # if response.status_code == 200:
        #    # For debugging purposes
        #    errors = list(filter(None, [form.errors or None for form in response.context_data['forms']]))
        #    self.assertEqual(errors, [])
        self.assertEqual(response.status_code, 302, msg="Delete deal does not redirect")

        activity = HistoricalActivity.objects.latest_only().deleted().latest()

        self.assert_deal_deleted(activity, self.users["administrator"])
