from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from grid.fields import *
from grid.forms.choices import actor_choices
from landmatrix.models import HistoricalActivityAttribute


class YearBasedFieldTestCaseMixin:

    field_class = YearBasedIntegerField
    field = None
    data_list = ['value1', '2000', '1', 'value2', '2001', '']
    data_cleaned = 'value1:2000:True#value2:2001:False'
    data_compressed = 'value1:2000:1#value2:2001:False'
    data_count = 6

    def setUp(self):
        self.field = self.get_field()

    def get_field(self):
        return self.field_class(**self.get_field_kwargs())

    def get_field_kwargs(self):
        return {
            'help_text': 'help_text',
            'required': False
        }

    def test_clean(self):
        cleaned = self.field.clean(self.data_list)
        self.assertEqual(self.data_count, len(self.field.fields))
        self.assertEqual(self.data_cleaned, cleaned)

    def test_compress_with_value(self):
        value = self.field.compress(self.data_list)
        self.assertEqual(self.data_compressed, value)

    def test_compress_without_value(self):
        value = self.field.compress([])
        self.assertEqual('', value)


class YearBasedIntegerFieldTestCase(YearBasedFieldTestCaseMixin,
                                    TestCase):

    field_class = YearBasedIntegerField
    data_list = ['1', '2000', '1', '2', '2001', '']
    data_cleaned = '1:2000:True#2:2001:'
    data_compressed = '1:2000:1#2:2001:'


class YearBasedFloatFieldTestCase(YearBasedFieldTestCaseMixin,
                                  TestCase):

    field_class = YearBasedFloatField
    data_list = ['1.0', '2000', '1', '2.0', '2001', '']
    data_cleaned = '1.0:2000:True#2.0:2001:'
    data_compressed = '1.0:2000:1#2.0:2001:'


class YearBasedChoiceFieldTestCase(YearBasedFieldTestCaseMixin,
                                   TestCase):

    field_class = YearBasedChoiceField
    data_list = ['value1', '2000', '1', 'value2', '2001', '']
    data_cleaned = 'value1:2000:True#value2:2001:'
    data_compressed = 'value1:2000:1#value2:2001:'

    def get_field(self):
        choices = (
            ('value1', 'label1'),
            ('value2', 'label2'),
        )
        return self.field_class(choices=choices, help_text='help_text', required=False)


class YearBasedModelMultipleChoiceIntegerFieldTestCase(YearBasedFieldTestCaseMixin,
                                                       TestCase):

    fixtures = [
        'countries_and_regions'
    ]

    field_class = YearBasedModelMultipleChoiceIntegerField
    data_list = [['104', '116'], '1000', '2000', '1', ['4', '8'], '2000', '2001', '']
    data_cleaned = '<QuerySet [<Country: Cambodia>, <Country: Myanmar>]>:1000:2000:True#' \
                   '<QuerySet [<Country: Afghanistan>, <Country: Albania>]>:2000:2001:'
    data_compressed = "['104', '116']:1000:2000:1#['4', '8']:2000:2001:"
    data_count = 8

    def setUp(self):
        super().setUp()

    def get_field_kwargs(self):
        return {
            'queryset': Country.objects.all(),
            'required': False
        }

    def test_init_with_placeholder(self):
        field = self.field_class(**self.get_field_kwargs(), placeholder='placeholder')
        self.assertEqual('placeholder', field.placeholder)

    def test_init_with_empty_placeholder(self):
        field = self.field_class(**self.get_field_kwargs(), placeholder='')
        self.assertEqual('', field.placeholder)


class YearBasedMultipleChoiceIntegerFieldTestCase(YearBasedFieldTestCaseMixin,
                                                  TestCase):

    field_class = YearBasedMultipleChoiceIntegerField
    data_list = [['value1', 'value2'], '1000', '2000', '1', ['value3', 'value4'], '2000', '2001', '']
    data_cleaned = "['value1', 'value2']:1000:2000:True#['value3', 'value4']:2000:2001:"
    data_compressed = "['value1', 'value2']:1000:2000:1#['value3', 'value4']:2000:2001:"
    data_count = 8

    def get_field_kwargs(self):
        choices = (
            ('value1', 'label1'),
            ('value2', 'label2'),
            ('value3', 'label3'),
            ('value4', 'label4'),
        )
        return {
            'choices': choices,
            'required': False
        }


class MultiCharFieldTestCase(YearBasedFieldTestCaseMixin,
                             TestCase):

    field_class = MultiCharField
    data_list = ['value1', 'value2', 'value3']
    data_cleaned = 'value1#value2#value3'
    data_compressed = data_cleaned
    data_count = 3


class UserModelChoiceFieldTestCase(TestCase):

    fixtures = [
        'countries_and_regions',
        'users_and_groups',
    ]

    def test(self):
        users = get_user_model().objects.all()
        field = UserModelChoiceField(queryset=users)
        label = field.label_from_instance(users.get(username='reporter'))
        self.assertEqual('Reporter Reporter', label)


class TitleFieldTestCase(TestCase):

    def test(self):
        field = TitleField(initial='initial')
        self.assertEqual(True, field.is_title)


class NestedMultipleChoiceFieldTestCase(TestCase):

    def setUp(self):
        choices = (
            ('value1', 'label1', None),
            ('value2', 'label2', (
                ('value2.1', 'label2.1'),
                ('value2.1', 'label2.2'),
            )),
        )
        self.field = NestedMultipleChoiceField(choices=choices)

    def test_valid_value(self):
        self.assertTrue(self.field.valid_value('value1'))
        self.assertTrue(self.field.valid_value('value2.1'))

    def test_get_value(self):
        self.assertEqual('label1', self.field.get_value('value1'))
        self.assertEqual('label2.1', self.field.get_value('value2.1'))


class FileFieldWithInitialTestCase(TestCase):

    def test_validate(self):
        file = SimpleUploadedFile("file.pdf", b"", content_type="application/pdf")
        field = FileFieldWithInitial()
        file.size = 20000000
        with self.assertRaises(ValidationError):
            field.validate(file)


class CountryFieldTestCase(TestCase):

    fixtures = [
        'countries_and_regions'
    ]

    def test(self):
        field = CountryField()
        self.assertEqual(71, field.queryset.count())


class ActorsFieldTestCase(YearBasedFieldTestCaseMixin,
                          TestCase):

    field_class = ActorsField
    data_list = ['value1', 'Government / State institutions', 'value2', 'Traditional land-owners / communities']
    data_cleaned = 'value1:Government / State institutions#value2:Traditional land-owners / communities'
    data_compressed = data_cleaned
    data_count = 4

    def get_field(self):
        return self.field_class(choices=actor_choices, required=False)


class AreaFieldTestCase(TestCase):

    def setUp(self):
        self.field = AreaField()

    def test_compress(self):
        file = SimpleUploadedFile("file.pdf", b"", content_type="application/pdf")
        self.assertEqual('test', self.field.compress(['test', None]))
        self.assertEqual(file, self.field.compress(['test', file]))
        self.assertEqual('', self.field.compress([]))

    def test_clean(self):
        value = ['{"type":"MultiPolygon","coordinates":[[[[100.39024939321291,-84.99256181934545],[100.96173157476198,-84.99458605320528],[100.90757241033326,-85.02036131846661],[100.31534065984499,-85.02277461634935],[100.39024939321291,-84.99256181934545]]]]}']
        cleaned = self.field.clean(value)
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
