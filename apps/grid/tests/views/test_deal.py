from subprocess import CalledProcessError

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase, override_settings

from apps.api.elasticsearch import es_save
from apps.grid.views.deal import *
from apps.landmatrix.tests.mixins import (
    InvestorsFixtureMixin,
    ActivitiesFixtureMixin,
    ElasticSearchFixtureMixin,
    InvestorActivityInvolvementsFixtureMixin,
)
from .base import BaseDealTestCase


class DealListViewTestCase(ElasticSearchFixtureMixin, TestCase):

    act_fixtures = [
        {"id": 1, "activity_identifier": 1, "attributes": {}},
        {"id": 2, "activity_identifier": 2, "attributes": {}},
        {"id": 3, "activity_identifier": 3, "fk_status_id": 1, "attributes": {}},
    ]
    inv_fixtures = [{"id": 1, "investor_identifier": 1, "name": "Test Investor #1"}]
    act_inv_fixtures = {"1": "1", "2": "1", "3": "1"}

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_without_group(self):
        response = self.client.get(reverse("data"))
        self.assertEqual(200, response.status_code)
        self.assertEqual("all", response.context.get("group"))
        items = response.context.get("data", {}).get("items")
        self.assertGreater(len(items), 0)
        self.assertEqual([1], items[0].get("activity_identifier"))
        self.assertEqual(["Myanmar"], items[0].get("target_country"))
        self.assertEqual(
            [{"id": "1", "name": "Test Investor 1"}], items[0].get("top_investors", [])
        )
        self.assertEqual([200], items[0].get("deal_size"))

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_with_group(self):
        response = self.client.get(
            reverse("deal_list", kwargs={"group": "target_country"})
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual("target_country", response.context.get("group"))
        items = response.context.get("data", {}).get("items")
        self.assertEqual(1, len(items))
        self.assertEqual("Myanmar", items[0].get("target_country", {}).get("display"))
        self.assertEqual(["Asia"], items[0].get("target_region"))
        self.assertGreater(items[0].get("deal_count")[0], 0)
        self.assertEqual([400], items[0].get("deal_size"))

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_with_group_value(self):
        response = self.client.get(
            reverse(
                "deal_list",
                kwargs={"group": "target_country", "group_value": "myanmar"},
            )
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual("target_country", response.context.get("group"))
        self.assertEqual("myanmar", response.context.get("group_value"))
        items = response.context.get("data", {}).get("items")
        self.assertGreater(len(items), 0)
        self.assertEqual([1], items[0].get("activity_identifier"))
        self.assertEqual(["Myanmar"], items[0].get("target_country"))
        self.assertEqual(
            [{"id": "1", "name": "Test Investor 1"}], items[0].get("top_investors", [])
        )
        self.assertEqual([200], items[0].get("deal_size"))


class DealCreateViewTestCase(InvestorsFixtureMixin, BaseDealTestCase):

    inv_fixtures = [{"id": 1, "investor_identifier": 1, "name": "Test Investor #1"}]

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_get(self):
        self.client.login(username="reporter", password="test")
        response = self.client.get(reverse("add_deal"))
        self.client.logout()
        self.assertEqual(200, response.status_code)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_reporter(self):
        data = self.DEAL_DATA.copy()
        data.update({"tg_action_comment": "Test add deal"})
        self.client.login(username="reporter", password="test")
        response = self.client.post(reverse("add_deal"), data)
        self.client.logout()
        self.assertEqual(302, response.status_code, msg="Add deal does not redirect")
        activity = HistoricalActivity.objects.latest_only().pending().latest()
        self.assertEqual(1, activity.activity_identifier)
        self.assertEqual("Test add deal", activity.comment)
        self.assertEqual(HistoricalActivity.STATUS_PENDING, activity.fk_status_id)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_editor(self):
        data = self.DEAL_DATA.copy()
        data.update({"tg_action_comment": "Test add deal"})
        self.client.login(username="editor", password="test")
        response = self.client.post(reverse("add_deal"), data)
        self.client.logout()
        self.assertEqual(302, response.status_code, msg="Add deal does not redirect")
        activity = HistoricalActivity.objects.latest_only().pending().latest()
        self.assertEqual(1, activity.activity_identifier)
        self.assertEqual("Test add deal", activity.comment)
        self.assertEqual(HistoricalActivity.STATUS_PENDING, activity.fk_status_id)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_administrator(self):
        data = self.DEAL_DATA.copy()
        data.update(
            {
                "operational_stakeholder": self.INVESTOR_CREATED,
                "tg_action_comment": "Test add deal",
                "approve_btn": True,
            }
        )
        self.client.login(username="administrator", password="test")
        response = self.client.post(reverse("add_deal"), data)
        self.client.logout()
        self.assertEqual(302, response.status_code, msg="Add deal does not redirect")
        activity = HistoricalActivity.objects.latest_only().public().latest()
        self.assertEqual(1, activity.activity_identifier)
        self.assertEqual("Test add deal", activity.comment)
        self.assertEqual(HistoricalActivity.STATUS_ACTIVE, activity.fk_status_id)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_invalid(self):
        data = self.DEAL_DATA.copy()
        self.client.login(username="reporter", password="test")
        response = self.client.post(reverse("add_deal"), data)
        self.client.logout()
        self.assertEqual(200, response.status_code)

        messages = list(response.context.get("messages"))
        self.assertGreater(len(messages), 0)
        self.assertEqual("Please correct the error below.", messages[-1].message)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_reject(self):
        data = self.DEAL_DATA.copy()
        data.update({"tg_action_comment": "Test add deal", "reject_btn": "on"})
        self.client.login(username="administrator", password="test")
        response = self.client.post(reverse("add_deal"), data)
        self.client.logout()
        self.assertEqual(302, response.status_code, msg="Add deal does not redirect")
        activity = HistoricalActivity.objects.latest_only().rejected().latest()
        self.assertEqual("Test add deal", activity.comment)
        self.assertEqual(HistoricalActivity.STATUS_REJECTED, activity.fk_status_id)


class DealUpdateViewTestCase(
    ActivitiesFixtureMixin,
    InvestorsFixtureMixin,
    InvestorActivityInvolvementsFixtureMixin,
    BaseDealTestCase,
):

    act_fixtures = [
        {"id": 1, "activity_identifier": 1, "attributes": {}},
        {"id": 2, "activity_identifier": 2, "attributes": {}},
        {"id": 3, "activity_identifier": 2, "fk_status_id": 1, "attributes": {}},
    ]
    inv_fixtures = [{"id": 1, "investor_identifier": 1}]
    act_inv_fixtures = {"1": "1", "2": "1", "3": "1"}

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_get(self):
        """

        :return:
        """
        self.client.login(username="reporter", password="test")
        response = self.client.get(reverse("change_deal", kwargs={"deal_id": 1}))
        self.client.logout()
        self.assertEqual(200, response.status_code)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_reporter(self):
        data = self.DEAL_DATA.copy()
        data.update({"tg_action_comment": "Test change deal"})
        self.client.login(username="reporter", password="test")
        response = self.client.post(reverse("change_deal", kwargs={"deal_id": 1}), data)
        self.client.logout()
        self.assertEqual(302, response.status_code, msg="Change deal does not redirect")
        activity = HistoricalActivity.objects.latest_only().pending().latest()
        self.assertEqual(1, activity.activity_identifier)
        self.assertEqual("Test change deal", activity.comment)
        self.assertEqual(HistoricalActivity.STATUS_PENDING, activity.fk_status_id)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_editor(self):
        data = self.DEAL_DATA.copy()
        data.update({"tg_action_comment": "Test change deal"})
        self.client.login(username="editor", password="test")
        response = self.client.post(reverse("change_deal", kwargs={"deal_id": 1}), data)
        self.client.logout()
        self.assertEqual(302, response.status_code, msg="Change deal does not redirect")
        activity = HistoricalActivity.objects.latest_only().pending().latest()
        self.assertEqual(1, activity.activity_identifier)
        self.assertEqual("Test change deal", activity.comment)
        self.assertEqual(HistoricalActivity.STATUS_PENDING, activity.fk_status_id)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_administrator(self):
        data = self.DEAL_DATA.copy()
        data.update(
            {
                "operational_stakeholder": self.INVESTOR_CREATED,
                "tg_action_comment": "Test change deal",
                "approve_btn": True,
            }
        )
        self.client.login(username="administrator", password="test")
        response = self.client.post(reverse("change_deal", kwargs={"deal_id": 1}), data)
        self.client.logout()
        self.assertEqual(302, response.status_code, msg="Change deal does not redirect")
        activity = HistoricalActivity.objects.latest_only().public().latest()
        self.assertEqual(1, activity.activity_identifier)
        self.assertEqual("Test change deal", activity.comment)
        self.assertEqual(HistoricalActivity.STATUS_OVERWRITTEN, activity.fk_status_id)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_editor_feedback(self):
        data = self.DEAL_DATA.copy()
        data.update({"tg_action_comment": "Test change deal", "assign_to_user": "3"})
        self.client.login(username="editor", password="test")
        response = self.client.post(reverse("change_deal", kwargs={"deal_id": 1}), data)
        self.client.logout()
        self.assertEqual(302, response.status_code, msg="Change deal does not redirect")
        activity = HistoricalActivity.objects.latest_only().pending().latest()
        self.assertGreater(activity.activityfeedback_set.count(), 0)
        feedback = activity.activityfeedback_set.first()
        self.assertEqual(3, feedback.fk_user_assigned_id)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_invalid(self):
        data = self.DEAL_DATA.copy()
        self.client.login(username="reporter", password="test")
        response = self.client.post(reverse("change_deal", kwargs={"deal_id": 1}), data)
        self.client.logout()
        self.assertEqual(200, response.status_code)

        messages = list(response.context.get("messages"))
        self.assertGreater(len(messages), 0)
        self.assertEqual("Please correct the error below.", messages[-1].message)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_reporter_pending(self):
        data = self.DEAL_DATA.copy()
        data.update({"tg_action_comment": "Test change deal"})
        self.client.login(username="reporter", password="test")
        response = self.client.post(
            reverse("change_deal", kwargs={"deal_id": 2, "history_id": 3}), data
        )
        self.client.logout()
        self.assertEqual(302, response.status_code)
        self.assertEqual("/deal/2/3/", response.url)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_does_not_exist(self):
        self.client.login(username="editor", password="test")
        response = self.client.get(reverse("change_deal", kwargs={"deal_id": 123}))
        self.client.logout()
        self.assertEqual(404, response.status_code)

    def test_with_history_id(self):
        data = self.DEAL_DATA.copy()
        data.update({"tg_action_comment": "Test change deal"})
        self.client.login(username="editor", password="test")
        response = self.client.post(
            reverse("change_deal", kwargs={"deal_id": 1, "history_id": 1}), data
        )
        self.client.logout()
        self.assertEqual(302, response.status_code, msg="Change deal does not redirect")
        activity = HistoricalActivity.objects.latest_only().pending().latest()
        self.assertEqual(1, activity.activity_identifier)
        self.assertEqual("Test change deal", activity.comment)
        self.assertEqual(HistoricalActivity.STATUS_PENDING, activity.fk_status_id)

    def test_not_editable(self):
        self.client.login(username="editor", password="test")
        response = self.client.get(
            reverse("change_deal", kwargs={"deal_id": 2, "history_id": 2})
        )
        self.client.logout()
        self.assertEqual(302, response.status_code)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_reject(self):
        data = self.DEAL_DATA.copy()
        data.update({"tg_action_comment": "Test change deal", "reject_btn": "on"})
        self.client.login(username="administrator", password="test")
        response = self.client.post(
            reverse("change_deal", kwargs={"deal_id": 2, "history_id": 3}), data
        )
        self.client.logout()
        self.assertEqual(302, response.status_code, msg="Change deal does not redirect")
        activity = HistoricalActivity.objects.get(id=3)
        self.assertEqual(2, activity.activity_identifier)
        self.assertEqual(HistoricalActivity.STATUS_REJECTED, activity.fk_status_id)

    def test_with_country_specific_form(self):
        # Overwrite target country with Mongolia
        activity = HistoricalActivity.objects.get(id=1)
        activity.attributes.filter(name="target_country").update(value="496")

        data = self.DEAL_DATA.copy()
        data.update({"tg_action_comment": "Test change deal"})
        self.client.login(username="editor", password="test")
        response = self.client.post(reverse("change_deal", kwargs={"deal_id": 1}), data)
        self.client.logout()
        self.assertEqual(302, response.status_code, msg="Change deal does not redirect")
        activity = HistoricalActivity.objects.latest_only().pending().latest()
        self.assertEqual(1, activity.activity_identifier)
        self.assertEqual("Test change deal", activity.comment)
        self.assertEqual(HistoricalActivity.STATUS_PENDING, activity.fk_status_id)


class DealDetailViewTestCase(
    ActivitiesFixtureMixin,
    InvestorsFixtureMixin,
    InvestorActivityInvolvementsFixtureMixin,
    BaseDealTestCase,
):

    act_fixtures = [
        {"id": 1, "activity_identifier": 1, "attributes": {}},
        {"id": 2, "activity_identifier": 2, "fk_status_id": 4, "attributes": {}},
    ]
    inv_fixtures = [{"id": 1, "investor_identifier": 1}]
    act_inv_fixtures = {"1": "1", "2": "1"}

    def test_with_anonymous(self):
        response = self.client.get(reverse("deal_detail", kwargs={"deal_id": 1}))
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response.context.get("activity").activity_identifier)

    def test_with_anonymous_not_public(self):
        response = self.client.get(reverse("deal_detail", kwargs={"deal_id": 2}))
        self.assertEqual(404, response.status_code)

    def test_with_reporter(self):
        self.client.login(username="reporter", password="test")
        response = self.client.get(reverse("deal_detail", kwargs={"deal_id": 1}))
        self.client.logout()
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response.context.get("activity").activity_identifier)

    def test_deleted(self):
        self.client.login(username="editor", password="test")
        response = self.client.get(reverse("deal_detail", kwargs={"deal_id": 2}))
        self.client.logout()
        self.assertEqual(404, response.status_code)

    def test_with_pdf(self):
        self.client.login(username="reporter", password="test")
        # We cannot render PDF since it requires wkhtmltopdf to be able to access the detail page URL
        with self.assertRaises(CalledProcessError):
            response = self.client.get(
                reverse("deal_detail_pdf", kwargs={"deal_id": 1})
            )
        self.client.logout()

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_does_not_exist(self):
        self.client.login(username="editor", password="test")
        response = self.client.get(reverse("deal_detail", kwargs={"deal_id": 123}))
        self.client.logout()
        self.assertEqual(404, response.status_code)

    def test_with_history_id(self):
        self.client.login(username="editor", password="test")
        response = self.client.get(
            reverse("deal_detail", kwargs={"deal_id": 1, "history_id": 1})
        )
        self.client.logout()
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response.context.get("activity").activity_identifier)


