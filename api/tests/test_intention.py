from landmatrix.models.activity_attribute_group import ActivityAttribute

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from api.query_sets.intention_query_set import IntentionQuerySet
from .api_test_functions import ApiTestFunctions
from api.tests.deals_test_data import DealsTestData


"""
/en/api/intention_of_investment.json?negotiation_status=concluded&deal_scope=transnational
/en/api/intention_of_investment.json?negotiation_status=intended&deal_scope=transnational
/en/api/intention_of_investment.json?negotiation_status=concluded&negotiation_status=intended&deal_scope=transnational
/en/api/intention_of_investment.json?negotiation_status=failed&deal_scope=transnational
/en/api/intention_of_investment.json?negotiation_status=concluded&deal_scope=domestic
/en/api/intention_of_investment.json?negotiation_status=intended&deal_scope=domestic
/en/api/intention_of_investment.json?negotiation_status=concluded&negotiation_status=intended&deal_scope=domestic
/en/api/intention_of_investment.json?negotiation_status=failed&deal_scope=domestic
/en/api/intention_of_investment.json?negotiation_status=concluded&deal_scope=transnational&deal_scope=domestic
/en/api/intention_of_investment.json?negotiation_status=intended&deal_scope=transnational&deal_scope=domestic
/en/api/intention_of_investment.json?negotiation_status=concluded&negotiation_status=intended&deal_scope=transnational&deal_scope=domestic
/en/api/intention_of_investment.json?negotiation_status=failed&deal_scope=transnational&deal_scope=domestic
/en/api/intention_of_investment.json?negotiation_status=concluded&deal_scope=transnational&data_source_type=1
/en/api/intention_of_investment.json?negotiation_status=intended&deal_scope=transnational&data_source_type=1
/en/api/intention_of_investment.json?negotiation_status=concluded&negotiation_status=intended&deal_scope=transnational&data_source_type=1
/en/api/intention_of_investment.json?negotiation_status=failed&deal_scope=transnational&data_source_type=1
/en/api/intention_of_investment.json?negotiation_status=concluded&deal_scope=domestic&data_source_type=1
/en/api/intention_of_investment.json?negotiation_status=intended&deal_scope=domestic&data_source_type=1
/en/api/intention_of_investment.json?negotiation_status=concluded&negotiation_status=intended&deal_scope=domestic&data_source_type=1
/en/api/intention_of_investment.json?negotiation_status=failed&deal_scope=domestic&data_source_type=1
/en/api/intention_of_investment.json?negotiation_status=concluded&deal_scope=transnational&deal_scope=domestic&data_source_type=1
/en/api/intention_of_investment.json?negotiation_status=intended&deal_scope=transnational&deal_scope=domestic&data_source_type=1
/en/api/intention_of_investment.json?negotiation_status=concluded&negotiation_status=intended&deal_scope=transnational&deal_scope=domestic&data_source_type=1
/en/api/intention_of_investment.json?negotiation_status=failed&deal_scope=transnational&deal_scope=domestic&data_source_type=1

/en/api/intention_of_investment.json?deal_scope=domestic&intention=agriculture
/en/api/intention_of_investment.json?deal_scope=transnational&intention=agriculture
/en/api/intention_of_investment.json?deal_scope=domestic&deal_scope=transnational&intention=agriculture
/en/api/intention_of_investment.json?deal_scope=domestic&intention=agriculture&data_source_type=1
/en/api/intention_of_investment.json?deal_scope=transnational&intention=agriculture&data_source_type=1
/en/api/intention_of_investment.json?deal_scope=domestic&deal_scope=transnational&intention=agriculture&data_source_type=1
"""


