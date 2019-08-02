from subprocess import CalledProcessError

from django.http import QueryDict
from django.test import TestCase
from django.urls import reverse


class ChartRedirectViewTestCase(TestCase):

    def test(self):
        response = self.client.get(reverse('charts'))
        self.assertEqual(302, response.status_code)
        self.assertEqual(reverse('chart_transnational_deals'), response.url)

    def test_with_country(self):
        data = QueryDict('country=104')
        response = self.client.get(reverse('charts'), data)
        self.assertEqual(302, response.status_code)
        url = '%s?country=104' % reverse('chart_intention')
        self.assertEqual(url, response.url)

    def test_with_region(self):
        data = QueryDict('region=142')
        response = self.client.get(reverse('charts'), data)
        self.assertEqual(302, response.status_code)
        url = '%s?region=142' % reverse('chart_intention')
        self.assertEqual(url, response.url)


class ChartViewTestCaseMixin:

    viewname = ''
    viewname_pdf = ''

    def test(self):
        response = self.client.get(reverse(self.viewname))
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.context_data.get('chart'))

    def test_pdf(self):
        if not self.viewname_pdf:
            return
        with self.assertRaises(CalledProcessError):
            response = self.client.get(reverse(self.viewname_pdf, kwargs={'format': 'PDF'}))


class IntentionChartViewTestCase(ChartViewTestCaseMixin,
                                 TestCase):

    viewname = 'chart_intention'
    viewname_pdf = 'chart_intention_pdf'


class NegotiationStatusChartViewTestCase(ChartViewTestCaseMixin,
                                         TestCase):

    viewname = 'chart_negotiation_status'
    viewname_pdf = 'chart_negotiation_status_pdf'


class ImplementationStatusChartViewTestCase(ChartViewTestCaseMixin,
                                            TestCase):

    viewname = 'chart_implementation_status'
    viewname_pdf = 'chart_implementation_status_pdf'


class IntentionAgricultureChartViewTestCase(ChartViewTestCaseMixin,
                                            TestCase):

    viewname = 'chart_intention_agriculture'
    viewname_pdf = 'chart_intention_agriculture_pdf'


class TransnationalDealsChartViewTestCase(ChartViewTestCaseMixin,
                                          TestCase):

    viewname = 'chart_transnational_deals'
    viewname_pdf = 'chart_transnational_deals_pdf'


class MapOfInvestmentsChartViewTestCase(ChartViewTestCaseMixin,
                                        TestCase):

    viewname = 'chart_map_of_investments'
    viewname_pdf = 'chart_map_of_investments_pdf'


class PerspectiveChartViewTestCase(ChartViewTestCaseMixin,
                                   TestCase):

    viewname = 'chart_perspective'
    viewname_pdf = 'chart_perspective_pdf'


class AgriculturalDriversChartViewTestCase(ChartViewTestCaseMixin,
                                           TestCase):

    viewname = 'chart_agricultural_drivers'
    viewname_pdf = 'chart_agricultural_drivers_pdf'


class ProduceInfoChartViewTestCase(ChartViewTestCaseMixin,
                                   TestCase):

    viewname = 'chart_produce_info'
    viewname_pdf = 'chart_produce_info_pdf'


class MiningChartViewTestCase(ChartViewTestCaseMixin,
                              TestCase):

    viewname = 'chart_mining'
    viewname_pdf = 'chart_mining_pdf'


class LoggingChartViewTestCase(ChartViewTestCaseMixin,
                               TestCase):

    viewname = 'chart_logging'
    viewname_pdf = 'chart_logging_pdf'


class ContractFarmingChartViewTestCase(ChartViewTestCaseMixin,
                                       TestCase):

    viewname = 'chart_contract_farming'
    viewname_pdf = 'chart_contract_farming_pdf'