class DealDeleteViewTestCase(
    ActivitiesFixtureMixin,
    InvestorsFixtureMixin,
    InvestorActivityInvolvementsFixtureMixin,
    BaseDealTestCase,
):

    act_fixtures = [
        {"id": 1, "activity_identifier": 1, "attributes": {}},
        {"id": 2, "activity_identifier": 2, "fk_status_id": 4, "attributes": {}},
    ]
    inv_fixtures = [{"id": 1, "investor_identifier": 1}]
    act_inv_fixtures = {"1": "1", "2": "1"}

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_get(self):
        self.client.login(username="editor", password="test")
        response = self.client.get(reverse("delete_deal", kwargs={"deal_id": 1}))
        self.client.logout()
        self.assertEqual(302, response.status_code)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_reporter(self):
        data = self.DEAL_DATA.copy()
        data.update({"tg_action_comment": "Test delete deal"})
        self.client.login(username="reporter", password="test")
        response = self.client.post(reverse("delete_deal", kwargs={"deal_id": 1}), data)
        self.client.logout()
        self.assertEqual(302, response.status_code, msg="Delete deal does not redirect")
        activity = HistoricalActivity.objects.latest_only().to_delete().latest()
        self.assertEqual(1, activity.activity_identifier)
        # self.assertEqual('Test delete deal', activity.comment)
        self.assertEqual(HistoricalActivity.STATUS_TO_DELETE, activity.fk_status_id)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_editor(self):
        data = self.DEAL_DATA.copy()
        data.update({"tg_action_comment": "Test delete deal"})
        self.client.login(username="editor", password="test")
        response = self.client.post(reverse("delete_deal", kwargs={"deal_id": 1}), data)
        self.client.logout()
        self.assertEqual(302, response.status_code, msg="Delete deal does not redirect")
        activity = HistoricalActivity.objects.latest_only().to_delete().latest()
        self.assertEqual(1, activity.activity_identifier)
        # self.assertEqual('Test delete deal', activity.comment)
        self.assertEqual(HistoricalActivity.STATUS_TO_DELETE, activity.fk_status_id)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_administrator(self):
        data = self.DEAL_DATA.copy()
        data.update({"tg_action_comment": "Test delete deal", "approve_btn": True})
        self.client.login(username="administrator", password="test")
        response = self.client.post(reverse("delete_deal", kwargs={"deal_id": 1}), data)
        self.client.logout()
        self.assertEqual(302, response.status_code, msg="Delete deal does not redirect")
        activity = HistoricalActivity.objects.latest_only().deleted().latest()
        self.assertEqual(1, activity.activity_identifier)
        # self.assertEqual('Test delete deal', activity.comment)
        self.assertEqual(HistoricalActivity.STATUS_DELETED, activity.fk_status_id)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_does_not_exist(self):
        data = self.DEAL_DATA.copy()
        data.update({"tg_action_comment": "Test delete deal"})
        self.client.login(username="editor", password="test")
        response = self.client.post(reverse("delete_deal", kwargs={"deal_id": 123}))
        self.client.logout()
        self.assertEqual(404, response.status_code)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_already_deleted(self):
        data = self.DEAL_DATA.copy()
        data.update({"tg_action_comment": "Test delete deal"})
        self.client.login(username="editor", password="test")
        response = self.client.post(reverse("delete_deal", kwargs={"deal_id": 2}), data)
        self.client.logout()
        self.assertEqual(404, response.status_code)


