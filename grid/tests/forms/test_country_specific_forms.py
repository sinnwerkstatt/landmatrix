from django.test import TestCase

from grid.forms.country_specific_forms import *
from landmatrix.models import HistoricalActivity


class GridCountrySpecificFormsTestCase(TestCase):

    fixtures = [
        'countries_and_regions',
        'status',
    ]

    def test_get_country_specific_form_classes_with_country(self):
        activity = HistoricalActivity.objects.create()
        activity.attributes.create(name='target_country', value=496)
        form_classes = get_country_specific_form_classes(activity)
        self.assertEqual(1, len(form_classes))
        self.assertEqual(MongoliaForm, form_classes[0])

    def test_get_country_specific_form_classes_without_country(self):
        activity = HistoricalActivity.objects.create()
        form_classes = get_country_specific_form_classes(activity)
        self.assertEqual(0, len(form_classes))
