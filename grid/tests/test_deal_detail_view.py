from django.test.client import Client
from django.test.testcases import TestCase
from time import time, mktime

from grid.tests.deals_test_data import DealsTestData
from grid.tests.with_client_mixin import WithClientMixin
from landmatrix.models.activity import Activity
from landmatrix.models.activity_attribute_group import ActivityAttributeGroup
from landmatrix.models.deal_history import DealHistoryItem

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class TestDealDetailView(DealsTestData, WithClientMixin, TestCase):

    INTENDED_SIZE = {'old': 314159265, 'new': 562951413}
    CONTRACT_SIZE = {'old': 271828182, 'new': 281828172}
    PRODUCTION_SIZE = {'old': 141421356, 'new': 653124141}

    def setUp(self):
        self.create_data({
            'intended_size': self.INTENDED_SIZE['old'],
            'contract_size': self.CONTRACT_SIZE['old'],
            'production_size': self.PRODUCTION_SIZE['old'],
        })
        self.activity_identifier = Activity.objects.last().activity_identifier
        DealHistoryItem.use_rounded_dates = False
        super(WithClientMixin, self).setUp()

    def test_call_deal_detail_view(self):
        response = self._get_url_following_redirects('/grid/%i/' % self.activity_identifier)
        self.assertEqual(200, response.status_code)

    def test_call_deal_detail_view_with_wrong_activity_identifier(self):
        response = self._get_url_following_redirects('/grid/%i/' % (self.activity_identifier+12345))
        self.assertEqual(404, response.status_code)

    def test_deal_detail_view_content(self):
        response = self._get_url_following_redirects('/grid/%i/' % self.activity_identifier)

        content = response.content.decode('utf-8')

        self.skipTest('operational stakeholder name not displayed in current template')

        self.assertIn(self.OS_NAME, content)
        self.assertIn(str(self.INTENDED_SIZE['old']), grep_line(content, 'intended_size')[0])
        self.assertIn(str(self.CONTRACT_SIZE['old']), grep_line(content, 'contract_size')[0])
        self.assertIn(str(self.PRODUCTION_SIZE['old']), grep_line(content, 'production_size')[0])

    def test_call_deal_detail_view_with_history(self):
        response = self._get_url_following_redirects('/grid/%i_%f/' % (self.activity_identifier, time()))
        self.assertEqual(200, response.status_code)

    def test_deal_detail_view_with_history_content(self):
        response = self._get_url_following_redirects('/grid/%i_%f/' % (self.activity_identifier, time()))

        content = response.content.decode('utf-8')

        self.skipTest('operational stakeholder name not displayed in current template')

        self.assertIn(self.OS_NAME, content)
        self.assertIn(str(self.INTENDED_SIZE['old']), grep_line(content, 'intended_size')[0])
        self.assertIn(str(self.CONTRACT_SIZE['old']), grep_line(content, 'contract_size')[0])
        self.assertIn(str(self.PRODUCTION_SIZE['old']), grep_line(content, 'production_size')[0])

    def test_deal_detail_view_with_history_changed(self):
        self._change_activity_attributes()

        response = self._get_url_following_redirects('/grid/%i_%f/' % (self.activity_identifier, time()))

        content = response.content.decode('utf-8')
        self.assertIn(str(self.INTENDED_SIZE['new']), grep_line(content, 'intended_size')[0])
        self.assertIn(str(self.CONTRACT_SIZE['new']), grep_line(content, 'contract_size')[0])
        self.assertIn(str(self.PRODUCTION_SIZE['new']), grep_line(content, 'production_size')[0])
        self.assertNotIn(str(self.INTENDED_SIZE['old']), grep_line(content, 'intended_size')[0])
        self.assertNotIn(str(self.CONTRACT_SIZE['old']), grep_line(content, 'contract_size')[0])
        self.assertNotIn(str(self.PRODUCTION_SIZE['old']), grep_line(content, 'production_size')[0])

    def test_deal_detail_view_with_history_old_version(self):
        attributes = self._change_activity_attributes()
        new_timestamp = attributes.history.first().history_date.timestamp()
        old_timestamp = attributes.history.last().history_date.timestamp()
        self.assertLess(old_timestamp, new_timestamp)
        hopefully_existing_timestamp = (new_timestamp+old_timestamp)/2.

        response = self._get_url_following_redirects('/grid/%i_%f/' % (self.activity_identifier, hopefully_existing_timestamp))

        content = response.content.decode('utf-8')
        self.assertIn(str(self.INTENDED_SIZE['old']), grep_line(content, 'intended_size')[0])
        self.assertIn(str(self.CONTRACT_SIZE['old']), grep_line(content, 'contract_size')[0])
        self.assertIn(str(self.PRODUCTION_SIZE['old']), grep_line(content, 'production_size')[0])

    def _change_activity_attributes(self):
        activity = Activity.objects.last()
        attributes = ActivityAttributeGroup.objects.filter(fk_activity=activity). \
            filter(attributes__contains=['intended_size']).first()
        attributes.attributes.update({
            'intended_size': self.INTENDED_SIZE['new'],
            'contract_size': self.CONTRACT_SIZE['new'],
            'production_size': self.PRODUCTION_SIZE['new'],
        })
        attributes.save()
        return attributes


def grep_line(string, search):
    return [item for item in string.split("\n") if search in item]