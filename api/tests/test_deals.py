from api.query_sets.deals_query_set import DealsQuerySet

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from .api_test_functions import ApiTestFunctions
from api.tests.deals_test_data import DealsTestData


"""
        limit, investor_country, investor_region, target_country, target_region, window
"""
class TestDeals(ApiTestFunctions, DealsTestData):

    POSTFIX = '.json'
    DEAL_SCOPE = 'transnational'
    NEGOTIATION_STATUS = 'concluded (oral agreement)'
    RELEVANT_ATTRIBUTES = {}
    NUM_RELEVANT_COMBINATIONS = 1

    def setUp(self):
        self._generate_countries(0)

    def tearDown(self):
        DealsQuerySet.DEBUG = False

    def test_empty(self):
        result = self.get_content('deals')
        self.assertEqual([], result)

    def test_deal_without_coordinates_not_returned(self):
        self._generate_deal(self.investor_country, self.deal_country, {})
        result = self.get_content('deals')
        self.assertEqual([], result)

    def test_one_deal(self):
        self._generate_deal(self.investor_country, self.deal_country, {'point_lat': 0, 'point_lon': 0})
        result = self.get_content('deals')
        self.assertEqual(1, len(result))
        self.assertEqual(0, float(result[0]['point_lat']))
        self.assertEqual(0, float(result[0]['point_lon']))
        self.assertEqual(None, result[0]['intention'])

    NUM_DEALS = 3
    def test_limit(self):
        for i in range(0, self.NUM_DEALS+1):
            self._generate_deal(self.investor_country, self.deal_country, {'point_lat': i, 'point_lon': i})

        result = self.get_content('deals')
        self.assertEqual(self.NUM_DEALS+1, len(result))

        self.POSTFIX += '?limit=%i' % self.NUM_DEALS
        result = self.get_content('deals')
        self.assertEqual(self.NUM_DEALS, len(result))

    def test_investor_country(self):
        self._generate_deal(self.investor_country, self.deal_country, {'point_lat': 0, 'point_lon': 1, 'intention': 'investor_country invests in deal_country'})
        self._generate_deal(self.deal_country, self.investor_country, {'point_lat': 2, 'point_lon': 3, 'intention': 'deal_country invests in investor_country'})
        result = self.get_content('deals')
        self.assertEqual(2, len(result))
        self.POSTFIX = '.json?investor_country=' + str(self.investor_country.id)
        result = self.get_content('deals')
        self.assertEqual(1, len(result))
        self.assertEqual('investor_country invests in deal_country', result[0]['intention'])
        self.POSTFIX = '.json?investor_country=' + str(self.deal_country.id)
        result = self.get_content('deals')
        self.assertEqual(1, len(result))
        self.assertEqual('deal_country invests in investor_country', result[0]['intention'])

    def test_target_country(self):
        self._generate_deal(self.investor_country, self.deal_country, {'point_lat': 0, 'point_lon': 1, 'intention': 'investor_country invests in deal_country'})
        self._generate_deal(self.deal_country, self.investor_country, {'point_lat': 2, 'point_lon': 3, 'intention': 'deal_country invests in investor_country'})
        result = self.get_content('deals')
        self.assertEqual(2, len(result))
        self.POSTFIX = '.json?target_country=' + str(self.deal_country.id)
        result = self.get_content('deals')
        self.assertEqual(1, len(result))
        self.assertEqual('investor_country invests in deal_country', result[0]['intention'])
        self.POSTFIX = '.json?target_country=' + str(self.investor_country.id)
        result = self.get_content('deals')
        self.assertEqual(1, len(result))
        self.assertEqual('deal_country invests in investor_country', result[0]['intention'])

    def test_investor_region(self):
        self._generate_deal(self.investor_country, self.deal_country, {'point_lat': 0, 'point_lon': 1, 'intention': 'investor_country invests in deal_country'})
        self._generate_deal(self.deal_country, self.investor_country, {'point_lat': 2, 'point_lon': 3, 'intention': 'deal_country invests in investor_country'})
        DealsQuerySet.DEBUG = True
        self.POSTFIX = '.json?investor_region=' + str(self.investor_region.id)
        result = self.get_content('deals')
        self.assertEqual(1, len(result))
        self.assertEqual('investor_country invests in deal_country', result[0]['intention'])
        self.POSTFIX = '.json?investor_region=' + str(self.deal_region.id)
        result = self.get_content('deals')
        self.assertEqual(1, len(result))
        self.assertEqual('deal_country invests in investor_country', result[0]['intention'])

    MIN_LAT = -30
    MAX_LAT = 30
    MIN_LON = -30
    MAX_LON = 30
    def test_window(self):
        for lat in range(2*self.MIN_LAT, 2*self.MAX_LAT, 5):
            for lon in range(2*self.MIN_LON, 2*self.MAX_LON, 5):
                self._generate_deal(self.investor_country, self.deal_country, {'point_lat': lat, 'point_lon': lon})
        self.POSTFIX = '.json?window=%f,%f,%f,%f' % (self.MIN_LAT, self.MAX_LAT, self.MIN_LON, self.MAX_LON)
        result = self.get_content('deals')
        for point in result:
            self.assertGreaterEqual(float(point['point_lat']), self.MIN_LAT)
            self.assertLessEqual(float(point['point_lat']), self.MAX_LAT)
            self.assertGreaterEqual(float(point['point_lon']), self.MIN_LAT)
            self.assertLessEqual(float(point['point_lon']), self.MAX_LAT)
