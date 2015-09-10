from api.query_sets.implementation_status_query_set import ImplementationStatusQuerySet
from api.views import ImplementationStatusJSONView

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from .api_test_functions import ApiTestFunctions
from api.tests.deals_test_data import DealsTestData


"""
/en/api/implementation_status.json?deal_scope=domestic
/en/api/implementation_status.json?deal_scope=transnational
/en/api/implementation_status.json?deal_scope=transnational&deal_scope=domestic
/en/api/implementation_status.json?deal_scope=domestic&data_source_type=1
/en/api/implementation_status.json?deal_scope=transnational&data_source_type=1
/en/api/implementation_status.json?deal_scope=transnational&deal_scope=domestic&data_source_type=1
"""
class TestImplementationStatus(ApiTestFunctions, DealsTestData):

    PREFIX = '/en/api/'
    POSTFIX = '.json?deal_scope=transnational&deal_scope=domestic'
    RELEVANT_ATTRIBUTES = {
        'pi_deal_size': '12345', 'deal_scope': 'transnational', 'pi_implementation_status': 'In operation (production)'
    }
    NUM_RELEVANT_DEALS = 2

    def tearDown(self):
        ImplementationStatusQuerySet.DEBUG = False

    def test_empty(self):
        result = self.get_content('implementation_status')
        self.assertEqual(len(ImplementationStatusQuerySet.IMPLEMENTATION_STATUS)+1, len(result))
        for record in result:
            self.assertEqual(0, record['deals'])
            self.assertEqual(0, record['hectares'])

    def test_with_data(self):
        self._generate_negotiation_status_data(123, self.RELEVANT_ATTRIBUTES)
        if self.__class__.__name__ == 'TestImplementationStatusTransnational':
            ImplementationStatusQuerySet.DEBUG = True
        result = self.get_content('implementation_status')
        self.assertEqual(len(ImplementationStatusQuerySet.IMPLEMENTATION_STATUS)+1, len(result))
        relevant_line = list(filter(lambda line: line['name'] == self.RELEVANT_ATTRIBUTES['pi_implementation_status'], result))
        if self.__class__.__name__ == 'TestImplementationStatusTransnational': print(result, relevant_line)
        self.assertEqual(1, relevant_line[0]['deals'])
        self.assertEqual(self.RELEVANT_ATTRIBUTES['pi_implementation_status'], relevant_line[0]['name'])
        self.assertEqual(float(self.RELEVANT_ATTRIBUTES['pi_deal_size']), relevant_line[0]['hectares'])

    def test_with_both_transnational_and_domestic(self):
        attributes = self.RELEVANT_ATTRIBUTES
        for index, scope in enumerate(['transnational', 'domestic']):
            attributes['deal_scope'] = scope
            self._generate_negotiation_status_data(123+index, attributes)

        result = self.get_content('implementation_status')
        self.assertEqual(len(ImplementationStatusQuerySet.IMPLEMENTATION_STATUS)+1, len(result))
        relevant_line = list(filter(lambda line: line['name'] == self.RELEVANT_ATTRIBUTES['pi_implementation_status'], result))
        self.assertEqual(self.NUM_RELEVANT_DEALS, relevant_line[0]['deals'])
        self.assertEqual(self.RELEVANT_ATTRIBUTES['pi_implementation_status'], relevant_line[0]['name'])
        self.assertEqual(self.NUM_RELEVANT_DEALS*float(self.RELEVANT_ATTRIBUTES['pi_deal_size']), relevant_line[0]['hectares'])


class TestImplementationStatusTransnational(TestImplementationStatus):

    POSTFIX = '.json?deal_scope=transnational'
    NUM_RELEVANT_DEALS = 1

class TestImplementationStatusDomestic(TestImplementationStatus):

    POSTFIX = '.json?deal_scope=domestic'
    RELEVANT_ATTRIBUTES = {
        'pi_deal_size': '12345', 'deal_scope': 'domestic', 'pi_implementation_status': 'In operation (production)'
    }
    NUM_RELEVANT_DEALS = 1
