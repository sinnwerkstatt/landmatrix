from decimal import Decimal

from django.test import TestCase

from landmatrix.models import Region


class RegionTestCase(TestCase):

    fixtures = [
        'countries_and_regions',
    ]

    def setUp(self):
        self.region = Region.objects.get(slug='asia')

    def test_point_lon(self):
        self.assertEqual(Decimal('99.6679687500005'), self.region.point_lon)

    def test_point_lat(self):
        self.assertEqual(Decimal('47.947201040938'), self.region.point_lat)
