from django.contrib.gis.geos import Point
from django.test import TestCase

from apps.ol3_widgets.widgets import *


class BaseGeometryWidgetTestCase(TestCase):

    def setUp(self):
        self.widget = BaseGeometryWidget(attrs={'class': 'class'})
        self.widget.template_name = 'widgets/map.html'

    def test_init(self):
        keys = {'geom_type', 'map_srid', 'map_width', 'map_height', 'display_raw', 'class'}
        self.assertEqual(keys, set(self.widget.attrs.keys()))

    def test_serialize(self):
        self.assertEqual('POINT (0 1)', self.widget.serialize(GEOSGeometry('POINT(0 1)', srid=4326)))

    def test_deserialize(self):
        geometry = self.widget.deserialize('POINT(0 1)')
        self.assertIsInstance(geometry, Point)
        self.assertEqual('POINT (0 1)', geometry.wkt)

    def test_get_context(self):
        context = self.widget.get_context(name='name', value=GEOSGeometry('POINT(0 1)', srid=4326))
        keys = {'class', 'geom_type', 'map_srid', 'map_width', 'map_height', 'display_raw', 'name', 'module',
                'serialized', 'STATIC_URL', 'LANGUAGE_BIDI', 'id'}
        for key in keys:
            self.assertIn(key, context.keys())

    def test_get_context_with_different_srid(self):
        context = self.widget.get_context(name='name', value=GEOSGeometry('POINT(0 1)', srid=3857))
        self.assertEqual(4326, context.get('map_srid'))

    def test_render(self):
        output = self.widget.render(name='name', value=GEOSGeometry('POINT(0 1)', srid=4326))
        self.assertGreater(len(output), 0)


class OpenLayersWidgetTestCase(TestCase):

    def setUp(self):
        self.widget = OpenLayersWidget()
        self.widget.template_name = 'widgets/map.html'

    def test_serialize(self):
        expected = '{ "type": "Point", "coordinates": [ 0.0, 1.0 ] }'
        self.assertEqual(expected, self.widget.serialize(GEOSGeometry('POINT(0 1)', srid=4326)))


class OSMWidgetTestCase(TestCase):

    def setUp(self):
        self.widget = OSMWidget(attrs={'class': 'class'})
        self.widget.template_name = 'widgets/map.html'

    def test_init(self):
        keys = {'initial_center_lon', 'initial_center_lat', 'initial_zoom', 'class'}
        for key in keys:
            self.assertIn(key, self.widget.attrs.keys())


class SerializedMapWidgetTestCase(TestCase):

    def setUp(self):
        self.widget = SerializedMapWidget(attrs={'class': 'class'})

    def test_init(self):
        keys = {'initial_layer', 'show_controls', 'show_deals', 'disable_drawing',
                'show_layer_switcher', 'initial_point',
                'bound_location_field_id', 'bound_lat_field_id',
                'bound_lon_field_id', 'bound_level_of_accuracy_field_id',
                'bound_target_country_field_id', 'class'}
        for key in keys:
            self.assertIn(key, self.widget.attrs.keys())


class MapWidgetTestCase(TestCase):

    def setUp(self):
        self.widget = MapWidget()

    def test_serialize(self):
        self.assertEqual('', self.widget.serialize('value'))

    def test_deserialize(self):
        self.assertEqual('', self.widget.deserialize('value'))


class LocationWidgetTestCase(TestCase):

    def setUp(self):
        self.widget = LocationWidget(map_attrs={'class': 'class'})

    def test_init(self):
        self.assertEqual({'class': 'class'}, self.widget.map_attrs)

    def test_render(self):
        output = self.widget.render(name='name', value=GEOSGeometry('POINT(0 1)', srid=4326))
        self.assertGreater(len(output), 0)
