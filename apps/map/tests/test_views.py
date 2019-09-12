from django.http import QueryDict
from django.test import RequestFactory, TestCase
from django.urls import reverse

from apps.map.views import MapSettingsMixin
from apps.wagtailcms.models import WagtailRootPage


class MapSettingsMixinTestCase(TestCase):

    def setUp(self):
        self.mixin = MapSettingsMixin()

    def test_get_legend(self):
        legend = self.mixin.get_legend()
        self.assertEqual({'implementation', 'intention', 'level_of_accuracy'}, set(legend.keys()))

    def test_get_polygon_layers(self):
        layers = self.mixin.get_polygon_layers()
        self.assertEqual({'contract_area', 'intended_area', 'production_area'}, set(layers.keys()))


class MapViewTestCase(TestCase):

    fixtures = [
        'countries_and_regions',
        'users_and_groups',
    ]

    def setUp(self):
        self.factory = RequestFactory()
        WagtailRootPage.objects.create(title='Root', path='/', depth=0,
                                       map_introduction='Map introduction')

    def test(self):
        response = self.client.get(reverse('map'))
        self.assertEqual(200, response.status_code)
        self.assertEqual('Map introduction', response.context.get('introduction'))

    def test_with_country(self):
        data = QueryDict('country=104')
        response = self.client.get(reverse('map'), data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(True, response.context.get('is_country'))
        self.assertEqual(104, response.context.get('map_object').id)

    def test_with_region(self):
        data = QueryDict('region=142')
        response = self.client.get(reverse('map'), data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(142, response.context.get('map_object').id)
