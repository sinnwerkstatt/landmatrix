from datetime import datetime

import pytz
from django.contrib.auth import get_user_model
from django.http import QueryDict
from django.test import RequestFactory

from apps.editor.views import *
from apps.grid.tests.views.base import BaseDealTestCase, BaseInvestorTestCase
from apps.landmatrix.models import ActivityChangeset
from apps.landmatrix.tests.mixins import ActivitiesFixtureMixin, InvestorsFixtureMixin


class FilteredQuerySetMixinTestCase(
    ActivitiesFixtureMixin, InvestorsFixtureMixin, BaseDealTestCase
):
    act_fixtures = [{"id": 10, "activity_identifier": 1}]
    inv_fixtures = [{"id": 10, "investor_identifier": 1}]

    def setUp(self):
        self.mixin = FilteredQuerySetMixin()
        super().setUp()

    def test_get_countries_with_user_country(self):
        request = RequestFactory()
        request.user = get_user_model().objects.get(username="editor-myanmar")
        request.GET = QueryDict()
        self.mixin.request = request
        countries = self.mixin._get_countries()
        self.assertEqual({"104"}, set(countries))

    def test_get_countries_with_request_country(self):
        request = RequestFactory()
        request.user = get_user_model().objects.get(username="editor")
        request.GET = QueryDict("country=104")
        self.mixin.request = request
        countries = self.mixin._get_countries()
        self.assertEqual({"104"}, set(countries))

    def test_get_countries_with_user_region(self):
        request = RequestFactory()
        request.user = get_user_model().objects.get(username="editor-asia")
        request.GET = QueryDict()
        self.mixin.request = request
        countries = self.mixin._get_countries()
        asia_countries = [str(c.id) for c in Country.objects.filter(fk_region_id=142)]
        self.assertEqual(set(asia_countries), set(countries))

    def test_get_countries_with_request_region(self):
        request = RequestFactory()
        request.user = get_user_model().objects.get(username="editor")
        request.GET = QueryDict("region=142")
        self.mixin.request = request
        countries = self.mixin._get_countries()
        asia_countries = [str(c.id) for c in Country.objects.filter(fk_region_id=142)]
        self.assertEqual(set(asia_countries), set(countries))

    def test_get_filtered_activity_queryset_with_country(self):
        request = RequestFactory()
        request.user = get_user_model().objects.get(username="editor-myanmar")
        request.GET = QueryDict()
        self.mixin.request = request
        queryset = self.mixin.get_filtered_activity_queryset()
        self.assertGreater(queryset.count(), 0)
        target_countries = set([d.target_country.id for d in queryset.all()])
        self.assertEqual({104}, target_countries)

    def test_get_filtered_activity_queryset_without_country(self):
        request = RequestFactory()
        request.user = get_user_model().objects.get(username="editor")
        request.GET = QueryDict()
        self.mixin.request = request
        queryset = self.mixin.get_filtered_activity_queryset()
        self.assertGreater(queryset.count(), 0)
        # target_countries = set([d.target_country for d in queryset.all() if d.target_country])
        # self.assertGreater(len(target_countries), 1)

    def test_get_filtered_investor_queryset_with_country(self):
        request = RequestFactory()
        request.user = get_user_model().objects.get(username="editor-myanmar")
        request.GET = QueryDict()
        self.mixin.request = request
        queryset = self.mixin.get_filtered_investor_queryset()
        self.assertGreater(queryset.count(), 0)

    def test_get_filtered_investor_queryset_without_country(self):
        request = RequestFactory()
        request.user = get_user_model().objects.get(username="editor")
        request.GET = QueryDict()
        self.mixin.request = request
        queryset = self.mixin.get_filtered_investor_queryset()
        self.assertGreater(queryset.count(), 0)


