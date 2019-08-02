from django.contrib.gis.gdal.geomtype import OGRGeomType
from django.contrib.gis.geos import MultiPolygon
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, RequestFactory
from django.utils.datastructures import MultiValueDict

from grid.forms.deal_spatial_form import *
from landmatrix.models import HistoricalActivity


class DealSpatialFormTestCase(TestCase):

    fixtures = [
        'countries_and_regions',
        'users_and_groups',
        'status',
        'activities',
    ]

    def setUp(self):
        self.form_class = DealSpatialForm
        self.initial = {
            'level_of_accuracy': 'Country',
            'location': 'Rakhaing-Staat, Myanmar (Birma)',
            'location-map': 'Rakhaing-Staat, Myanmar (Birma)',
            'point_lat': 19.810093,
            'point_lon': 93.98784269999999,
            'target_country': 104,
        }
        file_names = ["shapefile.cpg", "shapefile.dbf", "shapefile.prj", "shapefile.qpj", "shapefile.shp", "shapefile.shx"]
        self.data = {
            'location-TOTAL_FORMS': 1,
            'location-INITIAL_FORMS': 0,
            'location-MIN_NUM_FORMS': 1,
            'location-MAX_NUM_FORMS': 1,
            'location-0-level_of_accuracy': 'Exact location',
            'location-0-location': 'Rakhaing-Staat, Myanmar (Birma)',
            'location-0-location-map': 'Rakhaing-Staat, Myanmar (Birma)',
            'location-0-point_lat': 19.810093,
            'location-0-point_lon': 93.98784269999999,
            'location-0-target_country': 104,
            'location-0-contract_area_0': '{"type":"MultiPolygon","coordinates":[[[[100.39024939321291,-84.99256181934545],[100.96173157476198,-84.99458605320528],[100.90757241033326,-85.02036131846661],[100.31534065984499,-85.02277461634935],[100.39024939321291,-84.99256181934545]]]]}',
            'location-0-contract_area_1': '',
            'location-0-intended_area_0': '',
            #'location-0-intended_area_1': file_names,
        }
        files = []
        for file_name in file_names:
            upload_file = open('landmatrix/fixtures/shapefiles/%s' % file_name, 'rb')
            files.append(SimpleUploadedFile(file_name, upload_file.read(), content_type="text/plain"))
        self.form = self.form_class(data=self.data, files=MultiValueDict({
            'location-0-intended_area_1': files,
        }), prefix='location-0')

    def test_init(self):
        self.assertIn('show_layer_switcher', self.form.fields['location'].widget.map_attrs.keys())

    def test_get_location_map_widget_attrs(self):
        attrs = self.form.get_location_map_widget_attrs()
        self.assertIn('bound_location_field_id', attrs.keys())
        self.assertIn('bound_target_country_field_id', attrs.keys())
        self.assertIn('bound_level_of_accuracy_field_id', attrs.keys())
        self.assertIn('bound_lat_field_id', attrs.keys())
        self.assertIn('bound_lon_field_id', attrs.keys())

    def test_get_default_lat_lon_attrs(self):
        attrs = self.form.get_default_lat_lon_attrs()
        self.assertEqual(93.98784269999999, attrs.get('initial_center_lon'))
        self.assertEqual(19.810093, attrs.get('initial_center_lat'))
        self.assertEqual([93.98784269999999, 19.810093], attrs.get('initial_point'))

    def test_clean_contract_area(self):
        self.assertEqual(True, self.form.is_valid())
        cleaned = self.form.clean_contract_area()
        self.assertEqual(4326, cleaned.srid)
        coords = (
            (
                (
                    (100.39024939321291, -84.99256181934545),
                    (100.96173157476198, -84.99458605320528),
                    (100.90757241033326, -85.02036131846661),
                    (100.31534065984499, -85.02277461634935),
                    (100.39024939321291, -84.99256181934545),
                ),
            ),
        )
        self.assertEqual(coords, cleaned.coords)

    def test_clean_intended_area(self):
        self.assertEqual(True, self.form.is_valid())
        self.assertIsInstance(self.form.clean_intended_area(), MultiPolygon)

    def test_clean_production_area(self):
        self.assertEqual(True, self.form.is_valid())
        self.assertEqual('', self.form.clean_production_area())

    def test_get_attributes(self):
        self.assertEqual(True, self.form.is_valid())
        attributes = self.form.get_attributes(request=RequestFactory())
        self.assertIsInstance(attributes['contract_area'].get('polygon'), MultiPolygon)

    def test_get_data(self):
        activity = HistoricalActivity.objects.get(id=10)
        data = self.form.get_data(activity)
        self.assertEqual('104', data.get('target_country'))

    def test_get_fields_display(self):
        form = self.form_class(initial=self.initial)
        fields_display = form.get_fields_display()
        fields_dict = dict((f['name'], f) for f in fields_display)
        self.assertEqual(True, fields_dict.get('point_lat').get('hidden'))
        self.assertEqual(True, fields_dict.get('point_lon').get('hidden'))


