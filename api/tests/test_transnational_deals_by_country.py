__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from .api_test_functions import ApiTestFunctions
from api.tests.deals_test_data import DealsTestData

"""
/en/api/transnational_deals_by_country.json?negotiation_status=concluded&deal_scope=transnational&country=384
...
"""


class TestTransnationalDealsByCountry(ApiTestFunctions, DealsTestData):

    POSTFIX = '.json?negotiation_status=concluded&deal_scope=transnational'
    DEAL_SCOPE = 'transnational'
    NEGOTIATION_STATUS = 'concluded (oral agreement)'
    RELEVANT_ATTRIBUTES = {}
    NUM_RELEVANT_COMBINATIONS = 1

    def test_empty(self):
        result = self.get_content('transnational_deals_by_country')
        self.assertEqual(2, len(result))
        for key in ['target_country', 'investor_country']:
            self.assertEqual(0, result[key][0]['deals'])
            self.assertEqual(0, result[key][0]['hectares'])


    def test_with_data(self):
        self._generate_enough_deals()
        result = self.get_content('transnational_deals_by_country')
        if self.NUM_RELEVANT_COMBINATIONS == 0: return
        self.assertEqual(2, len(result))
        for key in ['target_country', 'investor_country']:
            for region in [0, 1]: # country region and total
                self.assertEqual(self.NUM_RELEVANT_COMBINATIONS*self.NUM_DEALS, result[key][region]['deals'])
                self.assertEqual(2*self.NUM_RELEVANT_COMBINATIONS*((1 << self.NUM_DEALS)-1), result[key][0]['hectares'])

    NUM_DEALS = 3
    def _generate_enough_deals(self):
        self._generate_countries(0)
        for i in range(0, self.NUM_DEALS):
            for scope in ['transnational', 'domestic']:
                for status in ['concluded (oral agreement)', "intended (under negotiation)", "failed (contract canceled)"]:
                    attributes = {'pi_deal_size': 2 << i, 'deal_scope': scope, 'pi_negotiation_status': status}
                    attributes.update(self.RELEVANT_ATTRIBUTES)
                    self._generate_deal(self.investor_country, self.deal_country, attributes)

class TestTransnationalDealsByCountryIntended(TestTransnationalDealsByCountry):
    NEGOTIATION_STATUS = "intended (under negotiation)"
    POSTFIX = '.json?negotiation_status=intended&deal_scope=transnational'


class TestTransnationalDealsByCountryConcludedIntended1(TestTransnationalDealsByCountry):
    NEGOTIATION_STATUS = 'concluded (oral agreement)'
    POSTFIX = '.json?negotiation_status=concluded&negotiation_status=intended&deal_scope=transnational'
    NUM_RELEVANT_COMBINATIONS = 2


class TestTransnationalDealsByCountryConcludedIntended2(TestTransnationalDealsByCountry):
    NEGOTIATION_STATUS = "intended (under negotiation)"
    POSTFIX = '.json?negotiation_status=concluded&negotiation_status=intended&deal_scope=transnational'
    NUM_RELEVANT_COMBINATIONS = 2


class TestTransnationalDealsByCountryFailed(TestTransnationalDealsByCountry):
    NEGOTIATION_STATUS = "failed (contract canceled)"
    POSTFIX = '.json?negotiation_status=failed&deal_scope=transnational'


class TestTransnationalDealsByCountryDataSource(TestTransnationalDealsByCountry):
    POSTFIX = '.json?negotiation_status=concluded&deal_scope=transnational&data_source_type=1'
    RELEVANT_ATTRIBUTES = {'type': 'Media report'}
    NUM_RELEVANT_COMBINATIONS = 0


class TestTransnationalDealsByCountryDataSourceNot(TestTransnationalDealsByCountry):
    POSTFIX = '.json?negotiation_status=concluded&deal_scope=transnational&data_source_type=1'
    RELEVANT_ATTRIBUTES = {'type': 'NOT A Media report'}