class TestIntention(ApiTestFunctions, DealsTestData):

    PREFIX = '/api/'
    POSTFIX = '.json?negotiation_status=concluded&deal_scope=transnational'
    DEAL_SCOPE = 'transnational'
    DEAL_SIZE = 12345
    RELEVANT_ATTRIBUTES = {
        'intention': 'Forestry', 'pi_negotiation_status': 'Concluded (Contract signed)'
    }
    NUM_RELEVANT_DEALS = 1

    def tearDown(self):
        IntentionQuerySet.DEBUG = False

    def test_empty(self):
        result = self.get_content('intention_of_investment')
        self.assertEqual(self.num_results(), len(result))
        for record in result:
            self.assertEqual(0, record['deals'])
            self.assertEqual(0, record['hectares'])

    def test_with_data(self):
        self._generate_negotiation_status_data(123, self.DEAL_SIZE, self.DEAL_SCOPE, self.RELEVANT_ATTRIBUTES)
        IntentionQuerySet.DEBUG = False
        result = self.get_content('intention_of_investment')
        if self.__class__.__name__ == 'TestIntentionAgriculture...':
            print(self.RELEVANT_ATTRIBUTES, ActivityAttribute.objects.all(), result)

        self.assertEqual(self.num_results(), len(result))

        if self.NUM_RELEVANT_DEALS == 0: return

        relevant_line = list(filter(lambda line: line['name'] == self.RELEVANT_ATTRIBUTES['intention'], result))

        self.assertEqual(1 if self.NUM_RELEVANT_DEALS > 0 else 0, relevant_line[0]['deals'])
        self.assertEqual(self.RELEVANT_ATTRIBUTES['intention'], relevant_line[0]['name'])
        self.assertEqual(float(self.DEAL_SIZE) if self.NUM_RELEVANT_DEALS > 0 else 0, relevant_line[0]['hectares'])

    def num_results(self):
        return len(IntentionQuerySet.INTENTIONS)+2

    def test_with_both_transnational_and_domestic(self):
        attributes = self.RELEVANT_ATTRIBUTES
        for index, scope in enumerate(['transnational', 'domestic']):
            self._generate_negotiation_status_data(123+index, self.DEAL_SIZE, scope, attributes)

        result = self.get_content('intention_of_investment')
        self.assertEqual(self.num_results(), len(result))

        if self.NUM_RELEVANT_DEALS == 0: return

        relevant_line = list(filter(lambda line: line['name'] == self.RELEVANT_ATTRIBUTES['intention'], result))
        self.assertEqual(self.NUM_RELEVANT_DEALS, relevant_line[0]['deals'])
        self.assertEqual(self.RELEVANT_ATTRIBUTES['intention'], relevant_line[0]['name'])
        self.assertEqual(self.NUM_RELEVANT_DEALS*float(self.DEAL_SIZE), relevant_line[0]['hectares'])


class TestIntentionIntended(TestIntention):

    POSTFIX = '.json?negotiation_status=intended&deal_scope=transnational'
    RELEVANT_ATTRIBUTES = {
        'pi_deal_size': '12345', 'deal_scope': 'transnational', 'intention': 'Forestry', 'pi_negotiation_status': 'intended (expression of interest)'
    }
    NUM_RELEVANT_DEALS = 1


class TestIntentionFailed(TestIntention):

    POSTFIX = '.json?negotiation_status=failed&deal_scope=transnational'
    RELEVANT_ATTRIBUTES = {
        'pi_deal_size': '12345', 'deal_scope': 'transnational', 'intention': 'Forestry', 'pi_negotiation_status': 'Failed (negotiations failed)'
    }
    NUM_RELEVANT_DEALS = 1


class TestIntentionConcludedIntended1(TestIntention):

    POSTFIX = '.json?negotiation_status=intended&negotiation_status=concluded&deal_scope=transnational'
    RELEVANT_ATTRIBUTES = {
        'pi_deal_size': '12345', 'deal_scope': 'transnational', 'intention': 'Forestry', 'pi_negotiation_status': 'intended (expression of interest)'
    }
    NUM_RELEVANT_DEALS = 1


class TestIntentionConcludedIntended2(TestIntention):

    POSTFIX = '.json?negotiation_status=intended&negotiation_status=concluded&deal_scope=transnational'
    RELEVANT_ATTRIBUTES = {
        'pi_deal_size': '12345', 'deal_scope': 'transnational', 'intention': 'Forestry', 'pi_negotiation_status': 'Concluded (Contract signed)'
    }
    NUM_RELEVANT_DEALS = 1


class TestIntentionConcludedIntended3(TestIntention):

    POSTFIX = '.json?negotiation_status=intended&negotiation_status=concluded&deal_scope=transnational'
    RELEVANT_ATTRIBUTES = {
        'pi_deal_size': '12345', 'deal_scope': 'transnational', 'intention': 'Forestry', 'pi_negotiation_status': 'Failed (negotiations failed)'
    }
    NUM_RELEVANT_DEALS = 0


class TestIntentionConcludedDomestic(TestIntention):

    POSTFIX = '.json?negotiation_status=concluded&deal_scope=domestic'
    DEAL_SCOPE = 'domestic'
    RELEVANT_ATTRIBUTES = {
        'pi_deal_size': '12345', 'deal_scope': 'domestic', 'intention': 'Forestry', 'pi_negotiation_status': 'Concluded (Contract signed)'
    }
    NUM_RELEVANT_DEALS = 1


class TestIntentionIntendedDomestic(TestIntentionConcludedDomestic):

    POSTFIX = '.json?negotiation_status=intended&deal_scope=domestic'
    DEAL_SCOPE = 'domestic'
    RELEVANT_ATTRIBUTES = {
        'pi_deal_size': '12345', 'deal_scope': 'domestic', 'intention': 'Forestry', 'pi_negotiation_status': 'intended (expression of interest)'
    }
    NUM_RELEVANT_DEALS = 1


