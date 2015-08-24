__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django.test import TestCase
from django.core.urlresolvers import reverse
from landmatrix.models import *
import json

from .deals_test_data import DealsTestData

class ApiTest(TestCase):

    def url(self, resource): return self.PREFIX + resource + self.POSTFIX
    def url_id(self, resource, id): return self.PREFIX + resource + self.INFIX + str(id) + self.POSTFIX

class ApiTestBase(DealsTestData):

    def get_content(self, resource):
        response = self.client.get(self.url(resource))
#        self.assertEqual(200, response.status_code)
        return json.loads(response.content.decode('utf-8'))

    def test_view_gets_called(self):
        response = self.client.get(self.url('status'))
        self.assertEqual(200, response.status_code)

    def test_view_returns_json(self):
        response = self.client.get(self.url('status'))
        json.loads(response.content.decode('utf-8'))

    def test_existing_record(self):
        response = self.client.get(self.url_id('status', 6))
        self.assertEqual(200, response.status_code)

    def test_nonexistent_record(self):
        response = self.client.get(self.url_id('status', 99999))
        self.assertEqual(404, response.status_code)

    def test_view_content(self):
        self.make_involvement()
        self.make_involvement(1.23)

        content = self.get_content('involvement')
        self.assertIsInstance(content, dict)
        self.assertGreaterEqual(len(content), 2)
        self.assertTrue(self.RESULTS_INDEX in content)

        for record in content[self.RESULTS_INDEX]:
            self.assertIsInstance(record, dict)
            self.assertTrue(self.URI_INDEX in record)
            self.assertTrue('investment_ratio' in record)

        self.assertEqual(1.23, float(content[self.RESULTS_INDEX][1]['investment_ratio']))

    def test_access_specific_record(self):
        self.make_involvement(1.23)

        content = self.get_content('involvement')
        response = self.client.get(content[self.RESULTS_INDEX][0][self.URI_INDEX])
        self.assertEqual(200, response.status_code)

        content = json.loads(response.content.decode('utf-8'))
        self.assertIsInstance(content, dict)
        self.assertTrue(self.URI_INDEX in content)
        self.assertTrue('investment_ratio' in content)
        self.assertEqual(1.23, float(content['investment_ratio']))

    def test_all_defined_models(self):
        for model in self.MODELS:
            content = self.get_content(model)
            self.assertIsInstance(content, dict)

    def test_foreign_keys(self):
        self.make_involvement()
        response = self.client.get(self.url('involvement'))
        content = json.loads(response.content.decode('utf-8'))
        for fk in ('fk_activity', 'fk_stakeholder', 'fk_primary_investor'):
            self.assertTrue(fk in content[self.RESULTS_INDEX][0])
            response = self.client.get(content[self.RESULTS_INDEX][0][fk])
            self.assertEqual(200, response.status_code)


class TastyPieTest(ApiTest, ApiTestBase):

    PREFIX = '/en/api/api/'
    POSTFIX = '/?format=json'
    INFIX = '/'
    URI_INDEX = 'resource_uri'
    RESULTS_INDEX = 'objects'
    MODELS = [ 'involvement', 'activity', 'stakeholder', 'primaryinvestor', 'status', 'activityattributegroup']

