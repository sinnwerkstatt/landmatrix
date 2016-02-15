from django.test.client import Client
from django.test.testcases import TestCase
from time import time

from global_app.tests.deals_test_data import DealsTestData
from landmatrix.models.activity import Activity

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class TestDealDetailView(DealsTestData, TestCase):

    def setUp(self):
        self.create_data()
        self.activity_identifier = Activity.objects.last().activity_identifier
        self.client = Client()

    def test_call_deal_detail_view(self):
        response = self._get_url_following_redirects('/global_app/%i/' % self.activity_identifier)
        self.assertEqual(200, response.status_code)

    def test_call_deal_detail_view_with_wrong_activity_identifier(self):
        response = self._get_url_following_redirects('/global_app/%i/' % (self.activity_identifier+12345))
        self.assertEqual(404, response.status_code)

    def test_call_deal_detail_view_with_history(self):
        response = self._get_url_following_redirects('/global_app/%i_%f/' % (self.activity_identifier, time()))
        self.assertEqual(200, response.status_code)


    def _get_url_following_redirects(self, url):
        response = self.client.get(url)
        print(url)
        while response.status_code in range(300, 308):
            print(url)
            response = self.client.get(response.url)
        return response

