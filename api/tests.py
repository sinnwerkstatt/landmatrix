__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django.test import TestCase
from django.core.urlresolvers import reverse
from landmatrix.models import Involvement
import json

class ApiViewTest(TestCase):

    def test_view_gets_called(self):
        response = self.client.get('/en/api/involvement/')
        self.assertEqual(200, response.status_code)

    def test_view_returns_json(self):
        response = self.client.get('/en/api/involvement/')
        json.loads(response.content.decode('utf-8'))

    def test_view_content(self):
        Involvement().save()
        Involvement(investment_ratio = 1.23).save()

        response = self.client.get('/en/api/involvement/')
        content = json.loads(response.content.decode('utf-8'))
        self.assertIsInstance(content, dict)
        self.assertGreaterEqual(len(content), 2)
        self.assertIsInstance(content, dict)
        self.assertTrue('results' in content)
        for record in content['results']:
            self.assertIsInstance(record, dict)
            self.assertTrue('url' in record)
            self.assertTrue('investment_ratio' in record)

        self.assertEqual(1.23, float(content['results'][1]['investment_ratio']))

    def test_access_specific_record(self):
        Involvement(investment_ratio = 1.23).save()
        response = self.client.get('/en/api/involvement/')
        content = json.loads(response.content.decode('utf-8'))
        url = content['results'][0]['url']
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        content = json.loads(response.content.decode('utf-8'))
        self.assertIsInstance(content, dict)
        self.assertTrue('url' in content)
        self.assertTrue('investment_ratio' in content)
        self.assertEqual(1.23, float(content['investment_ratio']))

    def test_nonexistent_record(self):
        response = self.client.get('/en/api/involvement/999999/')
        self.assertEqual(404, response.status_code)

    