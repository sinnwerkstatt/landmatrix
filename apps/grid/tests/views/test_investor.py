from datetime import datetime

import pytz
from django.contrib.auth import get_user_model
from django.contrib.messages.storage.fallback import FallbackStorage
from django.core.management import call_command
from django.http import QueryDict
from django.test import RequestFactory, TestCase, override_settings

from apps.api.elasticsearch import es_save
from apps.grid.views.investor import *
from apps.landmatrix.tests.mixins import (
    InvestorsFixtureMixin,
    ElasticSearchFixtureMixin,
    InvestorVentureInvolvementsFixtureMixin,
)
from .base import BaseInvestorTestCase, PermissionsTestCaseMixin


class InvestorListViewTestCase(
    ElasticSearchFixtureMixin, PermissionsTestCaseMixin, TestCase
):

    act_fixtures = [
        {"id": 1, "activity_identifier": 1, "attributes": {}},
        {"id": 2, "activity_identifier": 2, "attributes": {}},
        {"id": 3, "activity_identifier": 3, "attributes": {}},
        {"id": 4, "activity_identifier": 4, "attributes": {}},
        {"id": 5, "activity_identifier": 5, "attributes": {}},
    ]

    inv_fixtures = [
        {"id": 1, "investor_identifier": 1, "name": "Test Investor #1"},
        {"id": 2, "investor_identifier": 2, "name": "Test Investor #2"},
        {
            "id": 3,
            "investor_identifier": 2,
            "fk_status_id": 1,
            "name": "Test Investor #2",
        },
        {"id": 4, "investor_identifier": 3, "name": "Test Investor #3"},
        {"id": 5, "investor_identifier": 4, "name": "Test Investor #4"},
        {"id": 6, "investor_identifier": 5, "name": "Test Investor #5"},
        {"id": 7, "investor_identifier": 6, "name": "Test Investor #6"},
    ]

    act_inv_fixtures = {"1": "1", "2": "2", "4": "4", "5": "6"}

    inv_inv_fixtures = [
        {"fk_venture_id": "4", "fk_investor_id": "5", "role": "IN"},
        {"fk_venture_id": "6", "fk_investor_id": "7", "role": "ST"},
    ]

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_without_group(self):
        response = self.client.get(reverse("investor_list"))
        self.assertEqual(200, response.status_code)
        self.assertEqual("all", response.context.get("group"))
        items = response.context.get("data", {}).get("items")
        self.assertGreater(len(items), 0)
        self.assertEqual([1], items[0].get("investor_identifier"))
        self.assertEqual(["Test Investor #1"], items[0].get("name"))
        self.assertEqual(["Cambodia"], items[0].get("fk_country"))
        self.assertEqual(["Private company"], items[0].get("classification"))
        self.assertGreater(items[0].get("deal_count")[0], 0)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_with_group_fk_country(self):
        response = self.client.get(
            reverse("investor_list", kwargs={"group": "fk_country"})
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual("fk_country", response.context.get("group_slug"))
        items = response.context.get("data", {}).get("items")
        self.assertGreater(len(items), 0)
        expected = {"display": "Cambodia", "value": "116"}
        self.assertEqual(expected, items[0].get("fk_country"))
        self.assertGreater(items[0].get("investor_count")[0], 0)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_with_group_role(self):
        response = self.client.get(reverse("investor_list", kwargs={"group": "role"}))
        self.assertEqual(200, response.status_code)
        self.assertEqual("role", response.context.get("group_slug"))
        items = response.context.get("data", {}).get("items")
        self.assertGreater(len(items), 0)
        expected = {r[1] for r in InvestorBase.ROLE_CHOICES}
        self.assertEqual(
            expected, set(i.get("roles", {}).get("display") for i in items)
        )

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_with_group_value(self):
        response = self.client.get(
            reverse(
                "investor_list",
                kwargs={"group": "fk_country", "group_value": "cambodia"},
            )
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual("fk_country", response.context.get("group_slug"))
        self.assertEqual("cambodia", response.context.get("group_value"))
        items = response.context.get("data", {}).get("items")
        self.assertGreater(len(items), 0)
        self.assertEqual([1], items[0].get("investor_identifier"))
        self.assertEqual(["Test Investor #1"], items[0].get("name"))
        self.assertEqual(["Cambodia"], items[0].get("fk_country"))
        self.assertEqual(["Private company"], items[0].get("classification"))

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_with_admin(self):
        self.client.login(username="administrator", password="test")
        response = self.client.get(reverse("investor_list"))
        self.client.logout()
        self.assertEqual(200, response.status_code)
        self.assertEqual("all", response.context.get("group"))
        items = response.context.get("data", {}).get("items")
        self.assertGreater(len(items), 0)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_with_parent_filters(self):
        request = RequestFactory().get(reverse("investor_list"))
        request.user = get_user_model().objects.get(username="reporter")
        request.session = {
            "investor:filters": {
                "filter_1": {
                    "name": "filter_1",
                    "variable": "parent_stakeholder_name",
                    "operator": "is",
                    "value": "Test Investor #6",
                    "label": "Parent company Name",
                    "key": None,
                    "display_value": "Test Investor #6",
                }
            }
        }
        response = InvestorListView.as_view()(request)
        response = response.render()
        self.assertEqual(200, response.status_code)
        self.assertEqual("all", response.context_data.get("group"))
        items = response.context_data.get("data", {}).get("items")
        self.assertGreater(len(items), 0)
        self.assertEqual([5], items[0].get("investor_identifier"))
        self.assertEqual(["Test Investor #5"], items[0].get("name"))
        self.assertEqual(["Cambodia"], items[0].get("fk_country"))
        self.assertEqual(["Private company"], items[0].get("classification"))
        self.assertGreater(items[0].get("deal_count")[0], 0)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_with_status_filter(self):
        request = RequestFactory().get(reverse("investor_list"))
        request.user = get_user_model().objects.get(username="administrator")
        request.session = {}
        request.GET = QueryDict("status=1&status=2&status=3")
        response = InvestorListView.as_view()(request)
        response = response.render()
        self.assertEqual(200, response.status_code)
        self.assertEqual("all", response.context_data.get("group"))
        items = response.context_data.get("data", {}).get("items")
        self.assertGreater(len(items), 0)
        self.assertEqual([1], items[0].get("investor_identifier"))
        self.assertEqual(["Test Investor #1"], items[0].get("name"))
        self.assertEqual(["Cambodia"], items[0].get("fk_country"))
        self.assertEqual(["Private company"], items[0].get("classification"))
        self.assertGreater(items[0].get("deal_count")[0], 0)


class InvestorCreateViewTestCase(InvestorsFixtureMixin, BaseInvestorTestCase):

    inv_fixtures = [{"id": 1, "investor_identifier": 1, "name": "Test Investor #1"}]

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_get(self):
        self.client.login(username="reporter", password="test")
        response = self.client.get(reverse("investor_add"))
        self.client.logout()
        self.assertEqual(200, response.status_code)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_reporter(self):
        data = self.INVESTOR_DATA.copy()
        data.update({"action_comment": "Test add investor"})
        self.client.login(username="reporter", password="test")
        response = self.client.post(reverse("investor_add"), data)
        self.client.logout()
        self.assertEqual(
            302, response.status_code, msg="Add investor does not redirect"
        )
        investor = HistoricalInvestor.objects.latest_only().pending().latest()
        self.assertEqual("Test add investor", investor.action_comment)
        self.assertEqual(HistoricalInvestor.STATUS_PENDING, investor.fk_status_id)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_editor(self):
        data = self.INVESTOR_DATA.copy()
        data.update({"action_comment": "Test add investor"})
        self.client.login(username="editor", password="test")
        response = self.client.post(reverse("investor_add"), data)
        self.client.logout()
        self.assertEqual(
            302, response.status_code, msg="Add investor does not redirect"
        )
        investor = HistoricalInvestor.objects.latest_only().pending().latest()
        self.assertEqual("Test add investor", investor.action_comment)
        self.assertEqual(HistoricalInvestor.STATUS_PENDING, investor.fk_status_id)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_administrator(self):
        data = self.INVESTOR_DATA.copy()
        data.update({"action_comment": "Test add investor", "approve_btn": True})
        self.client.login(username="administrator", password="test")
        response = self.client.post(reverse("investor_add"), data)
        self.client.logout()
        self.assertEqual(
            302, response.status_code, msg="Add investor does not redirect"
        )
        investor = HistoricalInvestor.objects.latest_only().public().latest()
        self.assertEqual("Test add investor", investor.action_comment)
        self.assertEqual(HistoricalInvestor.STATUS_ACTIVE, investor.fk_status_id)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_invalid(self):
        data = self.INVESTOR_DATA.copy()
        data["fk_country"] = "9999"
        self.client.login(username="reporter", password="test")
        response = self.client.post(reverse("investor_add"), data)
        self.client.logout()
        self.assertEqual(200, response.status_code)

        messages = list(response.context.get("messages"))
        self.assertGreater(len(messages), 0)
        self.assertEqual("Please correct the error below.", messages[-1].message)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_popup(self):
        data = self.INVESTOR_DATA.copy()
        request = RequestFactory().post(reverse("investor_add"), data)
        request.user = get_user_model().objects.get(username="reporter")
        request.GET = QueryDict("popup=1")
        request.POST = data
        request.session = {}
        request._messages = FallbackStorage(request)
        response = InvestorCreateView.as_view()(request)
        self.assertEqual(200, response.status_code)
        self.assertIn(b"opener.dismissAddInvestorPopup", response.content)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_with_parent_id(self):
        data = self.INVESTOR_DATA.copy()
        request = RequestFactory().post(reverse("investor_add"), data)
        request.user = get_user_model().objects.get(username="reporter")
        request.GET = QueryDict("parent_id=2")
        request.POST = data
        request.session = {}
        request._messages = FallbackStorage(request)
        response = InvestorCreateView.as_view()(request)
        self.assertEqual(302, response.status_code)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_reject(self):
        data = self.INVESTOR_DATA.copy()
        data.update({"tg_action_comment": "Test add investor", "reject_btn": "on"})
        self.client.login(username="administrator", password="test")
        response = self.client.post(reverse("investor_add"), data)
        self.client.logout()
        self.assertEqual(302, response.status_code, msg="Add deal does not redirect")
        investor = HistoricalInvestor.objects.latest_only().rejected().latest()
        self.assertEqual("Test comment", investor.comment)
        self.assertEqual(HistoricalInvestor.STATUS_REJECTED, investor.fk_status_id)

    def test_parent_company_role(self):
        data = self.INVESTOR_DATA.copy()
        data.update({"tg_action_comment": "Test add investor"})
        request = RequestFactory().post(reverse("investor_add"), data)
        request.user = get_user_model().objects.get(username="reporter")
        request.GET = QueryDict("role=parent_company")
        request.POST = data
        request.session = {}
        request._messages = FallbackStorage(request)
        response = InvestorCreateView.as_view()(request)
        self.assertEqual(302, response.status_code)

    def test_tertiary_investor_lender_role(self):
        data = self.INVESTOR_DATA.copy()
        data.update({"tg_action_comment": "Test add investor"})
        request = RequestFactory().post(reverse("investor_add"), data)
        request.user = get_user_model().objects.get(username="reporter")
        request.GET = QueryDict("role=parent_investor")
        request.POST = data
        request.session = {}
        request._messages = FallbackStorage(request)
        response = InvestorCreateView.as_view()(request)
        self.assertEqual(302, response.status_code)


class InvestorUpdateViewTestCase(InvestorsFixtureMixin, BaseInvestorTestCase):

    fixtures = ["languages", "countries_and_regions", "users_and_groups", "status"]

    inv_fixtures = [
        {"id": 1, "investor_identifier": 1, "name": "Test Investor #1"},
        {"id": 2, "investor_identifier": 2, "name": "Test Investor #2"},
        {
            "id": 3,
            "investor_identifier": 2,
            "fk_status_id": 1,
            "history_date": datetime(2000, 1, 2, 0, 0, tzinfo=pytz.utc),
            "name": "Test Investor #2",
        },
    ]

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_get(self):
        self.client.login(username="reporter", password="test")
        response = self.client.get(
            reverse("investor_update", kwargs={"investor_id": 1})
        )
        self.client.logout()
        self.assertEqual(200, response.status_code)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_reporter(self):
        data = self.INVESTOR_DATA.copy()
        data.update({"action_comment": "Test change investor"})
        self.client.login(username="reporter", password="test")
        response = self.client.post(
            reverse("investor_update", kwargs={"investor_id": 1}), data
        )
        self.client.logout()
        self.assertEqual(
            302, response.status_code, msg="Change investor does not redirect"
        )
        investor = HistoricalInvestor.objects.latest_only().pending().latest()
        self.assertEqual(1, investor.investor_identifier)
        self.assertEqual("Test change investor", investor.action_comment)
        self.assertEqual(HistoricalInvestor.STATUS_PENDING, investor.fk_status_id)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_editor(self):
        data = self.INVESTOR_DATA.copy()
        data.update({"action_comment": "Test change investor"})
        self.client.login(username="editor", password="test")
        response = self.client.post(
            reverse("investor_update", kwargs={"investor_id": 1}), data
        )
        self.client.logout()
        self.assertEqual(
            302, response.status_code, msg="Change investor does not redirect"
        )
        investor = HistoricalInvestor.objects.latest_only().pending().latest()
        self.assertEqual(1, investor.investor_identifier)
        self.assertEqual("Test change investor", investor.action_comment)
        self.assertEqual(HistoricalInvestor.STATUS_PENDING, investor.fk_status_id)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_editor_reject(self):
        data = self.INVESTOR_DATA.copy()
        data.update({"action_comment": "Test change investor", "reject_btn": "on"})
        self.client.login(username="administrator", password="test")
        response = self.client.post(
            reverse("investor_update", kwargs={"investor_id": 2, "history_id": 3}), data
        )
        self.client.logout()
        self.assertEqual(
            302, response.status_code, msg="Change investor does not redirect"
        )
        investor = HistoricalInvestor.objects.get(id=3)
        self.assertEqual(2, investor.investor_identifier)
        self.assertEqual(HistoricalInvestor.STATUS_REJECTED, investor.fk_status_id)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_administrator(self):
        data = self.INVESTOR_DATA.copy()
        data.update({"action_comment": "Test change investor", "approve_btn": True})
        self.client.login(username="administrator", password="test")
        response = self.client.post(
            reverse("investor_update", kwargs={"investor_id": 1}), data
        )
        self.client.logout()
        self.assertEqual(
            302, response.status_code, msg="Change investor does not redirect"
        )
        investor = HistoricalInvestor.objects.latest_only().public().latest()
        self.assertEqual(1, investor.investor_identifier)
        self.assertEqual("Test change investor", investor.action_comment)
        self.assertEqual(HistoricalInvestor.STATUS_OVERWRITTEN, investor.fk_status_id)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_invalid(self):
        data = self.INVESTOR_DATA.copy()
        data["fk_country"] = "9999"
        self.client.login(username="reporter", password="test")
        response = self.client.post(
            reverse("investor_update", kwargs={"investor_id": 1}), data
        )
        self.client.logout()
        self.assertEqual(200, response.status_code)

        messages = list(response.context.get("messages"))
        self.assertGreater(len(messages), 0)
        self.assertEqual("Please correct the error below.", messages[-1].message)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_reporter_pending(self):
        data = self.INVESTOR_DATA.copy()
        data.update({"action_comment": "Test change investor"})
        self.client.login(username="reporter", password="test")
        response = self.client.post(
            reverse("investor_update", kwargs={"investor_id": 2, "history_id": 3}), data
        )
        self.client.logout()
        self.assertEqual(302, response.status_code)
        self.assertEqual("/investor/2/3/", response.url)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_does_not_exist(self):
        self.client.login(username="editor", password="test")
        response = self.client.get(
            reverse("investor_update", kwargs={"investor_id": 123})
        )
        self.client.logout()
        self.assertEqual(404, response.status_code)

    def test_with_history_id(self):
        data = self.INVESTOR_DATA.copy()
        data.update({"action_comment": "Test change investor"})
        self.client.login(username="editor", password="test")
        response = self.client.post(
            reverse("investor_update", kwargs={"investor_id": 1, "history_id": 1}), data
        )
        self.client.logout()
        self.assertEqual(
            302, response.status_code, msg="Change investor does not redirect"
        )
        investor = HistoricalInvestor.objects.latest_only().pending().latest()
        self.assertEqual(1, investor.investor_identifier)
        self.assertEqual("Test change investor", investor.action_comment)
        self.assertEqual(HistoricalInvestor.STATUS_PENDING, investor.fk_status_id)

    def test_not_editable(self):
        self.client.login(username="editor", password="test")
        response = self.client.get(
            reverse("investor_update", kwargs={"investor_id": 2, "history_id": 2})
        )
        self.client.logout()
        self.assertEqual(302, response.status_code)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_popup(self):
        data = self.INVESTOR_DATA.copy()
        data.update({"action_comment": "Test change investor"})
        request = RequestFactory().post(
            reverse("investor_update", kwargs={"investor_id": 1}), data
        )
        request.user = get_user_model().objects.get(username="reporter")
        request.GET = QueryDict("popup=1")
        request.POST = data
        request.session = {}
        request._messages = FallbackStorage(request)
        response = InvestorUpdateView.as_view()(request, investor_id=1)
        self.assertEqual(200, response.status_code)
        self.assertIn(b"opener.dismissChangeInvestorPopup", response.content)


class InvestorDetailViewTestCase(InvestorsFixtureMixin, BaseInvestorTestCase):

    fixtures = ["languages", "countries_and_regions", "users_and_groups", "status"]

    inv_fixtures = [
        {"id": 1, "investor_identifier": 1, "name": "Test Investor #1"},
        {
            "id": 2,
            "investor_identifier": 2,
            "fk_status_id": 4,
            "name": "Test Investor #2",
        },
    ]

    def test_with_anonymous(self):
        response = self.client.get(
            reverse("investor_detail", kwargs={"investor_id": 1})
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response.context.get("investor").investor_identifier)

    def test_with_anonymous_not_public(self):
        response = self.client.get(
            reverse("investor_detail", kwargs={"investor_id": 2})
        )
        self.assertEqual(404, response.status_code)

    def test_reporter(self):
        self.client.login(username="reporter", password="test")
        response = self.client.get(
            reverse("investor_detail", kwargs={"investor_id": 1})
        )
        self.client.logout()
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response.context.get("investor").investor_identifier)

    def test_deleted(self):
        self.client.login(username="editor", password="test")
        response = self.client.get(
            reverse("investor_detail", kwargs={"investor_id": 2})
        )
        self.client.logout()
        self.assertEqual(404, response.status_code)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_does_not_exist(self):
        self.client.login(username="editor", password="test")
        response = self.client.get(
            reverse("investor_detail", kwargs={"investor_id": 123})
        )
        self.client.logout()
        self.assertEqual(404, response.status_code)

    def test_with_history_id(self):
        self.client.login(username="editor", password="test")
        response = self.client.get(
            reverse("investor_detail", kwargs={"investor_id": 1, "history_id": 1})
        )
        self.client.logout()
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response.context.get("investor").investor_identifier)


