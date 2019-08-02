from django.conf import settings
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse

from api.elasticsearch import es_save
from landmatrix.models import Country
from wagtailcms.models import RegionPage, CountryPage


class CountryListViewTestCase(TestCase):

    fixtures = [
        'countries_and_regions'
    ]

    def test(self):
        response = self.client.get(reverse('countries_api'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(Country.objects.all().count(), len(response.data))
        expected = [4, 'afghanistan', 'Afghanistan']
        self.assertEqual(expected, response.data[0])


class TargetCountryListViewTestCase(TestCase):

    fixtures = [
        'countries_and_regions'
    ]

    def setUp(self):
        CountryPage.objects.create(title='Cambodia Page', country_id=116, path='/', depth=0)

    def test(self):
        response = self.client.get(reverse('target_countries_api'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.data))
        self.assertEqual('Observatories', response.data[0]['text'])
        expected = [[116, 'cambodia-page', 'Cambodia Page']]
        self.assertEqual(expected, response.data[0]['children'])
        self.assertEqual('Other', response.data[1]['text'])
        expected = [[104, 'myanmar', 'Myanmar']]
        self.assertEqual(expected, response.data[1]['children'])


class RegionListViewTestCase(TestCase):

    fixtures = [
        'countries_and_regions'
    ]

    def setUp(self):
        RegionPage.objects.create(title='Asia Page', region_id=142, path='/', depth=0)

    def test(self):
        response = self.client.get(reverse('regions_api'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.data))
        expected = [142, 'asia', 'Asia Page']
        self.assertEqual(expected, response.data[0])


class InvestorListViewTestCase(TestCase):

    @classmethod
    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def setUpClass(cls):
        super().setUpClass()

        fixtures = [
            'status',
            'countries_and_regions',
            'users_and_groups',
            'investors',
            'venture_involvements',
        ]
        for fixture in fixtures:
            call_command('loaddata', fixture)

        es_save.create_index(delete=True)
        #es_save.index_activity_documents()
        es_save.index_investor_documents()
        es_save.refresh_index()

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test(self):
        response = self.client.get(reverse('investors_api'), data={'q': 'test'})
        self.assertEqual(200, response.status_code)
        self.assertGreater(response.data.get('count'), 0)
        self.assertGreater(len(response.data.get('results')), 0)
        self.assertIn('next', response.data.keys())
        self.assertIn('previous', response.data.keys())