class LatestQuerySetMixinTestCase(ActivitiesFixtureMixin, BaseDealTestCase):

    act_fixtures = [
        {"id": 10, "activity_identifier": 1},
        {"id": 20, "activity_identifier": 2},
        {
            "id": 21,
            "activity_identifier": 2,
            "fk_status_id": 3,
            "history_date": datetime(2000, 1, 2, 0, 0, tzinfo=pytz.utc),
        },
        {"id": 30, "activity_identifier": 3},
        {
            "id": 31,
            "activity_identifier": 3,
            "fk_status_id": 1,
            "history_date": datetime(2000, 1, 2, 0, 0, tzinfo=pytz.utc),
        },
        {"id": 40, "activity_identifier": 4, "fk_status_id": 4},
    ]

    def setUp(self):
        self.mixin = LatestQuerySetMixin()
        request = RequestFactory()
        request.user = get_user_model().objects.get(username="editor")
        request.GET = QueryDict()
        self.mixin.request = request
        super().setUp()

    def test_get_latest_added_queryset(self):
        results = self.mixin.get_latest_added_queryset(limit=10)
        self.assertGreaterEqual(10, len(results))
        self.assertGreaterEqual(results[0].history_date, results[-1].history_date)
        statuses = [r.fk_status_id for r in results]
        self.assertEqual({2}, set(statuses))

    def test_get_latest_modified_queryset(self):
        results = self.mixin.get_latest_modified_queryset(limit=10)
        self.assertGreaterEqual(10, len(results))
        self.assertGreaterEqual(results[0].history_date, results[-1].history_date)
        statuses = [r.fk_status_id for r in results]
        self.assertEqual({3}, set(statuses))

    def test_get_latest_deleted_queryset(self):
        results = self.mixin.get_latest_deleted_queryset(limit=10)
        self.assertGreaterEqual(10, len(results))
        self.assertGreaterEqual(results[0].history_date, results[-1].history_date)
        statuses = [r.fk_status_id for r in results]
        self.assertEqual({4}, set(statuses))


