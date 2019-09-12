from django.test import TestCase
from django.urls import reverse

from apps.wagtailcms.models import CountryIndex, CountryPage


class CountryViewTestCase(TestCase):

    fixtures = [
        'countries_and_regions'
    ]

    def test_with_country_page(self):
        CountryPage.objects.create(title='Myanmar Page', slug='myanmar', country_id=104, path='/', depth=0)
        response = self.client.get(reverse('country', kwargs={'country_slug': 'myanmar'}))
        self.assertEqual(200, response.status_code)

    def test_with_index_page(self):
        CountryIndex.objects.create(title='Country index', slug='country', path='/', depth=0)
        response = self.client.get(reverse('country', kwargs={'country_slug': 'myanmar'}))
        self.assertEqual(200, response.status_code)

    def test_without_index_page(self):
        response = self.client.get(reverse('country', kwargs={'country_slug': 'myanmar'}))
        self.assertEqual(404, response.status_code)