class InvestorDeleteViewTestCase(InvestorsFixtureMixin, BaseInvestorTestCase):

    fixtures = ["countries_and_regions", "users_and_groups", "status"]

    inv_fixtures = [
        {"id": 1, "investor_identifier": 1, "name": "Test Investor #1"},
        {
            "id": 2,
            "investor_identifier": 2,
            "fk_status_id": 4,
            "name": "Test Investor #2",
        },
    ]

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_get(self):
        self.client.login(username="editor", password="test")
        response = self.client.get(
            reverse("investor_delete", kwargs={"investor_id": 1})
        )
        self.client.logout()
        self.assertEqual(302, response.status_code)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_reporter(self):
        data = self.INVESTOR_DATA.copy()
        data.update({"action_comment": "Test delete investor"})
        self.client.login(username="reporter", password="test")
        response = self.client.post(
            reverse("investor_delete", kwargs={"investor_id": 1}), data
        )
        self.client.logout()
        self.assertEqual(
            302, response.status_code, msg="Delete investor does not redirect"
        )
        investor = HistoricalInvestor.objects.latest_only().to_delete().latest()
        self.assertEqual(1, investor.investor_identifier)
        # self.assertEqual('Test delete investor', investor.action_comment)
        self.assertEqual(HistoricalInvestor.STATUS_TO_DELETE, investor.fk_status_id)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_editor(self):
        data = self.INVESTOR_DATA.copy()
        data.update({"action_comment": "Test delete investor"})
        self.client.login(username="editor", password="test")
        response = self.client.post(
            reverse("investor_delete", kwargs={"investor_id": 1}), data
        )
        self.client.logout()
        self.assertEqual(
            302, response.status_code, msg="Delete investor does not redirect"
        )
        investor = HistoricalInvestor.objects.latest_only().to_delete().latest()
        self.assertEqual(1, investor.investor_identifier)
        # self.assertEqual('Test delete investor', investor.action_comment)
        self.assertEqual(HistoricalInvestor.STATUS_TO_DELETE, investor.fk_status_id)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_administrator(self):
        data = self.INVESTOR_DATA.copy()
        data.update({"action_comment": "Test delete investor", "approve_btn": True})
        self.client.login(username="administrator", password="test")
        response = self.client.post(
            reverse("investor_delete", kwargs={"investor_id": 1}), data
        )
        self.client.logout()
        self.assertEqual(
            302, response.status_code, msg="Delete investor does not redirect"
        )
        investor = HistoricalInvestor.objects.latest_only().deleted().latest()
        self.assertEqual(1, investor.investor_identifier)
        # self.assertEqual('Test delete investor', investor.action_comment)
        self.assertEqual(HistoricalInvestor.STATUS_DELETED, investor.fk_status_id)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_does_not_exist(self):
        data = self.INVESTOR_DATA.copy()
        data.update({"action_comment": "Test delete investor"})
        self.client.login(username="editor", password="test")
        response = self.client.post(
            reverse("investor_delete", kwargs={"investor_id": 123})
        )
        self.client.logout()
        self.assertEqual(404, response.status_code)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_already_deleted(self):
        data = self.INVESTOR_DATA.copy()
        data.update({"action_comment": "Test delete investor"})
        self.client.login(username="editor", password="test")
        response = self.client.post(
            reverse("investor_delete", kwargs={"investor_id": 2}), data
        )
        self.client.logout()
        self.assertEqual(404, response.status_code)


