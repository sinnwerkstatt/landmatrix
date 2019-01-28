from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.storage.fallback import FallbackStorage
from django.core.urlresolvers import reverse
from django.http import Http404

from grid.views.investor import InvestorDetailView, RecoverInvestorView
from landmatrix.models import HistoricalInvestor
from landmatrix.tests.base import TestInvestorBase


class TestInvestorRecover(TestInvestorBase):

    fixtures = [
        'countries_and_regions',
        'users_and_groups',
        'status',
        'investors',
        'activities',
        'involvements',
    ]

    def test_editor(self):
        # Recover investor as editor
        investor = HistoricalInvestor.objects.deleted().latest()
        data = {
            # Action comment
            "tg_action_comment": "Test recover investor",
        }
        request = self.factory.post(reverse('investor_recover', kwargs={'investor_id': investor.investor_identifier}), data)
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['editor']
        response = RecoverInvestorView.as_view()(request, investor_id=investor.investor_identifier)
        self.assertEqual(response.status_code, 302, msg='Recover investor does not redirect')

        # Check if investor is public
        request = self.factory.get(reverse('investor_detail', kwargs={'investor_id': investor.investor_identifier}))
        request.user = AnonymousUser()
        try:
            response = InvestorDetailView.as_view()(request, investor_id=investor.investor_identifier)
        except Http404:
            pass
        else:
            self.fail("Investor recovered although editors shouldn't be able to recover")

    def test_admin(self):
        # Recover investor as editor
        investor = HistoricalInvestor.objects.deleted().latest()
        data = {
            # Action comment
            "tg_action_comment": "Test recover investor",
        }
        request = self.factory.post(reverse('investor_recover', kwargs={'investor_id': investor.investor_identifier}), data)
        # Mock messages framework (not available for unit tests)
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.users['administrator']
        response = RecoverInvestorView.as_view()(request, investor_id=investor.investor_identifier)
        self.assertEqual(response.status_code, 302, msg='Recover investor does not redirect')

        # Check if investor is public
        request = self.factory.get(reverse('investor_detail', kwargs={'investor_id': investor.investor_identifier}))
        request.user = AnonymousUser()
        try:
            response = InvestorDetailView.as_view()(request, investor_id=investor.investor_identifier)
        except Http404:
            self.fail("Investor still deleted after recovering")
        else:
            pass
