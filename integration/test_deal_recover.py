from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.storage.fallback import FallbackStorage
from django.urls import reverse
from django.http import Http404
from django.test import tag

from grid.views.deal import DealDetailView, DealRecoverView
from landmatrix.models import HistoricalActivity

from grid.tests.views.base import BaseDealTestCase


@tag('integration')
class TestDealRecover(BaseDealTestCase):

    fixtures = [
        'countries_and_regions',
        'users_and_groups',
        'status',
        'investors',
        'activities',
        'activity_involvements',
        'venture_involvements',
    ]

    def test_editor(self):
        # Recover deal as editor
        activity = HistoricalActivity.objects.latest_only().deleted().latest()
        data = {
            # Action comment
            "tg_action_comment": "Test recover deal",
        }
        request = self.factory.post(reverse('recover_deal', kwargs={'deal_id': activity.activity_identifier}), data)
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['editor']
        response = DealRecoverView.as_view()(request, deal_id=activity.activity_identifier)
        self.assertEqual(response.status_code, 302, msg='Recover deal does not redirect')

        # Check if deal is public
        request = self.factory.get(reverse('deal_detail', kwargs={'deal_id': activity.activity_identifier}))
        request.user = AnonymousUser()
        try:
            response = DealDetailView.as_view()(request, deal_id=activity.activity_identifier)
        except Http404:
            pass
        else:
            self.fail("Deal recovered although editors shouldn't be able to recover")

    def test_admin(self):
        # Recover deal as editor
        activity = HistoricalActivity.objects.latest_only().deleted().latest()
        data = {
            # Action comment
            "tg_action_comment": "Test recover deal",
        }
        request = self.factory.post(reverse('recover_deal', kwargs={'deal_id': activity.activity_identifier}), data)
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['administrator']
        response = DealRecoverView.as_view()(request, deal_id=activity.activity_identifier)
        self.assertEqual(response.status_code, 302, msg='Recover deal does not redirect')

        # Check if deal is public
        request = self.factory.get(reverse('deal_detail', kwargs={'deal_id': activity.activity_identifier}))
        request.user = AnonymousUser()
        try:
            response = DealDetailView.as_view()(request, deal_id=activity.activity_identifier)
        except Http404:
            self.fail("Deal still deleted after recovering")
        else:
            pass