class InvestorRecoverViewTestCase(InvestorsFixtureMixin, BaseInvestorTestCase):

    fixtures = ["countries_and_regions", "users_and_groups", "status"]

    inv_fixtures = [
        {
            "id": 1,
            "investor_identifier": 1,
            "fk_status_id": 4,
            "name": "Test Investor #1",
        },
        {"id": 2, "investor_identifier": 2, "name": "Test Investor #2"},
    ]

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_get(self):
        self.client.login(username="editor", password="test")
        response = self.client.get(
            reverse("investor_recover", kwargs={"investor_id": 1})
        )
        self.client.logout()
        self.assertEqual(302, response.status_code)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_editor(self):
        data = self.INVESTOR_DATA.copy()
        data.update({"action_comment": "Test recover investor"})
        self.client.login(username="editor", password="test")
        response = self.client.post(
            reverse("investor_recover", kwargs={"investor_id": 1}), data
        )
        self.client.logout()
        self.assertEqual(
            302, response.status_code, msg="Recover investor does not redirect"
        )
        self.assertEqual(
            0,
            HistoricalInvestor.objects.filter(comment="Test recover investor").count(),
        )

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_administrator(self):
        data = self.INVESTOR_DATA.copy()
        data.update({"action_comment": "Test recover investor", "approve_btn": True})
        self.client.login(username="administrator", password="test")
        response = self.client.post(
            reverse("investor_recover", kwargs={"investor_id": 1}), data
        )
        self.client.logout()
        self.assertEqual(
            302, response.status_code, msg="Recover investor does not redirect"
        )
        investor = HistoricalInvestor.objects.latest_only().public().latest()
        self.assertEqual(1, investor.investor_identifier)
        # self.assertEqual('Test recover investor', investor.action_comment)
        self.assertEqual(HistoricalInvestor.STATUS_OVERWRITTEN, investor.fk_status_id)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_does_not_exist(self):
        self.client.login(username="editor", password="test")
        response = self.client.get(
            reverse("investor_recover", kwargs={"investor_id": 123})
        )
        self.client.logout()
        self.assertEqual(404, response.status_code)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_not_deleted(self):
        self.client.login(username="editor", password="test")
        response = self.client.get(
            reverse("investor_recover", kwargs={"investor_id": 2})
        )
        self.client.logout()
        self.assertEqual(404, response.status_code)