class PendingChangesMixinTestCase(
    ActivitiesFixtureMixin, InvestorsFixtureMixin, BaseDealTestCase
):

    act_fixtures = [
        {"id": 10, "activity_identifier": 1, "fk_status_id": 1},
        {"id": 20, "activity_identifier": 2},
        {
            "id": 21,
            "activity_identifier": 2,
            "fk_status_id": 3,
            "history_date": datetime(2000, 1, 2, 0, 0, tzinfo=pytz.utc),
        },
        {"id": 30, "activity_identifier": 3},
        {
            "id": 31,
            "activity_identifier": 3,
            "fk_status_id": 1,
            "history_date": datetime(2000, 1, 2, 0, 0, tzinfo=pytz.utc),
        },
        {"id": 40, "activity_identifier": 4, "fk_status_id": 4},
        {"id": 50, "activity_identifier": 5, "fk_status_id": 5},
        {"id": 60, "activity_identifier": 6, "fk_status_id": 6},
        {"id": 70, "activity_identifier": 7, "fk_status_id": 2, "history_user_id": 2},
    ]

    inv_fixtures = [
        {"id": 10, "investor_identifier": 1, "fk_status_id": 1},
        {"id": 20, "investor_identifier": 2},
        {
            "id": 21,
            "investor_identifier": 2,
            "fk_status_id": 3,
            "history_date": datetime(2000, 1, 2, 0, 0, tzinfo=pytz.utc),
        },
        {"id": 30, "investor_identifier": 3},
        {
            "id": 31,
            "investor_identifier": 3,
            "fk_status_id": 1,
            "history_date": datetime(2000, 1, 2, 0, 0, tzinfo=pytz.utc),
        },
        {"id": 40, "investor_identifier": 4, "fk_status_id": 4},
        {"id": 50, "investor_identifier": 5, "fk_status_id": 5},
        {"id": 60, "investor_identifier": 6, "fk_status_id": 6},
        {"id": 70, "investor_identifier": 7, "fk_status_id": 2, "history_user_id": 2},
    ]

    def setUp(self):
        super().setUp()
        self.mixin = PendingChangesMixin()
        request = RequestFactory()
        request.user = get_user_model().objects.get(username="editor")
        request.GET = QueryDict()
        self.mixin.request = request

    def test_get_permitted_activities_for_reporter(self):
        self.mixin.request.user = get_user_model().objects.get(username="reporter")
        queryset = self.mixin.get_permitted_activities()
        self.assertEqual(0, queryset.count())

    def test_get_permitted_activities_for_editor(self):
        self.mixin.request.user = get_user_model().objects.get(username="editor")
        queryset = self.mixin.get_permitted_activities()
        self.assertGreater(queryset.count(), 0)

    def test_get_permitted_activities_for_administrator(self):
        self.mixin.request.user = get_user_model().objects.get(username="administrator")
        queryset = self.mixin.get_permitted_activities()
        self.assertGreater(queryset.count(), 0)

    def test_get_permitted_investors_for_reporter(self):
        self.mixin.request.user = get_user_model().objects.get(username="reporter")
        queryset = self.mixin.get_permitted_investors()
        self.assertEqual(0, queryset.count())

    def test_get_permitted_investors_for_editor(self):
        self.mixin.request.user = get_user_model().objects.get(username="editor")
        queryset = self.mixin.get_permitted_investors()
        self.assertGreater(queryset.count(), 0)

    def test_get_permitted_investors_for_administrator(self):
        self.mixin.request.user = get_user_model().objects.get(username="administrator")
        queryset = self.mixin.get_permitted_investors()
        self.assertGreater(queryset.count(), 0)

    def test_get_pending_adds_queryset(self):
        results = self.mixin.get_pending_adds_queryset(limit=10)
        self.assertGreater(len(results), 0)
        self.assertGreaterEqual(results[0].history_date, results[-1].history_date)
        statuses = [r.fk_status_id for r in results]
        self.assertEqual({1}, set(statuses))

    def test_get_pending_updates_queryset(self):
        results = self.mixin.get_pending_updates_queryset()
        self.assertGreater(len(results), 0)
        self.assertGreaterEqual(results[0].history_date, results[-1].history_date)
        statuses = [r.fk_status_id for r in results]
        self.assertEqual({1}, set(statuses))

    def test_get_pending_deletes_queryset(self):
        results = self.mixin.get_pending_deletes_queryset()
        self.assertGreater(len(results), 0)
        self.assertGreaterEqual(results[0].history_date, results[-1].history_date)
        statuses = [r.fk_status_id for r in results]
        self.assertEqual({6}, set(statuses))

    def test_get_feedback_queryset(self):
        ActivityFeedback.objects.create(
            fk_activity_id=10,
            fk_user_assigned_id=2,
            fk_user_created_id=1,
            comment="Test feedback",
        )
        results = self.mixin.get_feedback_queryset()
        self.assertGreater(len(results), 0)

    def test_get_rejected_queryset(self):
        ActivityChangeset.objects.create(
            fk_activity_id=50, fk_user_id=2, comment="Test changeset"
        )
        results = self.mixin.get_rejected_queryset()
        self.assertGreater(len(results), 0)
        self.assertGreaterEqual(results[0].history_date, results[-1].history_date)
        statuses = [r.fk_status_id for r in results]
        self.assertEqual({5}, set(statuses))

    def test_get_for_user_queryset(self):
        results = self.mixin.get_for_user_queryset()
        self.assertGreater(len(results), 0)
        self.assertGreaterEqual(results[0].history_date, results[-1].history_date)


class DashboardViewTestCase(ActivitiesFixtureMixin, BaseDealTestCase):

    act_fixtures = [
        {"id": 10, "activity_identifier": 1},
        {"id": 20, "activity_identifier": 2},
        {
            "id": 21,
            "activity_identifier": 2,
            "fk_status_id": 3,
            "history_date": datetime(2000, 1, 2, 0, 0, tzinfo=pytz.utc),
        },
        {"id": 30, "activity_identifier": 3},
        {
            "id": 31,
            "activity_identifier": 3,
            "fk_status_id": 1,
            "history_date": datetime(2000, 1, 2, 0, 0, tzinfo=pytz.utc),
        },
        {"id": 40, "activity_identifier": 4, "fk_status_id": 4},
    ]

    def test(self):
        ActivityFeedback.objects.create(
            fk_activity_id=10,
            fk_user_assigned_id=2,
            fk_user_created_id=1,
            comment="Test feedback",
        )
        self.client.login(username="editor", password="test")
        response = self.client.get(reverse("editor"))
        self.client.logout()
        self.assertEqual(200, response.status_code)
        self.assertGreater(len(response.context.get("latest_added")), 0)
        self.assertGreater(len(response.context.get("latest_modified")), 0)
        self.assertGreater(len(response.context.get("latest_deleted")), 0)
        self.assertGreater(len(response.context.get("manage")), 0)
        self.assertGreater(len(response.context.get("feedbacks", {}).get("feeds")), 0)


