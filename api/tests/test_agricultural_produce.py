from api.views.agricultural_produce_json_view import AgriculturalProduceJSONView
from landmatrix.models.activity import Activity
from landmatrix.models.activity_attribute_group import ActivityAttributeGroup
from landmatrix.models.agricultural_produce import AgriculturalProduce
from landmatrix.models.crop import Crop

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from .api_test_functions import ApiTestFunctions
from api.tests.deals_test_data import DealsTestData

"""
/en/api/agricultural-produce.json?negotiation_status=intended&deal_scope=domestic
/en/api/agricultural-produce.json?negotiation_status=intended&deal_scope=transnational
/en/api/agricultural-produce.json?negotiation_status=intended&deal_scope=domestic&deal_scope=transnational
/en/api/agricultural-produce.json?negotiation_status=concluded&deal_scope=domestic
/en/api/agricultural-produce.json?negotiation_status=concluded&deal_scope=transnational
/en/api/agricultural-produce.json?negotiation_status=concluded&deal_scope=domestic&deal_scope=transnational
/en/api/agricultural-produce.json?negotiation_status=intended&negotiation_status=concluded&deal_scope=domestic
/en/api/agricultural-produce.json?negotiation_status=intended&negotiation_status=concluded&deal_scope=transnational
/en/api/agricultural-produce.json?negotiation_status=intended&negotiation_status=concluded&deal_scope=domestic&deal_scope=transnational
/en/api/agricultural-produce.json?negotiation_status=failed&deal_scope=domestic
/en/api/agricultural-produce.json?negotiation_status=failed&deal_scope=transnational
/en/api/agricultural-produce.json?negotiation_status=failed&deal_scope=domestic&deal_scope=transnational
/en/api/agricultural-produce.json?negotiation_status=intended&deal_scope=domestic&data_source_type=1
/en/api/agricultural-produce.json?negotiation_status=intended&deal_scope=transnational&data_source_type=1
/en/api/agricultural-produce.json?negotiation_status=intended&deal_scope=domestic&deal_scope=transnational&data_source_type=1
/en/api/agricultural-produce.json?negotiation_status=concluded&deal_scope=domestic&data_source_type=1
/en/api/agricultural-produce.json?negotiation_status=concluded&deal_scope=transnational&data_source_type=1
/en/api/agricultural-produce.json?negotiation_status=concluded&deal_scope=domestic&deal_scope=transnational&data_source_type=1
/en/api/agricultural-produce.json?negotiation_status=intended&negotiation_status=concluded&deal_scope=domestic&data_source_type=1
/en/api/agricultural-produce.json?negotiation_status=intended&negotiation_status=concluded&deal_scope=transnational&data_source_type=1
/en/api/agricultural-produce.json?negotiation_status=intended&negotiation_status=concluded&deal_scope=domestic&deal_scope=transnational&data_source_type=1
/en/api/agricultural-produce.json?negotiation_status=failed&deal_scope=domestic&data_source_type=1
/en/api/agricultural-produce.json?negotiation_status=failed&deal_scope=transnational&data_source_type=1
/en/api/agricultural-produce.json?negotiation_status=failed&deal_scope=domestic&deal_scope=transnational&data_source_type=1
"""