class TestIntentionFailedDomestic(TestIntentionConcludedDomestic):

    POSTFIX = '.json?negotiation_status=failed&deal_scope=domestic'
    DEAL_SCOPE = 'domestic'
    RELEVANT_ATTRIBUTES = {
        'pi_deal_size': '12345', 'deal_scope': 'domestic', 'intention': 'Forestry', 'pi_negotiation_status': 'Failed (negotiations failed)'
    }
    NUM_RELEVANT_DEALS = 1


class TestIntentionConcludedIntendedDomestic1(TestIntentionConcludedDomestic):

    POSTFIX = '.json?negotiation_status=intended&negotiation_status=concluded&deal_scope=domestic'
    DEAL_SCOPE = 'domestic'
    RELEVANT_ATTRIBUTES = {
        'pi_deal_size': '12345', 'deal_scope': 'domestic', 'intention': 'Forestry', 'pi_negotiation_status': 'intended (expression of interest)'
    }
    NUM_RELEVANT_DEALS = 1


class TestIntentionConcludedIntendedDomestic2(TestIntentionConcludedDomestic):

    POSTFIX = '.json?negotiation_status=intended&negotiation_status=concluded&deal_scope=domestic'
    DEAL_SCOPE = 'domestic'
    RELEVANT_ATTRIBUTES = {
        'pi_deal_size': '12345', 'deal_scope': 'domestic', 'intention': 'Forestry', 'pi_negotiation_status': 'Concluded (Contract signed)'
    }
    NUM_RELEVANT_DEALS = 1


class TestIntentionConcludedIntendedDomestic3(TestIntentionConcludedDomestic):

    POSTFIX = '.json?negotiation_status=intended&negotiation_status=concluded&deal_scope=domestic'
    DEAL_SCOPE = 'domestic'
    RELEVANT_ATTRIBUTES = {
        'pi_deal_size': '12345', 'deal_scope': 'domestic', 'intention': 'Forestry', 'pi_negotiation_status': 'Failed (negotiations failed)'
    }
    NUM_RELEVANT_DEALS = 0


class TestIntentionDataSource(TestIntention):

    POSTFIX = '.json?negotiation_status=concluded&deal_scope=transnational&data_source_type=1'
    RELEVANT_ATTRIBUTES = {
        'pi_deal_size': '12345', 'deal_scope': 'transnational', 'intention': 'Forestry', 'pi_negotiation_status': 'Concluded (Contract signed)',
        'type': 'Media report'
    }
    NUM_RELEVANT_DEALS = 0


class TestIntentionDataSourceNot(TestIntention):

    POSTFIX = '.json?negotiation_status=concluded&deal_scope=transnational&data_source_type=1'
    RELEVANT_ATTRIBUTES = {
        'pi_deal_size': '12345', 'deal_scope': 'transnational', 'intention': 'Forestry', 'pi_negotiation_status': 'Concluded (Contract signed)',
        'type': 'NOT Media report'
    }
    NUM_RELEVANT_DEALS = 1


class TestIntentionAgriculture(TestIntention):

    POSTFIX = '.json?negotiation_status=concluded&deal_scope=transnational&intention=agriculture'
    RELEVANT_ATTRIBUTES = {
        'pi_deal_size': '12345', 'deal_scope': 'transnational', 'intention': 'Forestry', 'pi_negotiation_status': 'Concluded (Contract signed)',
        'type': 'Media report'
    }
    NUM_RELEVANT_DEALS = 0

    def num_results(self):
        return len(IntentionQuerySet.INTENTIONS_AGRICULTURE)+2


class TestIntentionBiofuels(TestIntentionAgriculture):

    RELEVANT_ATTRIBUTES = {
        'pi_deal_size': '12345', 'deal_scope': 'transnational', 'intention': 'Biofuels', 'pi_negotiation_status': 'Concluded (Contract signed)',
        'type': 'Media report'
    }
    NUM_RELEVANT_DEALS = 1


class TestIntentionFoodCrops(TestIntentionAgriculture):

    RELEVANT_ATTRIBUTES = {
        'pi_deal_size': '12345', 'deal_scope': 'transnational', 'intention': 'Food crops', 'pi_negotiation_status': 'Concluded (Contract signed)',
        'type': 'Media report'
    }
    NUM_RELEVANT_DEALS = 1


class TestIntentionLivestock(TestIntentionAgriculture):

    RELEVANT_ATTRIBUTES = {
        'pi_deal_size': '12345', 'deal_scope': 'transnational', 'intention': 'Livestock', 'pi_negotiation_status': 'Concluded (Contract signed)',
        'type': 'Media report'
    }
    NUM_RELEVANT_DEALS = 1

class TestIntentionNonfood(TestIntentionAgriculture):

    RELEVANT_ATTRIBUTES = {
        'pi_deal_size': '12345', 'deal_scope': 'transnational', 'intention': 'Non-food agricultural commodities', 'pi_negotiation_status': 'Concluded (Contract signed)',
        'type': 'Media report'
    }
    NUM_RELEVANT_DEALS = 1
