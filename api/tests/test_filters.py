import json

from django.test.testcases import TestCase

from api.query_sets.fake_query_set import FakeQuerySet
from global_app.views.view_aux_functions import FILTER_VAR_ACT, FILTER_VAR_INV

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class TestFilters(TestCase):

    FILTER_VALUES = {
        "target_country": 10, "location": 'x', "intention": 10, "intended_size": 1, "contract_size": 1,
        "production_size": 1, "negotiation_status": 10, "implementation_status": 10, "crops": 1, "nature": 1,
        "contract_farming": 10, "url": 'x', "type": 1, "company": 'x', "investor_name": 'x', "country": 1,
    }

    def setUp(self):
        FakeQuerySet.DEBUG = False

    def tearDown(self):
        FakeQuerySet.DEBUG = False

    def test_all_filters_single(self):
        for filter in FILTER_VAR_ACT+FILTER_VAR_INV:
            print(filter)
            self._get_content(self._fake_url_params(filter))

    def _fake_url_params(self, filter):
        return '/api/agricultural-produce.json?negotiation_status=concluded&deal_scope=transnational'\
               '&filtered=true&limit=&order_by=deal_id' \
               '&prefix=conditions_empty' \
               '&conditions_empty-TOTAL_FORMS=1&conditions_empty-INITIAL_FORMS=2' \
               '&conditions_empty-MIN_NUM_FORMS=&conditions_empty-MAX_NUM_FORMS=' \
               '&variable=&operator=&value=&hidden_value=' \
               '&conditions_empty-0-variable=' + filter + \
               '&conditions_empty-0-operator=is&conditions_empty-0-value=' + str(self.FILTER_VALUES[filter]) + \
               '&conditions_empty-0-hidden_value='

    def _get_content(self, resource):
        url, response = self._get_url_following_redirects(resource)
        self.assertEqual(200, response.status_code)
        try:
            return json.loads(response.content.decode('utf-8'))
        except ValueError as e:
            print(response.content.decode('utf-8'))
            raise e

    def _get_url_following_redirects(self, url):
        response = self.client.get(url)
        while response.status_code in range(300, 308):
            url = response.url
            response = self.client.get(url)
        return url, response