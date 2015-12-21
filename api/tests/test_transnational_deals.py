from api.query_sets.transnational_deals_query_set import TransnationalDealsQuerySet
from landmatrix.models.activity_attribute_group import ActivityAttributeGroup
from landmatrix.models.country import Country

from .api_test_functions import ApiTestFunctions
from api.tests.deals_test_data import DealsTestData

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


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
    DEAL_SIZE = 12345
    RELEVANT_ATTRIBUTES = {
        'pi_negotiation_status': 'Concluded (Contract signed)'
    }
    NUM_RELEVANT_DEALS = 1

    def setUp(self):
        self.RELEVANT_ATTRIBUTES['deal_scope'] = self.DEAL_SCOPE

    def tearDown(self):
        TransnationalDealsQuerySet.DEBUG = False

    def test_empty(self):
        result = self.get_content('transnational_deals')
        self.assertEqual(0, len(result))

    def test_with_data(self):
        self._generate_negotiation_status_data(123, self.DEAL_SIZE, self.DEAL_SCOPE, self.RELEVANT_ATTRIBUTES)
        result = self.get_content('transnational_deals')
        if self.__class__.__name__ == 'TestIntentionAgriculture...':
            TransnationalDealsQuerySet.DEBUG = True

        self.assertEqual(self.NUM_RELEVANT_DEALS*Country.objects.count(), len(result))

        if self.NUM_RELEVANT_DEALS == 0: return

        self.assertIn(str(self.deal_country.id), map(lambda entry: entry['id'], result))
        self.assertIn(str(self.investor_country.id), map(lambda entry: entry['id'], result))

        for entry in result:
            self.assertIn('slug', entry)
            self.assertIn('id', entry)
            self.assertIn('name', entry)
            self.assertIn('imports', entry)
            self.assertIn('size', entry)

        target_country = list(filter(lambda entry: entry['id'] == str(self.deal_country.id), result))[0]
        investor_country = list(filter(lambda entry: entry['id'] == str(self.investor_country.id), result))[0]

        self.assertEqual([investor_country['name']], target_country['imports'])
        self.assertEqual(str(self.deal_region.id)+'.'+self.deal_country.name, target_country['name'])

        self.assertEqual([], investor_country['imports'])
        self.assertEqual(str(self.investor_region.id)+'.'+self.investor_country.name, investor_country['name'])


class TestTransnationalDealsIntended(TestTransnationalDeals):

    POSTFIX = '.json?negotiation_status=intended&deal_scope=transnational'
    RELEVANT_ATTRIBUTES = {
        'pi_negotiation_status': 'intended (expression of interest)'
    }
    NUM_RELEVANT_DEALS = 1


class TestTransnationalDealsConcludedIntended(TestTransnationalDeals):

    POSTFIX = '.json?negotiation_status=concluded&negotiation_status=intended&deal_scope=transnational'
    RELEVANT_ATTRIBUTES = {
        'pi_negotiation_status': 'intended (expression of interest)'
    }
    NUM_RELEVANT_DEALS = 1


class TestTransnationalDealsFailed(TestTransnationalDeals):

    POSTFIX = '.json?negotiation_status=failed&deal_scope=transnational'
    RELEVANT_ATTRIBUTES = {
        'pi_negotiation_status': 'Failed (negotiations failed)'
    }
    NUM_RELEVANT_DEALS = 1


class TestTransnationalDealsDataSource(TestTransnationalDeals):

    POSTFIX = '.json?negotiation_status=intended&deal_scope=transnational&data_source_type=1'
    RELEVANT_ATTRIBUTES = {
        'pi_negotiation_status': 'intended (expression of interest)',
        'type': 'Media report'
    }
    NUM_RELEVANT_DEALS = 0


class TestTransnationalDealsDataSourceNot(TestTransnationalDeals):

    POSTFIX = '.json?negotiation_status=intended&deal_scope=transnational&data_source_type=1'
    RELEVANT_ATTRIBUTES = {
        'pi_negotiation_status': 'intended (expression of interest)',
        'type': 'NOT A Media report'
    }
    NUM_RELEVANT_DEALS = 1
