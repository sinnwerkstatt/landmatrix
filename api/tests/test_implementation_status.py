from api.query_sets.implementation_status_query_set import ImplementationStatusQuerySet
from api.views import ImplementationStatusJSONView

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from .api_test_functions import ApiTestFunctions
from api.tests.deals_test_data import DealsTestData


class TestImplementationStatus(ApiTestFunctions, DealsTestData):

    PREFIX = '/en/api/'
    POSTFIX = '.json?deal_scope=transnational&deal_scope=domestic'
    RELEVANT_ATTRIBUTES = {
        'pi_deal_size': '12345', 'deal_scope': 'transnational', 'pi_implementation_status': 'In operation (production)'
    }

    def tearDown(self):
        ImplementationStatusQuerySet.DEBUG = False

    def test_empty(self):
        result = self.get_content('implementation_status')
        for record in result:
            self.assertEqual(0, record['deals'])
            self.assertEqual(0, record['hectares'])

    def test_with_data(self):
        self._generate_negotiation_status_data(123, self.RELEVANT_ATTRIBUTES)
        result = self.get_content('implementation_status')
        self.assertEqual(len(ImplementationStatusJSONView.IMPLEMENTATION_STATUS)+1, len(result))
        relevant_line = list(filter(lambda line: line['name'] == self.RELEVANT_ATTRIBUTES['pi_implementation_status'], result))
        print(relevant_line)
        self.assertEqual(1, relevant_line[0]['deals'])
        self.assertEqual(self.RELEVANT_ATTRIBUTES['pi_implementation_status'], relevant_line[0]['name'])
        self.assertEqual(float(self.RELEVANT_ATTRIBUTES['pi_deal_size']), relevant_line[0]['hectares'])
