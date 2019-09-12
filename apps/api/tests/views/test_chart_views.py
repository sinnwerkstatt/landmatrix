from decimal import Decimal

from django.core.management import call_command
from django.http import QueryDict
from django.test import TestCase, override_settings
from django.urls import reverse

from apps.api.elasticsearch import es_save
from apps.landmatrix.models import Region


class ChartViewsTestCase(TestCase):

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
            call_command('loaddata', fixture)
        es_save.create_index(delete=True)
        es_save.index_activity_documents()
        es_save.index_investor_documents()
        es_save.refresh_index()

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_negotiation_status_list_view(self):
        response = self.client.get(reverse('negotiation_status_api'))
        self.assertEqual(200, response.status_code)
        expected = [
            {'name': 'Concluded (Contract signed)', 'deals': 3, 'hectares': 3000}
        ]
        self.assertEqual(expected, response.data)

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_resource_extraction_view(self):
        response = self.client.get(reverse('resource_extraction_api'))
        self.assertEqual(200, response.status_code)
        response_dict = dict((d['name'], d) for d in response.data)
        self.assertGreater(response_dict.get('Contract signed', {}).get('deals'), 0)
        self.assertEqual(1000, response_dict.get('Contract signed', {}).get('hectares'))

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_logging_view(self):
        response = self.client.get(reverse('logging_api'))
        self.assertEqual(200, response.status_code)
        response_dict = dict((d['name'], d) for d in response.data)
        self.assertGreater(response_dict.get('Contract signed', {}).get('deals'), 0)
        self.assertEqual(2000, response_dict.get('Contract signed', {}).get('hectares'))

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_contract_farming_view(self):
        response = self.client.get(reverse('contract_farming_api'))
        self.assertEqual(200, response.status_code)
        response_dict = dict((d['name'], d) for d in response.data)
        self.assertGreater(response_dict.get('Contract signed', {}).get('deals'), 0)
        self.assertEqual(2000, response_dict.get('Contract signed', {}).get('hectares'))

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_implementation_status_list_view(self):
        response = self.client.get(reverse('implementation_status_api'))
        self.assertEqual(200, response.status_code)
        response_dict = dict((d['name'], d) for d in response.data)
        self.assertEqual(1, response_dict.get('Startup phase (no production)', {}).get('deals'))
        self.assertEqual(1000, response_dict.get('Startup phase (no production)', {}).get('hectares'))
        self.assertEqual(1, response_dict.get('In operation (production)', {}).get('deals'))
        self.assertEqual(1000, response_dict.get('In operation (production)', {}).get('hectares'))

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_investment_intention_list_view(self):
        response = self.client.get(reverse('intention'))
        self.assertEqual(200, response.status_code)
        response_dict = dict((d['name'], d) for d in response.data)
        #self.assertGreater(response_dict.get('Forest logging / management', {}).get('deals'), 0)
        #self.assertEqual(1000, response_dict.get('Forest logging / management', {}).get('hectares'))
        #self.assertEqual('Forestry', response_dict.get('Forest logging / management', {}).get('parent'))
        self.assertGreater(response_dict.get('Forest logging / management', {}).get('deals'), 0)
        self.assertEqual(1000, response_dict.get('Forest logging / management', {}).get('hectares'))
        self.assertEqual('Forestry', response_dict.get('Forest logging / management', {}).get('parent'))
        self.assertEqual(1, response_dict.get('Multiple intentions', {}).get('deals'))
        self.assertEqual(1000, response_dict.get('Multiple intentions', {}).get('hectares'))
        self.assertEqual('Other', response_dict.get('Multiple intentions', {}).get('parent'))

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_investment_intention_list_view_with_agriculture(self):
        data = QueryDict('intention=agriculture')
        response = self.client.get(reverse('intention'), data)
        self.assertEqual(200, response.status_code)
        response_dict = dict((d['name'], d) for d in response.data)
        self.assertEqual(1, response_dict.get('Multiple intentions', {}).get('deals'))
        self.assertEqual(1000, response_dict.get('Multiple intentions', {}).get('hectares'))
        self.assertEqual('Other', response_dict.get('Multiple intentions', {}).get('parent'))

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_investment_intention_list_view_with_forestry(self):
        data = QueryDict('intention=forestry')
        response = self.client.get(reverse('intention'), data)
        self.assertEqual(200, response.status_code)
        response_dict = dict((d['name'], d) for d in response.data)
        self.assertEqual(1, response_dict.get('Multiple intentions', {}).get('deals'))
        self.assertEqual(1000, response_dict.get('Multiple intentions', {}).get('hectares'))
        self.assertEqual('Other', response_dict.get('Multiple intentions', {}).get('parent'))

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_investor_country_summary_view(self):
        response = self.client.get(reverse('investor_country_summaries_api'))
        self.assertEqual(200, response.status_code)
        expected = [
            {'country': 'Cambodia',
             'country_id': '116',
             'country_slug': 'cambodia',
             'deals': 4,
             'domestic': 0,
             'lat': Decimal('12.565679000000'),
             'lat_max': Decimal('14.705078125000'),
             'lat_min': Decimal('10.411230468700'),
             'lon': Decimal('104.990963000000'),
             'lon_max': Decimal('107.605468750000'),
             'lon_min': Decimal('102.319726563000'),
             'name': 'Cambodia',
             'region': 'Asia',
             'region_slug': 'asia',
             'transnational': 4,
             'url': '/data/by-investor-country/cambodia/'}
        ]
        self.assertEqual(expected, response.data)

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_investor_countries_for_target_country_view(self):
        data = QueryDict('country_id=104')
        response = self.client.get(reverse('investor_countries_for_target_country_api'), data)
        self.assertEqual(200, response.status_code)
        expected = [
            {'country': 'Cambodia',
             'country_id': '116',
             'country_slug': 'cambodia',
             'deals': 4,
             'domestic': 0,
             'lat': Decimal('12.565679000000'),
             'lat_max': Decimal('14.705078125000'),
             'lat_min': Decimal('10.411230468700'),
             'lon': Decimal('104.990963000000'),
             'lon_max': Decimal('107.605468750000'),
             'lon_min': Decimal('102.319726563000'),
             'name': 'Cambodia',
             'region': 'Asia',
             'region_slug': 'asia',
             'transnational': 4,
             'url': '/data/by-investor-country/cambodia/'}
        ]
        self.assertEqual(expected, response.data)

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_target_country_summary_view(self):
        response = self.client.get(reverse('target_country_summaries_api'))
        self.assertEqual(200, response.status_code)
        expected = [
            {'country': 'Myanmar',
             'country_id': '104',
             'country_slug': 'myanmar',
             'deals': 4,
             'domestic': 0,
             'lat': Decimal('21.913965000000'),
             'lat_max': Decimal('28.517041015600'),
             'lat_min': Decimal('9.875390625000'),
             'lon': Decimal('95.956223000000'),
             'lon_max': Decimal('101.147265625000'),
             'lon_min': Decimal('92.179589843800'),
             'name': 'Myanmar',
             'region': 'Asia',
             'region_slug': 'asia',
             'transnational': 4,
             'url': '/data/by-target-country/myanmar/'}
        ]
        self.assertEqual(expected, response.data)

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_target_countries_for_investor_country_view_with_country(self):
        data = QueryDict('country=116')
        response = self.client.get(reverse('target_countries_for_investor_country_api'), data)
        self.assertEqual(200, response.status_code)
        expected = [
            {'country': 'Myanmar',
             'country_id': '104',
             'country_slug': 'myanmar',
             'deals': 4,
             'domestic': 0,
             'lat': Decimal('21.913965000000'),
             'lat_max': Decimal('28.517041015600'),
             'lat_min': Decimal('9.875390625000'),
             'lon': Decimal('95.956223000000'),
             'lon_max': Decimal('101.147265625000'),
             'lon_min': Decimal('92.179589843800'),
             'name': 'Myanmar',
             'region': 'Asia',
             'region_slug': 'asia',
             'transnational': 4,
             'url': '/data/by-target-country/myanmar/'}
        ]
        self.assertEqual(expected, response.data)

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_target_countries_for_investor_country_view_with_region(self):
        data = QueryDict('region=142')
        response = self.client.get(reverse('target_countries_for_investor_country_api'), data)
        self.assertEqual(200, response.status_code)
        expected = [
            {'country': 'Myanmar',
             'country_id': '104',
             'country_slug': 'myanmar',
             'deals': 4,
             'domestic': 0,
             'lat': Decimal('21.913965000000'),
             'lat_max': Decimal('28.517041015600'),
             'lat_min': Decimal('9.875390625000'),
             'lon': Decimal('95.956223000000'),
             'lon_max': Decimal('101.147265625000'),
             'lon_min': Decimal('92.179589843800'),
             'name': 'Myanmar',
             'region': 'Asia',
             'region_slug': 'asia',
             'transnational': 4,
             'url': '/data/by-target-country/myanmar/'}
        ]
        self.assertEqual(expected, response.data)

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_top_10_countries_view(self):
        response = self.client.get(reverse('top_10_countries_api'))
        self.assertEqual(200, response.status_code)
        investor_country = [
            {'id': '116', 'name': 'Cambodia', 'hectares': 3000.0, 'slug': 'cambodia', 'deals': 4}
        ]
        self.assertEqual(investor_country, response.data.get('investor_country'))
        target_country = [
            {'id': '104', 'name': 'Myanmar', 'hectares': 3000.0, 'slug': 'myanmar', 'deals': 4}
        ]
        self.assertEqual(target_country, response.data.get('target_country'))

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_transnational_deal_list_view(self):
        response = self.client.get(reverse('transnational_deals_api'))
        self.assertEqual(200, response.status_code)
        expected = [
            {
                'id': '104',
                'imports': ['142.Cambodia'],
                'name': '142.Myanmar',
                'size': 1,
                'slug': 'myanmar'
            },
            {
                 'id': '116',
                 'imports': [],
                 'name': '142.Cambodia',
                 'size': 1,
                 'slug': 'cambodia'}
        ]
        self.assertEqual(expected, response.data)

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_transnational_deal_list_view_with_region(self):
        data = QueryDict('region=142')
        response = self.client.get(reverse('transnational_deals_api'), data)
        self.assertEqual(200, response.status_code)
        expected = [
            {
                'id': '104',
                'imports': ['-1.Cambodia'],
                'name': '-1.Myanmar',
                'size': 1,
                'slug': 'myanmar'
            },
            {
                 'id': '116',
                 'imports': [],
                 'name': '-1.Cambodia',
                 'size': 1,
                 'slug': 'cambodia'}
        ]
        self.assertEqual(expected, response.data)

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_transnational_deals_by_country_view_with_target_country(self):
        response = self.client.get(reverse('transnational_deals_by_country_api'), data={'country': 104})
        self.assertEqual(200, response.status_code)
        target_country = [
            {'region_id': '142', 'slug': 'asia', 'region': 'Asia', 'hectares': 3000.0, 'deals': 4}
        ]
        self.assertEqual(target_country, response.data.get('target_country'))
        self.assertEqual([], response.data.get('investor_country'))

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_transnational_deals_by_country_view_with_investor_country(self):
        response = self.client.get(reverse('transnational_deals_by_country_api'), data={'country': 116})
        self.assertEqual(200, response.status_code)
        investor_country = [
            {'region_id': '142', 'slug': 'asia', 'region': 'Asia', 'hectares': 3000.0, 'deals': 4}
        ]
        self.assertEqual(investor_country, response.data.get('investor_country'))
        self.assertEqual([], response.data.get('target_country'))

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_transnational_deals_by_country_view_without_country(self):
        response = self.client.get(reverse('transnational_deals_by_country_api'))
        self.assertEqual(400, response.status_code)

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_hectares_view(self):
        response = self.client.get(reverse('hectares_api'))
        self.assertEqual(200, response.status_code)
        expected = {'deals': 4, 'hectares': 3000}
        self.assertEqual(expected, response.data)

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_agricultural_produce_list_view(self):
        response = self.client.get(reverse('agricultural_produce_api'))
        self.assertEqual(200, response.status_code)
        response_dict = dict((d['region'], d) for d in response.data)

        for region in Region.objects.all():
            self.assertIn(region.slug, response_dict.keys())

        self.assertEqual(2000.0, response_dict.get('asia', {}).get('available'))
        self.assertEqual(100, response_dict.get('asia', {}).get('agricultural_produce', {}).get('non_food'))
        self.assertEqual(2000.0, response_dict.get('asia', {}).get('hectares', {}).get('non_food'))

        self.assertEqual(2000.0, response_dict.get('overall', {}).get('available'))
        self.assertEqual(100, response_dict.get('overall', {}).get('agricultural_produce', {}).get('non_food'))
        self.assertEqual(2000.0, response_dict.get('overall', {}).get('hectares', {}).get('non_food'))

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_produce_info_view(self):
        response = self.client.get(reverse('produce_info_api'))
        self.assertEqual(200, response.status_code)
        crops = [
            {'name': 'Accacia', 'size': 2000},
            {'name': 'Alfalfa', 'size': 1000}
        ]
        self.assertEqual(crops, response.data.get('crops'))
        animals = [
            {'name': 'Aquaculture (animals)', 'size': 1000},
            {'name': 'Bees', 'size': 1000}
        ]
        self.assertEqual(animals, response.data.get('animals'))
        minerals = [
            {'name': 'Anthracite', 'size': 1000},
            {'name': 'Asphaltite', 'size': 1000}
        ]
        self.assertEqual(minerals, response.data.get('minerals'))
