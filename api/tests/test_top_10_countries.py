import pprint
from api.query_sets.top_10_countries_query_set import Top10InvestorCountriesQuerySet, Top10TargetCountriesQuerySet
from landmatrix.models.country import Country

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


from .api_test_functions import ApiTestFunctions
from api.tests.deals_test_data import DealsTestData

"""
/en/api/top-10-countries.json?negotiation_status=concluded&deal_scope=transnational
/en/api/top-10-countries.json?negotiation_status=intended&deal_scope=transnational
/en/api/top-10-countries.json?negotiation_status=concluded&negotiation_status=intended&deal_scope=transnational
/en/api/top-10-countries.json?negotiation_status=failed&deal_scope=transnational
/en/api/top-10-countries.json?negotiation_status=concluded&deal_scope=transnational&data_source_type=1
/en/api/top-10-countries.json?negotiation_status=intended&deal_scope=transnational&data_source_type=1
/en/api/top-10-countries.json?negotiation_status=concluded&negotiation_status=intended&deal_scope=transnational&data_source_type=1
/en/api/top-10-countries.json?negotiation_status=failed&deal_scope=transnational&data_source_type=1
"""

class TestTop10Countries(ApiTestFunctions, DealsTestData):

    PREFIX = '/en/api/'
    POSTFIX = '.json?negotiation_status=concluded&deal_scope=transnational'
    DEAL_SCOPE = 'transnational'
    NEGOTIATION_STATUS = 'concluded (oral agreement)'
    RELEVANT_ATTRIBUTES = {}
    NUM_RELEVANT_DEALS = 1

    def setUp(self):
        self.RELEVANT_ATTRIBUTES['deal_scope'] = self.DEAL_SCOPE

    def tearDown(self):
        Top10InvestorCountriesQuerySet.DEBUG = False

    def test_empty(self):
        result = self.get_content('top-10-countries')
        self.assertEqual(2, len(result))
        for country in result.values():
            self.assertEqual(0, len(country))

    NUM_DEALS = 11
    def test_with_data(self):
        self._generate_enough_deals(self.NEGOTIATION_STATUS)

        investors, targets = self._get_result()

        self.assertEqual(1, len(targets))
        self.assertEqual(self.deal_country.name, targets[0]['name'])
        self.assertEqual(self.NUM_DEALS, targets[0]['deals'])
        self.assertEqual((2 << self.NUM_DEALS)-2, targets[0]['hectares'])

        self.assertEqual(10, len(investors))
        last_size = 1000000
        for i in range(0, 10):
            self.assertEqual(1, investors[i]['deals'])
            self.assertGreater(last_size, investors[i]['hectares'])
            last_size = investors[i]['hectares']

    def test_with_wrong_status(self):
        self._generate_enough_deals(self.NEGOTIATION_STATUS + 'xxx')

        investors, targets = self._get_result()

        self.assertEqual(0, len(targets))
        self.assertEqual(0, len(investors))

    def _get_result(self):
        result = self.get_content('top-10-countries')
        investors = result['investor_country']
        targets = result['target_country']
        return investors, targets

    def _generate_enough_deals(self, status):
        self._generate_countries(self.NUM_DEALS)
        for i in range(0, self.NUM_DEALS + 1):
            investor_country = Country(self.investor_country.id + 1 + i)
            attributes = {'pi_deal_size': 2 << i, 'deal_scope': self.DEAL_SCOPE, 'pi_negotiation_status': status}
            attributes.update(self.RELEVANT_ATTRIBUTES)
            self._generate_deal(investor_country, self.deal_country, attributes)


class TestTop10CountriesIntended(TestTop10Countries):
    NEGOTIATION_STATUS = "intended (under negotiation)"
    POSTFIX = '.json?negotiation_status=intended&deal_scope=transnational'


class TestTop10CountriesConcludedIntended1(TestTop10Countries):
    NEGOTIATION_STATUS = 'concluded (oral agreement)'
    POSTFIX = '.json?negotiation_status=concluded&negotiation_status=intended&deal_scope=transnational'


class TestTop10CountriesConcludedIntended2(TestTop10Countries):
    NEGOTIATION_STATUS = "intended (under negotiation)"
    POSTFIX = '.json?negotiation_status=concluded&negotiation_status=intended&deal_scope=transnational'


class TestTop10CountriesFailed(TestTop10Countries):
    NEGOTIATION_STATUS = "failed (contract canceled)"
    POSTFIX = '.json?negotiation_status=failed&deal_scope=transnational'


class TestTop10CountriesDataSource(TestTop10Countries):

    POSTFIX = '.json?negotiation_status=concluded&deal_scope=transnational&data_source_type=1'
    RELEVANT_ATTRIBUTES = {'type': 'Media report'}

    def test_with_data(self):
        self._generate_enough_deals(self.NEGOTIATION_STATUS)
        investors, targets = self._get_result()
        self.assertEqual(0, len(targets))
        self.assertEqual(0, len(investors))


class TestTop10CountriesDataSourceNot(TestTop10Countries):
    POSTFIX = '.json?negotiation_status=concluded&deal_scope=transnational&data_source_type=1'
    RELEVANT_ATTRIBUTES = {'type': 'NOT A Media report'}