class PublicDealSpatialFormTestCase(TestCase):

    def setUp(self):
        self.initial = {
            'level_of_accuracy': 'Country',
            'location': 'Rakhaing-Staat, Myanmar (Birma)',
            'location-map': 'Rakhaing-Staat, Myanmar (Birma)',
            'point_lat': 19.810093,
            'point_lon': 93.98784269999999,
            'target_country': 104,
        }
        files = []
        self.form = PublicDealSpatialForm(initial=self.initial, prefix='location-0')

    def test_get_location_map_widget_attrs(self):
        attrs = self.form.get_location_map_widget_attrs()
        self.assertEqual(True, attrs.get('disable_drawing'))


class DealSpatialBaseFormSetTestCase(TestCase):

    fixtures = [
        'countries_and_regions',
        'users_and_groups',
        'status',
        'activities',
    ]

    def setUp(self):
        self.formset_class = formset_factory(DealSpatialForm, min_num=1, validate_min=True, extra=0,
                                             formset=DealSpatialBaseFormSet)
        self.initial = [
            {
                'level_of_accuracy': 'Country',
                'location': 'Rakhaing-Staat, Myanmar (Birma)',
                'location-map': 'Rakhaing-Staat, Myanmar (Birma)',
                'point_lat': 19.810093,
                'point_lon': 93.98784269999999,
                'target_country': 104,
            }
        ]
        self.data = {
            'location-TOTAL_FORMS': 1,
            'location-INITIAL_FORMS': 0,
            'location-MIN_NUM_FORMS': 1,
            'location-MAX_NUM_FORMS': 1,
            'location-0-level_of_accuracy': 'Exact location',
            'location-0-location': 'Rakhaing-Staat, Myanmar (Birma)',
            'location-0-location-map': 'Rakhaing-Staat, Myanmar (Birma)',
            'location-0-point_lat': 19.810093,
            'location-0-point_lon': 93.98784269999999,
            'location-0-target_country': 104,
        }
        self.formset = self.formset_class(data=self.data, prefix='location')

    def test_get_data(self):
        activity = HistoricalActivity.objects.get(id=10)
        data = self.formset.get_data(activity)
        self.assertIsInstance(data, (list, tuple))
        self.assertGreater(len(data), 0)
        self.assertEqual('104', data[0].get('target_country'))

    def test_get_attributes(self):
        self.assertEqual(True, self.formset.is_valid())
        attributes = self.formset.get_attributes(request=RequestFactory())
        self.assertIsInstance(attributes, (list, tuple))
        self.assertGreater(len(attributes), 0)
        self.assertEqual(104, attributes[0]['target_country'].get('value'))

    def test_meta(self):
        self.assertEqual(self.formset.Meta, self.formset.meta)