class ManageItemsTestCaseMixin(ActivitiesFixtureMixin):

    act_fixtures = [
        {"id": 10, "activity_identifier": 1, "fk_status_id": 1},
        {"id": 20, "activity_identifier": 2},
        {
            "id": 21,
            "activity_identifier": 2,
            "fk_status_id": 3,
            "history_date": datetime(2000, 1, 2, 0, 0, tzinfo=pytz.utc),
        },
        {"id": 30, "activity_identifier": 3},
        {
            "id": 31,
            "activity_identifier": 3,
            "fk_status_id": 1,
            "history_date": datetime(2000, 1, 2, 0, 0, tzinfo=pytz.utc),
        },
        {"id": 40, "activity_identifier": 4, "fk_status_id": 4},
        {"id": 50, "activity_identifier": 5, "fk_status_id": 5},
        {"id": 60, "activity_identifier": 6, "fk_status_id": 6},
        {"id": 70, "activity_identifier": 7, "fk_status_id": 2, "history_user_id": 2},
    ]

    url = None

    def test(self):
        self.client.login(username="editor", password="test")
        response = self.client.get(self.url)
        self.client.logout()
        self.assertEqual(200, response.status_code)
        self.assertGreater(len(response.context.get("items")), 0)


class LogAddedViewTestCase(ManageItemsTestCaseMixin, BaseDealTestCase):

    url = reverse("log_added")


class LogModifiedViewTestCase(ManageItemsTestCaseMixin, BaseDealTestCase):

    url = reverse("log_modified")


class LogDeletedViewTestCase(ManageItemsTestCaseMixin, BaseDealTestCase):

    url = reverse("log_deleted")


class ManageRootViewTestCase(BaseDealTestCase):

    fixtures = ["countries_and_regions", "users_and_groups", "status"]

    def test_with_reporter(self):
        self.client.login(username="reporter", password="test")
        response = self.client.get(reverse("manage"))
        self.client.logout()
        self.assertEqual(302, response.status_code)
        self.assertEqual(reverse("manage_for_user"), response.url)

    def test_with_editor(self):
        self.client.login(username="editor", password="test")
        response = self.client.get(reverse("manage"))
        self.client.logout()
        self.assertEqual(302, response.status_code)
        self.assertEqual(reverse("manage_feedback"), response.url)


class ManageFeedbackViewTestCase(ManageItemsTestCaseMixin, BaseDealTestCase):
    def setUp(self):
        super().setUp()
        ActivityFeedback.objects.create(
            fk_activity_id=10,
            fk_user_assigned_id=2,
            fk_user_created_id=1,
            comment="Test feedback",
        )

    url = reverse("manage_feedback")


class ManageRejectedViewTestCase(ManageItemsTestCaseMixin, BaseDealTestCase):

    url = reverse("manage_rejected")

    def setUp(self):
        super().setUp()
        ActivityChangeset.objects.create(
            fk_activity_id=50, fk_user_id=2, comment="Test changeset"
        )


class ManageAddsViewTestCase(ManageItemsTestCaseMixin, BaseDealTestCase):

    url = reverse("manage_pending_adds")


class ManageUpdatesViewTestCase(ManageItemsTestCaseMixin, BaseDealTestCase):

    url = reverse("manage_pending_updates")


class ManageDeletesViewTestCase(ManageItemsTestCaseMixin, BaseDealTestCase):

    url = reverse("manage_pending_deletes")


class ManageForUserViewTestCase(ManageItemsTestCaseMixin, BaseDealTestCase):

    url = reverse("manage_for_user")


