from api.query_sets.hectares_query_set import HectaresQuerySet

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from .api_test_functions import ApiTestFunctions
from api.tests.deals_test_data import DealsTestData

"""
/en/api/hectares.json?negotiation_status=concluded&deal_scope=transnational
/en/api/hectares.json?negotiation_status=concluded&deal_scope=domestic
/en/api/hectares.json?negotiation_status=concluded&deal_scope=transnational&deal_scope=domestic
/en/api/hectares.json?negotiation_status=intended&deal_scope=domestic
/en/api/hectares.json?negotiation_status=intended&deal_scope=transnational
/en/api/hectares.json?negotiation_status=intended&deal_scope=transnational&deal_scope=domestic
/en/api/hectares.json?negotiation_status=concluded&negotiation_status=intended&deal_scope=domestic
/en/api/hectares.json?negotiation_status=concluded&negotiation_status=intended&deal_scope=transnational
/en/api/hectares.json?negotiation_status=concluded&negotiation_status=intended&deal_scope=transnational&deal_scope=domestic
/en/api/hectares.json?negotiation_status=failed&deal_scope=domestic
/en/api/hectares.json?negotiation_status=failed&deal_scope=transnational
/en/api/hectares.json?negotiation_status=failed&deal_scope=transnational&deal_scope=domestic
/en/api/hectares.json?negotiation_status=intended&deal_scope=domestic&data_source_type=1
/en/api/hectares.json?negotiation_status=intended&deal_scope=transnational&data_source_type=1
/en/api/hectares.json?negotiation_status=intended&deal_scope=transnational&deal_scope=domestic&data_source_type=1
/en/api/hectares.json?negotiation_status=concluded&deal_scope=domestic&data_source_type=1
/en/api/hectares.json?negotiation_status=concluded&deal_scope=transnational&data_source_type=1
/en/api/hectares.json?negotiation_status=concluded&deal_scope=transnational&deal_scope=domestic&data_source_type=1
/en/api/hectares.json?negotiation_status=concluded&negotiation_status=intended&deal_scope=domestic&data_source_type=1
/en/api/hectares.json?negotiation_status=concluded&negotiation_status=intended&deal_scope=transnational&data_source_type=1
/en/api/hectares.json?negotiation_status=concluded&negotiation_status=intended&deal_scope=transnational&deal_scope=domestic&data_source_type=1
/en/api/hectares.json?negotiation_status=failed&deal_scope=domestic&data_source_type=1
/en/api/hectares.json?negotiation_status=failed&deal_scope=transnational&data_source_type=1
/en/api/hectares.json?negotiation_status=failed&deal_scope=transnational&deal_scope=domestic&data_source_type=1
"""


class TestHectares(ApiTestFunctions, DealsTestData):

    POSTFIX = '.json?negotiation_status=concluded&deal_scope=transnational'
    DEAL_SCOPE = 'transnational'
    NEGOTIATION_STATUS = 'concluded (oral agreement)'
    RELEVANT_ATTRIBUTES = {}
    NUM_RELEVANT_COMBINATIONS = 1

    def test_empty(self):
        result = self.get_content('hectares')
        self.assertEqual(2, len(result))
        self.assertEqual(0, result['deals'])
        self.assertEqual(None, result['hectares'])

    def test_with_data(self):
        self._generate_enough_deals()
        result = self.get_content('hectares')
        self.assertEqual(self.NUM_RELEVANT_COMBINATIONS*self.NUM_DEALS, result['deals'])
        self.assertEqual(self.NUM_RELEVANT_COMBINATIONS*self.NUM_DEALS*(self.NUM_DEALS+1), result['hectares'] or 0)

    NUM_DEALS = 2
    def _generate_enough_deals(self):
        self._generate_countries(0)
        for i in range(0, self.NUM_DEALS):
            for scope in ['transnational', 'domestic']:
                for status in ['concluded (oral agreement)', "intended (under negotiation)", "failed (contract canceled)"]:
                    attributes = {'pi_deal_size': 2 << i, 'deal_scope': scope, 'pi_negotiation_status': status}
                    attributes.update(self.RELEVANT_ATTRIBUTES)
                    self._generate_deal(self.investor_country, self.deal_country, attributes)


class TestHectaresIntended(TestHectares):
    NEGOTIATION_STATUS = "intended (under negotiation)"
    POSTFIX = '.json?negotiation_status=intended&deal_scope=transnational'


class TestHectaresConcludedIntended1(TestHectares):
    NEGOTIATION_STATUS = 'concluded (oral agreement)'
    POSTFIX = '.json?negotiation_status=concluded&negotiation_status=intended&deal_scope=transnational'
    NUM_RELEVANT_COMBINATIONS = 2


class TestHectaresConcludedIntended2(TestHectares):
    NEGOTIATION_STATUS = "intended (under negotiation)"
    POSTFIX = '.json?negotiation_status=concluded&negotiation_status=intended&deal_scope=transnational'
    NUM_RELEVANT_COMBINATIONS = 2


class TestHectaresFailed(TestHectares):
    NEGOTIATION_STATUS = "failed (contract canceled)"
    POSTFIX = '.json?negotiation_status=failed&deal_scope=transnational'


class TestHectaresDomesticConcluded(TestHectares):
    NEGOTIATION_STATUS = 'concluded (oral agreement)'
    DEAL_SCOPE = 'domestic'
    POSTFIX = '.json?negotiation_status=concluded&deal_scope=domestic'


class TestHectaresDomesticIntended(TestHectaresDomesticConcluded):
    NEGOTIATION_STATUS = "intended (under negotiation)"
    POSTFIX = '.json?negotiation_status=intended&deal_scope=domestic'


class TestHectaresDomesticConcludedIntended1(TestHectaresDomesticConcluded):
    NEGOTIATION_STATUS = 'concluded (oral agreement)'
    POSTFIX = '.json?negotiation_status=concluded&negotiation_status=intended&deal_scope=domestic'
    NUM_RELEVANT_COMBINATIONS = 2


class TestHectaresDomesticConcludedIntended2(TestHectaresDomesticConcluded):
    NEGOTIATION_STATUS = "intended (under negotiation)"
    POSTFIX = '.json?negotiation_status=concluded&negotiation_status=intended&deal_scope=domestic'
    NUM_RELEVANT_COMBINATIONS = 2


class TestHectaresDomesticFailed(TestHectaresDomesticConcluded):
    NEGOTIATION_STATUS = "failed (contract canceled)"
    POSTFIX = '.json?negotiation_status=failed&deal_scope=domestic'


class TestHectaresDataSource(TestHectares):

    POSTFIX = '.json?negotiation_status=concluded&deal_scope=transnational&data_source_type=1'
    RELEVANT_ATTRIBUTES = {'type': 'Media report'}
    NUM_RELEVANT_COMBINATIONS = 0


class TestHectaresDataSourceNot(TestHectares):
    POSTFIX = '.json?negotiation_status=concluded&deal_scope=transnational&data_source_type=1'
    RELEVANT_ATTRIBUTES = {'type': 'NOT A Media report'}

