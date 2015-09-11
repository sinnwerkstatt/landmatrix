__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from api.query_sets.implementation_status_query_set import ImplementationStatusQuerySet
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
    DEAL_SCOPE = 'transnational'
    RELEVANT_ATTRIBUTES = {
        'pi_deal_size': '12345', 'deal_scope': 'transnational', 'pi_implementation_status': 'In operation (production)'
    }
    NUM_RELEVANT_DEALS = 2

    def setUp(self):
        self.RELEVANT_ATTRIBUTES['deal_scope'] = self.DEAL_SCOPE

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
        result = self.get_content('implementation_status')
        self.assertEqual(len(ImplementationStatusQuerySet.IMPLEMENTATION_STATUS)+1, len(result))
        relevant_line = list(filter(lambda line: line['name'] == self.RELEVANT_ATTRIBUTES['pi_implementation_status'], result))
        #if self.__class__.__name__ == 'TestImplementationStatusTransnational': print(result, relevant_line)
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
    DEAL_SCOPE = 'transnational'
    NUM_RELEVANT_DEALS = 1


class TestImplementationStatusDomestic(TestImplementationStatus):

    POSTFIX = '.json?deal_scope=domestic'
    DEAL_SCOPE = 'domestic'
    NUM_RELEVANT_DEALS = 1

class TestImplementationStatusDomesticDataSource(TestImplementationStatus):

    POSTFIX = '.json?deal_scope=transnational&deal_scope=domestic&data_source_type=1'
    EXPECTED_DEAL_COUNT = 0
    EXPECTED_SIZE = 0
    RELEVANT_ATTRIBUTES = {
        'pi_deal_size': '12345', 'deal_scope': 'transnational', 'pi_implementation_status': 'In operation (production)', 'type': 'Media report'
    }

    def test_with_data(self):
        self._generate_negotiation_status_data(123, self.RELEVANT_ATTRIBUTES)
        self.test_empty()

    def test_with_both_transnational_and_domestic(self):
        attributes = self.RELEVANT_ATTRIBUTES
        for index, scope in enumerate(['transnational', 'domestic']):
            attributes['deal_scope'] = scope
            self._generate_negotiation_status_data(123+index, attributes)
        self.test_empty()


class TestImplementationStatusDomesticDataSourceNot(TestImplementationStatus):

    POSTFIX = '.json?deal_scope=transnational&deal_scope=domestic&data_source_type=1'
    EXPECTED_DEAL_COUNT = 2
    RELEVANT_ATTRIBUTES = {
        'pi_deal_size': '12345', 'deal_scope': 'transnational', 'pi_implementation_status': 'In operation (production)', 'type': 'NOT Media report'
    }
