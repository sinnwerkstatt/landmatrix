__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from global_app.views.view_aux_functions import create_condition_formset
from global_app.views.browse_filter_conditions import BrowseFilterConditions

from django.test import TestCase
from django.http import QueryDict
from django.utils.datastructures import MultiValueDict

class TestViewAuxFunctions(TestCase):

    default_formset_args = QueryDict('form-TOTAL_FORMS=1&form-INITIAL_FORMS=0&form-MAX_NUM_FORMS=')
    actual_formset_args = MultiValueDict({
        'conditions_empty-0-operator': ['in'], 'conditions_empty-1-operator': ['is'],
        'conditions_empty-MAX_NUM_FORMS': [''], 'conditions_empty-0-value': ['30', '40'],
        'conditions_empty-1-variable': ['-2'], 'conditions_empty-0-variable': ['5233'],
        'conditions_empty-TOTAL_FORMS': [2], 'conditions_empty-1-value': ['20'],
        'conditions_empty-INITIAL_FORMS': [2]
    })

    def setUp(self):
        self.debug_browse = BrowseFilterConditions.DEBUG
        self.Formset = create_condition_formset()

    def tearDown(self):
        BrowseFilterConditions.DEBUG = self.debug_browse

    def test_formset(self):
        self.assertFalse(self.Formset().is_valid())
        self.assertTrue(self.Formset(self.default_formset_args).is_valid())

    def test_parse_whatever(self):
        self._assert_has_required_keys(BrowseFilterConditions(self.Formset()).parse())
        filters = BrowseFilterConditions(self.Formset(self.default_formset_args)).parse()

    def test_parse_order_by(self):
        ORDER = 'blah'
        self.assertIn(ORDER, BrowseFilterConditions(self.Formset(), ['blah']).parse()['order_by'])

    def test_with_actual_data(self):
        formset = self.Formset(self.actual_formset_args, prefix="conditions_empty")
        try:
            BrowseFilterConditions(formset, ['deal_id']).parse()
        except NameError:
            self.fail('parse() not yet fully implemented')

    def _assert_has_required_keys(self, filter_conditions):
        self.assertEqual({'order_by', 'limit', 'investor', 'activity', 'deal_scope'}, set(filter_conditions))