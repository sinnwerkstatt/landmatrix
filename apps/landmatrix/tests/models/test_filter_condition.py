from django.test import TestCase

from apps.api.filters import Filter
from apps.landmatrix.models import FilterCondition, FilterPreset


class FilterConditionTestCase(TestCase):

    def setUp(self):
        self.preset = FilterPreset.objects.create(name='Test preset')
        self.condition = FilterCondition.objects.create(fk_rule=self.preset,
                                                        variable='variable',
                                                        key='value',
                                                        operator='is',
                                                        value='value')

    def test_to_filter(self):
        api_filter = self.condition.to_filter()
        self.assertIsInstance(api_filter, Filter)

    def test_parsed_value_with_comma(self):
        self.condition.value = 'value1, value2'
        self.assertEqual(['value1', 'value2'], self.condition.parsed_value)
