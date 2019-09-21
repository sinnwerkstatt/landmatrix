try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import csv
import zipfile
from io import BytesIO

from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse
from openpyxl import load_workbook

from apps.api.elasticsearch import es_save


class ExportViewTestCase(TestCase):

    @classmethod
    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def setUpClass(cls):
        super().setUpClass()

        fixtures = [
            'countries_and_regions',
            'users_and_groups',
            'status',
            'crops',
            'animals',
            'minerals',
            'investors',
            'activities',
            'activity_involvements',
            'venture_involvements',
        ]
        for fixture in fixtures:
            call_command('loaddata', fixture, **{'verbosity': 0})
        es_save.create_index(delete=True)
        es_save.index_activity_documents()
        es_save.index_investor_documents()
        es_save.refresh_index()

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def assert_xls_content(self, response):
        self.assertEqual('application/ms-excel', response['Content-Type'])
        wb = load_workbook(BytesIO(response.content), read_only=True)
        deals = wb['Deals']
        self.assertGreater(len([row for row in deals.rows]), 1)
        involvements = wb['Involvements']
        self.assertGreater(len([row for row in involvements.rows]), 1)
        investors = wb['Investors']
        self.assertGreater(len([row for row in investors.rows]), 1)

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_xls_without_group(self):
        response = self.client.get(reverse('export', kwargs={'format': 'xls'}))
        self.assertEqual(200, response.status_code)
        self.assert_xls_content(response)

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_xls_with_group(self):
        response = self.client.get(reverse('export', kwargs={'format': 'xls',
                                                             'group': 'target_country'}))
        self.assertEqual(200, response.status_code)
        self.assert_xls_content(response)

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_xls_with_group_value(self):
        response = self.client.get(reverse('export', kwargs={'format': 'xls',
                                                             'group': 'intention',
                                                             'group_value': 'Mining'}))
        self.assertEqual(200, response.status_code)
        self.assert_xls_content(response)

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_xls_with_group_value_country(self):
        response = self.client.get(reverse('export', kwargs={'format': 'xls',
                                                             'group': 'target_country',
                                                             'group_value': 'myanmar'}))
        self.assertEqual(200, response.status_code)
        self.assert_xls_content(response)

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_xls_with_group_value_region(self):
        response = self.client.get(reverse('export', kwargs={'format': 'xls',
                                                             'group': 'target_region',
                                                             'group_value': 'asia'}))
        self.assertEqual(200, response.status_code)
        self.assert_xls_content(response)

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_xls_with_group_value_crop(self):
        response = self.client.get(reverse('export', kwargs={'format': 'xls',
                                                             'group': 'crops',
                                                             'group_value': 'accacia'}))
        self.assertEqual(200, response.status_code)
        self.assert_xls_content(response)

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_xls_with_deal_as_anonymous(self):
        response = self.client.get(reverse('export', kwargs={'format': 'xls',
                                                             'deal_id': '1'}))
        self.assertEqual(200, response.status_code)
        self.assert_xls_content(response)

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_xls_with_deal_as_reporter(self):
        self.client.login(username='reporter', password='test')
        response = self.client.get(reverse('export', kwargs={'format': 'xls',
                                                             'deal_id': '1'}))
        self.client.logout()
        self.assertEqual(200, response.status_code)
        self.assert_xls_content(response)

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_xls_with_deal_as_reporter(self):
        self.client.login(username='editor', password='test')
        response = self.client.get(reverse('export', kwargs={'format': 'xls',
                                                             'deal_id': '1'}))
        self.client.logout()
        self.assertEqual(200, response.status_code)
        self.assert_xls_content(response)

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_csv(self):
        response = self.client.get(reverse('export', kwargs={'format': 'csv'}))
        self.assertEqual(200, response.status_code)
        self.assertEqual('application/x-zip-compressed', response['Content-Type'])
        zip_file = zipfile.ZipFile(BytesIO(response.content))
        file_names = ['deals.csv', 'involvements.csv', 'investors.csv']
        self.assertEqual(file_names, zip_file.namelist())
        for file_name in file_names:
            file_content = zip_file.open(file_name).read()
            reader = csv.reader(file_content.decode('utf-8'))
            rows = [row for row in reader]
            self.assertGreater(len(rows), 1)

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_xml(self):
        response = self.client.get(reverse('export', kwargs={'format': 'xml'}))
        self.assertEqual(200, response.status_code)
        self.assertEqual('text/xml', response['Content-Type'])
        root = ET.fromstring(response.content.decode('utf-8'))
        self.assertEqual(3, len(root))
        # Deals
        deals = root.find('deals')
        self.assertIsNotNone(deals)
        self.assertGreater(len(deals.findall('item')), 0)
        # Involvements
        involvements = root.find('involvements')
        self.assertIsNotNone(involvements)
        self.assertGreater(len(involvements.findall('item')), 0)
        # Investors
        investors = root.find('investors')
        self.assertIsNotNone(investors)
        self.assertGreater(len(investors.findall('item')), 0)
