from django.test import TestCase
from django.core.urlresolvers import reverse
from landmatrix.models import Involvement
import json

class ApiViewTest(TestCase):

    def test_view_gets_called(self):
        response = self.client.get('/api/involvement/')
        self.assertEqual(200, response.status_code)

    def test_view_returns_json(self):
        response = self.client.get('/api/involvement/')
        json.loads(response.content.decode('utf-8'))

    def test_view_content(self):
        i = Involvement()
        i.save();
        i = Involvement(investment_ratio = 1.23)
        i.save();

        response = self.client.get('/api/involvement/')
        content = json.loads(response.content.decode('utf-8'))
        print(content)
        self.assertIsInstance(content, list)
        self.assertGreaterEqual(2, len(content))
        self.assertIsInstance(content[0], dict)
        self.assertIsInstance(content[1], dict)
