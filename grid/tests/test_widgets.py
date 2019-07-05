from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.gis.gdal.geometries import MultiPolygon
from django.contrib.gis.gdal.geomtype import OGRGeomType
from django.forms import Select, SelectMultiple, CheckboxInput, TextInput
from django.test import TestCase

from grid.widgets import *


class TitleWidgetTestCase(TestCase):

    def test(self):
        widget = TitleWidget(initial='initial')
        rendered = widget.render(name='name', value='value', attrs={})
        self.assertEqual('<h3>initial</h3>', rendered)


class YearBasedWidgetTestCase(TestCase):

    def setUp(self):
        self.widget = YearBasedWidget(help_text='help_text',
                                      attrs={'attr_key': 'attr_value'})

    def test_get_widgets(self):
        widgets = self.widget.get_widgets()
        self.assertEqual(3, len(widgets))
        self.assertEqual(self.widget.widget, widgets[0])
        self.assertIn('year-based', widgets[0].attrs['class'])
        self.assertIn('year-based-year', widgets[1].attrs['class'])
        self.assertIn('year-based-is-current', widgets[2].attrs['class'])

    def test_decompress_without_value(self):
        decompressed = self.widget.decompress('')
        self.assertEqual([None, None], decompressed)

    def test_decompress_with_value(self):
        decompressed = self.widget.decompress('value1:2000:1#value2:2001:')
        self.assertEqual(['value1', '2000', '1', 'value2', '2001', ''], decompressed)

    def test_format_output(self):
        output = self.widget.format_output(['1', '2', '3'])
        self.assertEqual('123', output)

    def test_get_multiple(self):
        self.assertEqual({False}, set(self.widget.get_multiple()))

    def test_value_from_datadict(self):
        data = {
            'name_0': 'value1',
            'name_1': '2000',
            'name_2': '1',
            'name_3': 'value2',
            'name_4': '2001'
        }
        value = self.widget.value_from_datadict(data, {}, 'name')
        self.assertEqual(6, len(value))
        self.assertEqual(6, len(self.widget.widgets))

    def test_render(self):
        value = ['value1', '2000', '1', 'value2', '2001', '']
        output = self.widget.render('name', value, attrs={})
        self.assertIn('value1', output)
        self.assertIn('2000', output)
        self.assertIn('value2', output)
        self.assertIn('2001', output)


class YearBasedTextInputTestCase(TestCase):

    def setUp(self):
        self.widget = YearBasedTextInput()

    def test_decompress_without_value(self):
        decompressed = self.widget.decompress('')
        self.assertEqual([None, None], decompressed)

    def test_decompress_with_value(self):
        decompressed = self.widget.decompress('value1:2000:1#value2:2001:')
        self.assertEqual(['value1', '2000', '1', 'value2', '2001', ''], decompressed)


class YearBasedSelectTestCase(TestCase):

    def test(self):
        widget = YearBasedSelect(choices=())
        self.assertIsInstance(widget.widget, Select)


class YearBasedSelectMultipleTestCase(TestCase):

    def test(self):
        widget = YearBasedSelectMultiple(choices=())
        self.assertIsInstance(widget.widget, SelectMultiple)


class YearBasedSelectMultipleNumberTestCase(TestCase):

    def test(self):
        widget = YearBasedSelectMultipleNumber(choices=(), attrs={'placeholder': 'placeholder'})
        widgets = widget.get_widgets()
        self.assertEqual(4, len(widgets))
        self.assertEqual('placeholder', widgets[1].attrs['placeholder'])


class TextChoiceInputTestCase(TestCase):

    def test(self):
        widget = TextChoiceInput(choices=())
        self.assertEqual(2, len(widget.get_widgets()))


class MultiTextInputTestCase(TestCase):

    def test(self):
        widget = MultiTextInput()
        widgets = widget.get_widgets()
        self.assertEqual(1, len(widgets))
        self.assertIsInstance(widgets[0], TextInput)


class PrimaryInvestorSelectTestCase(TestCase):

    def test(self):
        widget = PrimaryInvestorSelect()
        output = widget.render('name', 'value', attrs={})
        self.assertIn('class="btn change-investor"', output)
        self.assertIn('class="btn add-investor"', output)


