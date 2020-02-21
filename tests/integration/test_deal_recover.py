from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.storage.fallback import FallbackStorage
from django.http import Http404
from django.test import override_settings, tag
from django.urls import reverse

from apps.grid.tests.views.base import BaseDealTestCase
from apps.grid.views.deal import DealDetailView, DealRecoverView
from apps.landmatrix.models import HistoricalActivity
from apps.landmatrix.tests.mixins import (
    ActivitiesFixtureMixin,
    InvestorsFixtureMixin,
    InvestorActivityInvolvementsFixtureMixin,
)


@tag("integration")
class TestDealRecover(
    ActivitiesFixtureMixin,
    InvestorsFixtureMixin,
    InvestorActivityInvolvementsFixtureMixin,
    BaseDealTestCase,
):

    act_fixtures = [
        {"id": 1, "activity_identifier": 1, "fk_status_id": 4, "attributes": {}}
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
    ]
    act_inv_fixtures = {"1": "1"}

    @override_settings(
        ELASTICSEARCH_INDEX_NAME="landmatrix_test", CELERY_ALWAYS_EAGER=True
    )
    def test_editor(self):
        # Recover deal as editor
        activity = HistoricalActivity.objects.latest_only().deleted().latest()
        data = {
            # Action comment
            "tg_action_comment": "Test recover deal"
        }
        request = self.factory.post(
            reverse("recover_deal", kwargs={"deal_id": activity.activity_identifier}),
            data,
        )
        # Mock messages framework (not available for unit tests)
        setattr(request, "session", {})
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        request.user = self.users["editor"]
        response = DealRecoverView.as_view()(
            request, deal_id=activity.activity_identifier
        )
        self.assertEqual(
            response.status_code, 302, msg="Recover deal does not redirect"
        )

        # Check if deal is public
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
            self.fail("Deal recovered although editors shouldn't be able to recover")

    @override_settings(
        ELASTICSEARCH_INDEX_NAME="landmatrix_test", CELERY_ALWAYS_EAGER=True
    )
    def test_admin(self):
        # Recover deal as editor
        activity = HistoricalActivity.objects.latest_only().deleted().latest()
        data = {
            # Action comment
            "tg_action_comment": "Test recover deal"
        }
        request = self.factory.post(
            reverse("recover_deal", kwargs={"deal_id": activity.activity_identifier}),
            data,
        )
        # Mock messages framework (not available for unit tests)
        setattr(request, "session", {})
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        request.user = self.users["administrator"]
        response = DealRecoverView.as_view()(
            request, deal_id=activity.activity_identifier
        )
        self.assertEqual(
            response.status_code, 302, msg="Recover deal does not redirect"
        )

        # Check if deal is public
        request = self.factory.get(
            reverse("deal_detail", kwargs={"deal_id": activity.activity_identifier})
        )
        request.user = AnonymousUser()
        try:
            response = DealDetailView.as_view()(
                request, deal_id=activity.activity_identifier
            )
        except Http404:
            self.fail("Deal still deleted after recovering")
        else:
            pass