class ManageItemTestCaseMixin:

    fixtures = ["countries_and_regions", "users_and_groups", "status"]

    url = None
    object_class = HistoricalActivity
    object_id = None
    object_status = None
    success_url = reverse("manage_feedback")

    def assert_object_updated(self):
        object = self.object_class.objects.get(id=self.object_id)
        self.assertEqual(self.object_status, object.fk_status_id)

    def test_get(self):
        self.client.login(username="administrator", password="test")
        response = self.client.get(self.url)
        self.client.logout()
        self.assertEqual(200, response.status_code)

    def test_post(self):
        data = {"tg_action_comment": "Test"}
        self.client.login(username="administrator", password="test")
        response = self.client.post(self.url, data=data)
        self.client.logout()
        self.assertEqual(302, response.status_code)
        self.assertEqual(reverse("manage_feedback"), response.url)
        self.assert_object_updated()


class ApproveActivityChangeViewTestCase(
    ActivitiesFixtureMixin, ManageItemTestCaseMixin, BaseDealTestCase
):

    act_fixtures = [
        {"id": 10, "activity_identifier": 1, "fk_status_id": 1, "attributes": {}}
    ]

    url = reverse("manage_approve_change_deal", kwargs={"id": 10})
    object_id = 10
    object_status = 2


class RejectActivityChangeViewTestCase(
    ActivitiesFixtureMixin, ManageItemTestCaseMixin, BaseDealTestCase
):

    act_fixtures = [
        {"id": 10, "activity_identifier": 1, "fk_status_id": 1, "attributes": {}}
    ]

    url = reverse("manage_reject_change_deal", kwargs={"id": 10})
    object_id = 10
    object_status = 5


class ApproveActivityDeleteViewTestCase(
    ActivitiesFixtureMixin, ManageItemTestCaseMixin, BaseDealTestCase
):

    act_fixtures = [
        {
            "id": 10,
            "activity_identifier": 1,
            "fk_status_id": 6,
            "history_user_id": 2,
            "attributes": {},
        }
    ]

    url = reverse("manage_approve_delete_deal", kwargs={"id": 10})
    object_id = 10
    object_status = 4


class RejectActivityDeleteViewTestCase(
    ActivitiesFixtureMixin, ManageItemTestCaseMixin, BaseDealTestCase
):

    act_fixtures = [
        {"id": 10, "activity_identifier": 1, "fk_status_id": 6, "attributes": {}}
    ]

    url = reverse("manage_reject_delete_deal", kwargs={"id": 10})
    object_id = 10
    object_status = 5


class ApproveInvestorChangeViewTestCase(
    InvestorsFixtureMixin, ManageItemTestCaseMixin, BaseInvestorTestCase
):

    inv_fixtures = [{"id": 10, "investor_identifier": 1, "fk_status_id": 1}]

    url = reverse("manage_approve_change_investor", kwargs={"id": 10})
    object_class = HistoricalInvestor
    object_id = 10
    object_status = 2


class RejectInvestorChangeViewTestCase(
    InvestorsFixtureMixin, ManageItemTestCaseMixin, BaseInvestorTestCase
):

    inv_fixtures = [{"id": 10, "investor_identifier": 1, "fk_status_id": 1}]

    url = reverse("manage_reject_change_investor", kwargs={"id": 10})
    object_class = HistoricalInvestor
    object_id = 10
    object_status = 5


class ApproveInvestorDeleteViewTestCase(
    InvestorsFixtureMixin, ManageItemTestCaseMixin, BaseInvestorTestCase
):

    inv_fixtures = [{"id": 10, "investor_identifier": 1, "fk_status_id": 6}]

    url = reverse("manage_approve_delete_investor", kwargs={"id": 10})
    object_class = HistoricalInvestor
    object_id = 10
    object_status = 4


class RejectInvestorDeleteViewTestCase(
    InvestorsFixtureMixin, ManageItemTestCaseMixin, BaseInvestorTestCase
):

    inv_fixtures = [{"id": 10, "investor_identifier": 1, "fk_status_id": 6}]

    url = reverse("manage_reject_delete_investor", kwargs={"id": 10})
    object_class = HistoricalInvestor
    object_id = 10
    object_status = 5
