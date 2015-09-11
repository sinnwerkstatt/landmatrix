from landmatrix.models.activity_attribute_group import ActivityAttributeGroup

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from api.query_sets.intention_query_set import IntentionQuerySet
from .api_test_functions import ApiTestFunctions
from api.tests.deals_test_data import DealsTestData


"""
/en/api/transnational_deals.json?negotiation_status=concluded&deal_scope=transnational
/en/api/transnational_deals.json?negotiation_status=intended&deal_scope=transnational
/en/api/transnational_deals.json?negotiation_status=concluded&negotiation_status=intended&deal_scope=transnational
/en/api/transnational_deals.json?negotiation_status=failed&deal_scope=transnational
/en/api/transnational_deals.json?negotiation_status=concluded&deal_scope=transnational&data_source_type=1
/en/api/transnational_deals.json?negotiation_status=intended&deal_scope=transnational&data_source_type=1
/en/api/transnational_deals.json?negotiation_status=concluded&negotiation_status=intended&deal_scope=transnational&data_source_type=1
/en/api/transnational_deals.json?negotiation_status=failed&deal_scope=transnational&data_source_type=1
"""


class TestTransnationalDeals(ApiTestFunctions, DealsTestData):

    PREFIX = '/en/api/'
    POSTFIX = '.json?negotiation_status=concluded&deal_scope=transnational'
    DEAL_SCOPE = 'transnational'
    RELEVANT_ATTRIBUTES = {
        'pi_deal_size': '12345', 'deal_scope': 'transnational', 'intention': 'Forestry', 'pi_negotiation_status': 'Concluded (Contract signed)'
    }
    NUM_RELEVANT_DEALS = 1

    def setUp(self):
        self.RELEVANT_ATTRIBUTES['deal_scope'] = self.DEAL_SCOPE

    def tearDown(self):
        IntentionQuerySet.DEBUG = False

    def test_empty(self):
        result = self.get_content('transnational_deals')
        self.assertEqual(self.num_results(), len(result))
        for record in result:
            self.assertEqual(0, record['deals'])
            self.assertEqual(0, record['hectares'])

    def test_with_data(self):
        self._generate_negotiation_status_data(123, self.RELEVANT_ATTRIBUTES)
        IntentionQuerySet.DEBUG = False
        result = self.get_content('transnational_deals')
        if self.__class__.__name__ == 'TestIntentionAgriculture...':
            print(self.RELEVANT_ATTRIBUTES, ActivityAttributeGroup.objects.all(), result)

        self.assertEqual(self.num_results(), len(result))

        if self.NUM_RELEVANT_DEALS == 0: return

        relevant_line = list(filter(lambda line: line['name'] == self.RELEVANT_ATTRIBUTES['intention'], result))

        self.assertEqual(1 if self.NUM_RELEVANT_DEALS > 0 else 0, relevant_line[0]['deals'])
        self.assertEqual(self.RELEVANT_ATTRIBUTES['intention'], relevant_line[0]['name'])
        self.assertEqual(float(self.RELEVANT_ATTRIBUTES['pi_deal_size']) if self.NUM_RELEVANT_DEALS > 0 else 0, relevant_line[0]['hectares'])

    def num_results(self):
        return len(IntentionQuerySet.INTENTIONS)+2

    def test_with_both_transnational_and_domestic(self):
        attributes = self.RELEVANT_ATTRIBUTES
        for index, scope in enumerate(['transnational', 'domestic']):
            attributes['deal_scope'] = scope
            self._generate_negotiation_status_data(123+index, attributes)

        result = self.get_content('transnational_deals')
        self.assertEqual(self.num_results(), len(result))

        if self.NUM_RELEVANT_DEALS == 0: return

        relevant_line = list(filter(lambda line: line['name'] == self.RELEVANT_ATTRIBUTES['intention'], result))
        self.assertEqual(self.NUM_RELEVANT_DEALS, relevant_line[0]['deals'])
        self.assertEqual(self.RELEVANT_ATTRIBUTES['intention'], relevant_line[0]['name'])
        self.assertEqual(self.NUM_RELEVANT_DEALS*float(self.RELEVANT_ATTRIBUTES['pi_deal_size']), relevant_line[0]['hectares'])