class TestAgriculturalProduce(ApiTestFunctions, DealsTestData):

    PREFIX = '/en/api/'
    POSTFIX = '.json?negotiation_status=concluded&deal_scope=transnational'
    DEAL_SCOPE = 'transnational'
    NEGOTIATION_STATUS = 'concluded (oral agreement)'
    RELEVANT_ATTRIBUTES = {}
    NUM_RELEVANT_COMBINATIONS = 1

    def test_empty(self):
        result = self.get_content('agricultural-produce')
        self.assertEqual(len(AgriculturalProduceJSONView.REGIONS), len(result))
        for region in result:
            self.assertIn(region['region'], AgriculturalProduceJSONView.REGIONS)
            self.assertEqual(0, region['available'])
            self.assertEqual(0, region['not_available'])

    def test_with_data(self):
        self._generate_enough_deals()
        result = self.get_content('agricultural-produce')
        for region in result:
            self.assertIn(region['region'], AgriculturalProduceJSONView.REGIONS)
            if region['region'] == 'overall':
                self.assertEqual(
                    self.NUM_RELEVANT_COMBINATIONS*AgriculturalProduce.objects.count()*(self.NUM_DEALS*(self.NUM_DEALS+1))/2*self.NUM_CROPS*2,
                    region['available']
                )
                self.assertEqual(0, region['not_available'])
                for produce in region['hectares']:
                    if produce == 'multiple_use':
                        self.assertEqual(0, region['hectares'][produce])
                    else:
                        self.assertEqual(2*self.NUM_RELEVANT_COMBINATIONS*self.NUM_CROPS*(self.NUM_DEALS*(self.NUM_DEALS+1))/2, region['hectares'][produce])

            else:
                self.assertEqual(0, region['available'])
                self.assertEqual(0, region['not_available'])
                for subfield in ['hectares', 'agricultural_produce']:
                    for produce in region[subfield]:
                        self.assertEqual(0, region[subfield][produce])

    NUM_DEALS = 1
    def _generate_enough_deals(self):
        self._generate_countries(0)
        self._generate_agricultural_produce()
        for i in range(0, self.NUM_DEALS):
            for scope in ['transnational', 'domestic']:
                for status in ['concluded (oral agreement)', "intended (under negotiation)", "failed (contract canceled)"]:
                    for crop in Crop.objects.all():
                        attributes = {'pi_deal_size': 2 << i, 'deal_scope': scope, 'pi_negotiation_status': status, 'crops': crop.id}
                        attributes.update(self.RELEVANT_ATTRIBUTES)
                        self._generate_deal(self.investor_country, self.deal_country, attributes)


    NUM_CROPS = 2
    def _generate_agricultural_produce(self):
        for produce_name in ['Food Crop', 'Non-Food', 'Flex-Crop']:
            produce = AgriculturalProduce(name=produce_name)
            produce.save()
            for i in range(0, self.NUM_CROPS):
                Crop(name=produce_name+str(i), fk_agricultural_produce=produce).save()

class TestAgriculturalProduceIntended(TestAgriculturalProduce):
    NEGOTIATION_STATUS = "intended (under negotiation)"
    POSTFIX = '.json?negotiation_status=intended&deal_scope=transnational'


class TestAgriculturalProduceConcludedIntended1(TestAgriculturalProduce):
    NEGOTIATION_STATUS = 'concluded (oral agreement)'
    POSTFIX = '.json?negotiation_status=concluded&negotiation_status=intended&deal_scope=transnational'
    NUM_RELEVANT_COMBINATIONS = 2


class TestAgriculturalProduceConcludedIntended2(TestAgriculturalProduce):
    NEGOTIATION_STATUS = "intended (under negotiation)"
    POSTFIX = '.json?negotiation_status=concluded&negotiation_status=intended&deal_scope=transnational'
    NUM_RELEVANT_COMBINATIONS = 2


class TestAgriculturalProduceFailed(TestAgriculturalProduce):
    NEGOTIATION_STATUS = "failed (contract canceled)"
    POSTFIX = '.json?negotiation_status=failed&deal_scope=transnational'


class TestAgriculturalProduceDomesticConcluded(TestAgriculturalProduce):
    NEGOTIATION_STATUS = 'concluded (oral agreement)'
    DEAL_SCOPE = 'domestic'
    POSTFIX = '.json?negotiation_status=concluded&deal_scope=domestic'


class TestAgriculturalProduceDomesticIntended(TestAgriculturalProduceDomesticConcluded):
    NEGOTIATION_STATUS = "intended (under negotiation)"
    POSTFIX = '.json?negotiation_status=intended&deal_scope=domestic'


class TestAgriculturalProduceDomesticConcludedIntended1(TestAgriculturalProduceDomesticConcluded):
    NEGOTIATION_STATUS = 'concluded (oral agreement)'
    POSTFIX = '.json?negotiation_status=concluded&negotiation_status=intended&deal_scope=domestic'
    NUM_RELEVANT_COMBINATIONS = 2


class TestAgriculturalProduceDomesticConcludedIntended2(TestAgriculturalProduceDomesticConcluded):
    NEGOTIATION_STATUS = "intended (under negotiation)"
    POSTFIX = '.json?negotiation_status=concluded&negotiation_status=intended&deal_scope=domestic'
    NUM_RELEVANT_COMBINATIONS = 2


class TestAgriculturalProduceDomesticFailed(TestAgriculturalProduceDomesticConcluded):
    NEGOTIATION_STATUS = "failed (contract canceled)"
    POSTFIX = '.json?negotiation_status=failed&deal_scope=domestic'

def pprint(array):
    for element in array:
        print(element)