class DealRecoverViewTestCase(
    ActivitiesFixtureMixin,
    InvestorsFixtureMixin,
    InvestorActivityInvolvementsFixtureMixin,
    BaseDealTestCase,
):

    act_fixtures = [
        {"id": 1, "activity_identifier": 1, "fk_status_id": 4, "attributes": {}},
        {"id": 2, "activity_identifier": 2, "attributes": {}},
    ]
    inv_fixtures = [{"id": 1, "investor_identifier": 1}]
    act_inv_fixtures = {"1": "1", "2": "1"}

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_get(self):
        self.client.login(username="editor", password="test")
        response = self.client.get(reverse("recover_deal", kwargs={"deal_id": 1}))
        self.client.logout()
        self.assertEqual(302, response.status_code)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_editor(self):
        data = self.DEAL_DATA.copy()
        data.update({"tg_action_comment": "Test recover deal"})
        self.client.login(username="editor", password="test")
        response = self.client.post(
            reverse("recover_deal", kwargs={"deal_id": 1}), data
        )
        self.client.logout()
        self.assertEqual(
            302, response.status_code, msg="Recover deal does not redirect"
        )
        self.assertEqual(
            0, HistoricalActivity.objects.filter(comment="Test recover deal").count()
        )

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_administrator(self):
        data = self.DEAL_DATA.copy()
        data.update({"tg_action_comment": "Test recover deal", "approve_btn": True})
        self.client.login(username="administrator", password="test")
        response = self.client.post(
            reverse("recover_deal", kwargs={"deal_id": 1}), data
        )
        self.client.logout()
        self.assertEqual(
            302, response.status_code, msg="Recover deal does not redirect"
        )
        activity = HistoricalActivity.objects.latest_only().public().latest()
        self.assertEqual(1, activity.activity_identifier)
        # self.assertEqual('Test recover deal', activity.comment)
        self.assertEqual(HistoricalActivity.STATUS_OVERWRITTEN, activity.fk_status_id)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_does_not_exist(self):
        self.client.login(username="editor", password="test")
        response = self.client.get(reverse("recover_deal", kwargs={"deal_id": 123}))
        self.client.logout()
        self.assertEqual(404, response.status_code)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_not_deleted(self):
        self.client.login(username="editor", password="test")
        response = self.client.get(reverse("recover_deal", kwargs={"deal_id": 2}))
        self.client.logout()
        self.assertEqual(404, response.status_code)


class DealTestCase(
    ActivitiesFixtureMixin,
    InvestorsFixtureMixin,
    InvestorActivityInvolvementsFixtureMixin,
    BaseDealTestCase,
):

    act_fixtures = [{"id": 1, "activity_identifier": 1, "attributes": {}}]
    inv_fixtures = [{"id": 1, "investor_identifier": 1}]
    act_inv_fixtures = {"1": "1"}

    def test_get_forms(self):
        activity = HistoricalActivity.objects.latest_only().public().latest()
        # Overwrite target country with Mongolia
        activity.attributes.filter(name="target_country").update(value="496")
        user = get_user_model().objects.get(username="reporter")
        forms = get_forms(activity, user)
        self.assertGreater(len(forms), 0)

    def test_get_form(self):
        activity = HistoricalActivity.objects.latest_only().public().latest()
        form_tuple = (DealActionCommentForm.Meta.name, DealActionCommentForm)
        form = get_form(activity, form_tuple)
        self.assertIsInstance(form, DealActionCommentForm)
        self.assertEqual("", form.initial.get("tg_action_comment"))
