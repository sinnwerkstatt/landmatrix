from django.test import TestCase
from django.urls import reverse

from apps.wagtailcms.models import RegionIndex, RegionPage


class RegionViewTestCase(TestCase):

    fixtures = [
        'countries_and_regions'
    ]

    def test_with_region_page(self):
        RegionPage.objects.create(title='Asia Page', slug='asia', region_id=142, path='/', depth=0)
        response = self.client.get(reverse('region', kwargs={'region_slug': 'asia'}))
        self.assertEqual(200, response.status_code)

    def test_with_index_page(self):
        RegionIndex.objects.create(title='Region index', slug='region', path='/', depth=0)
        response = self.client.get(reverse('region', kwargs={'region_slug': 'asia'}))
        self.assertEqual(200, response.status_code)

    def test_without_index_page(self):
        response = self.client.get(reverse('region', kwargs={'region_slug': 'asia'}))
        self.assertEqual(404, response.status_code)