class NumberInputTestCase(TestCase):

    def test(self):
        widget = NumberInput()
        output = widget.render('name', 'value', attrs={})
        self.assertIn('type="number"', output)
        self.assertIn('class="form-control"', output)


class FileInputWithInitialTestCase(TestCase):

    def setUp(self):
        self.widget = FileInputWithInitial()
        self.file = SimpleUploadedFile("file.pdf", b"", content_type="application/pdf")

    def test_render(self):
        output = self.widget.render('name', self.file, attrs={})
        self.assertIn('href="/media/uploads/file.pdf"', output)
        self.assertIn('<input type="file" name="name-new">', output)

    def test_value_from_datadict(self):
        files = {
            'file-new': self.file
        }
        value = self.widget.value_from_datadict({}, files, 'file')
        self.assertEqual(self.file, value)


class NestedCheckboxSelectMultipleTestCase(TestCase):

    def test(self):
        choices = (
            ('value1', 'label1', None),
            ('value2', 'label2', (
                ('value2.1', 'label2.1'),
                ('value2.2', 'label2.2'),
            )),
        )
        widget = NestedCheckboxSelectMultiple(choices=choices)
        output = widget.render('name', 'value', attrs={})
        self.assertIn('value1', output)
        self.assertIn('label2', output)
        self.assertIn('value2', output)
        self.assertIn('label2', output)
        self.assertIn('value2.1', output)
        self.assertIn('label2.1', output)
        self.assertIn('value2.2', output)
        self.assertIn('label2.2', output)


class CountrySelectTestCase(TestCase):

    fixtures = [
        'countries_and_regions'
    ]

    def test(self):
        choices = (
            (104, "Myanmar"),
        )
        widget = CountrySelect(choices=choices)
        output = widget.render('name', 'value', attrs={})
        self.assertIn('<option value="104" title="MM">', output)


class CommentInputTestCase(TestCase):

    def test(self):
        widget = CommentInput()
        output = widget.render('name', 'value', attrs={})
        self.assertIn('rows="3"', output)
        self.assertIn('class="form-control"', output)


class AreaWidgetTestCase(TestCase):

    def setUp(self):
        self.widget = AreaWidget(initially_hidden=True)
        self.data = MultiPolygon(OGRGeomType('MultiPolygon'))
        # '{"type":"MultiPolygon","coordinates":[[[[105.4458627008179,-77.06121616327937],[105.42558520066531,-77.15539340276317],[105.94018309342653,-77.15175800165704],[105.94533293473512,-77.03865854985577],[105.4458627008179,-77.06121616327937]]]]}"'
        file_names = ["shapefile.cpg", "shapefile.dbf", "shapefile.prj", "shapefile.qpj", "shapefile.shp", "shapefile.shx"]
        files = []
        for file_name in file_names:
            upload_file = open('landmatrix/fixtures/shapefiles/%s' % file_name, 'rb')
            files.append(SimpleUploadedFile(file_name, upload_file.read(), content_type="text/plain"))
        self.files = files

    def test_render(self):
        self.assertEqual(2, len(self.widget.widgets))
        output = self.widget.render('name', [self.data, self.files], attrs={})
        self.assertIn('class="map-serialized-data', output)
        self.assertIn('name="name_0"', output)
        self.assertIn('data-map-widget-options', output)
        self.assertIn('<input type="file" name="name_1" multiple>', output)

    def test_decompress(self):
        decompressed = self.widget.decompress(self.data)
        self.assertEqual([self.data, False], decompressed)

    def test_format_output(self):
        output = self.widget.format_output('name', ['1', '2'])
        self.assertIn('id="name-container"', output)
        self.assertIn('1', output)
        self.assertIn('2', output)


class InvestorSelectTestCase(TestCase):

    def test(self):
        choices = (
            ('10', 'Investor name #1'),
        )
        investor_identifiers = {
            '10': {
                'investor_identifier': '1'
            }
        }
        widget = InvestorSelect(choices=choices, data=investor_identifiers)
        output = widget.render('name', '10', attrs={})
        self.assertIn('<option value="10" selected data-investor_identifier="1">', output)
