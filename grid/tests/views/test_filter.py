import json

from django.contrib.auth import get_user_model
from django.http import QueryDict
from django.test import TestCase, RequestFactory
from django.urls import reverse
from rest_framework.response import Response

from grid.views.filter import *


class FilterWidgetAjaxViewTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def get_result_dict(self, params, doc_type='deal'):
        request = self.factory.get(reverse('ajax_widget', kwargs={'doc_type': doc_type}))
        request.GET = QueryDict(params)
        response = FilterWidgetAjaxView.as_view()(request, doc_type=doc_type)
        response = response.render()
        return json.loads(response.content)

    def test_with_activity_identifier(self):
        result = self.get_result_dict('key_id=activity_identifier&name=value&operation=is&value=1')
        self.assertEqual(['lt', 'gt', 'gte', 'lte', 'is', 'is_empty'], result.get('allowed_operations'))
        widget = '<input type="number" name="value" value="1" id="id_value" class="valuefield form-control">'
        self.assertEqual(widget, result.get('widget'))

    def test_with_deal_count(self):
        result = self.get_result_dict('key_id=deal_count&name=value&operation=is&value=1', doc_type='investor')
        self.assertEqual(['lt', 'gt', 'gte', 'lte', 'is', 'is_empty'], result.get('allowed_operations'))
        widget = '<input type="number" name="value" value="1" id="id_value" class="valuefield form-control">'
        self.assertEqual(widget, result.get('widget'))

    def test_with_multi_value_field(self):
        result = self.get_result_dict('key_id=intention&name=value&operation=is&value=1')
        self.assertEqual(['is', 'not_in', 'in', 'is_empty'], result.get('allowed_operations'))
        self.assertIn('<select name="value" id="id_value" class="valuefield form-control">', result.get('widget'))

    def test_with_date_field(self):
        result = self.get_result_dict('key_id=updated_date&name=value&operation=gte&value=2000-01-01')
        self.assertEqual(['lt', 'gt', 'gte', 'lte', 'is', 'is_empty'], result.get('allowed_operations'))
        widget = '<input class="form-control" id="id_value" name="value" type="text" value="2000-01-01"/>'
        self.assertIn(widget, result.get('widget'))

    def test_without_boolean_field(self):
        result = self.get_result_dict('key_id=file_not_public&name=value&operation=is&value=')
        self.assertEqual(['is', 'is_empty'], result.get('allowed_operations'))
        widget = '<select name="value" id="id_value" class="valuefield form-control">\n  ' \
                 '<option value="True" selected>Yes</option>\n\n  <option value="False">No</option>\n\n</select>'
        self.assertEqual(widget, result.get('widget'))

    def test_without_field(self):
        result = self.get_result_dict('key_id=&name=value&operation=is&value=1')
        self.assertEqual(['contains', 'is', 'is_empty'], result.get('allowed_operations'))
        widget = '<input type="text" name="value" value="1" id="id_value">'
        self.assertEqual(widget, result.get('widget'))


class FilterWidgetMixinTestCase(TestCase):

    fixtures = [
        'countries_and_regions',
        'users_and_groups',
        'filters',
    ]

    def setUp(self):
        self.mixin = FilterWidgetMixin()
        self.mixin.request = RequestFactory()
        self.mixin.request.user = get_user_model().objects.get(username='reporter')
        self.mixin.request.GET = QueryDict('status=1&status=2&status=3')
        self.mixin.request.session = {
            'deal:set_default_filters': False,
            'deal:filters': [],
            'deal:enabled_presets': [],
            'deal:disabled_presets': [],
        }

    def test_get_context_data(self):
        context = self.mixin.get_context_data()
        self.assertIsInstance(context, dict)
        expected = {'variables', 'presets', 'set_default_filters', 'status'}
        self.assertEqual(expected, set(context.keys()))

    def test_set_country_region_filter_with_deal_and_country(self):
        # Test with filter already set
        self.mixin.request.session['deal:filters'] = {
            'country': {
                'name': 'country',
                'variable': 'country',
                'operator': 'is',
                'value': '104',
                'label': 'Country',
                'key': None,
                'display_value': 'Myanmar'
            }
        }
        self.mixin.set_country_region_filter({'country': 104})
        expected = {
            'country': {
                'name': 'country',
                'variable': 'target_country',
                'operator': 'is',
                'value': 104,
                'label': 'Target country',
                'key': None,
                'display_value': 'Myanmar'
            }
        }
        self.assertEqual(expected, self.mixin.request.session.get('deal:filters'))

    def test_set_country_region_filter_with_deal_and_region(self):
        self.mixin.set_country_region_filter({'region': 142})
        expected = {
            'region': {
                'name': 'region',
                'variable': 'target_region',
                'operator': 'is', 'value': 142,
                'label': 'Target region',
                'key': None,
                'display_value': 'Asia'
            }
        }
        self.assertEqual(expected, self.mixin.request.session.get('deal:filters'))

    def test_set_country_region_filter_with_investor_and_country(self):
        self.mixin.doc_type = 'investor'
        # Test with filter already set
        self.mixin.request.session['investor:filters'] = {
            'country': {
                'name': 'country',
                'variable': 'fk_country',
                'operator': 'is',
                'value': '104',
                'label': 'Country of registration/origin',
                'key': None,
                'display_value': 'Myanmar'
            }
        }
        self.mixin.set_country_region_filter({'country': 104})
        expected = {
            'country': {
                'name': 'country',
                'variable': 'fk_country',
                'operator': 'is',
                'value': 104,
                'label': 'Country of registration/origin',
                'key': None,
                'display_value': 'Myanmar'
            }
        }
        self.assertEqual(expected, self.mixin.request.session.get('investor:filters'))

    def test_set_country_region_filter_with_investor_and_region(self):
        self.mixin.doc_type = 'investor'
        self.mixin.set_country_region_filter({'region': 142})
        expected = {
            'region': {
                'name': 'region',
                'variable': 'region',
                'operator': 'is', 'value': 142,
                'label': 'Region of registration/origin',
                'key': None,
                'display_value': 'Asia'
            }
        }
        self.assertEqual(expected, self.mixin.request.session.get('investor:filters'))

    def test_remove_country_region_filter(self):
        self.mixin.request.session['deal:filters'] = {
            'custom_filter': {
                'name': 'custom_filter',
                'variable': 'activity_identifier',
                'operator': 'is',
                'value': '1',
                'label': 'Deal ID',
                'key': None,
                'display_value': '1'
            },
            'country': {
                'name': 'country',
                'variable': 'country',
                'operator': 'is',
                'value': '104',
                'label': 'Country',
                'key': None,
                'display_value': 'Myanmar'
            },
            'region': {
                'name': 'region',
                'variable': 'region',
                'operator': 'is',
                'value': '142',
                'label': 'Region',
                'key': None,
                'display_value': 'Asia'
            },
        }
        self.mixin.remove_country_region_filter()
        self.assertEqual({'custom_filter'}, set(self.mixin.request.session.get('deal:filters').keys()))

    def test_set_default_filters_global(self):
        self.mixin.request.session['deal:set_default_filters'] = True
        # Test with some presets already set
        self.mixin.request.session['deal:filters'] = {
            'default_preset_1': {
                'name': 'default_preset_1',
                'preset_id': 1,
                'label': 'Exclude Mining',
                'hidden': False,
            },
        }
        # Test with conflicting presets, enable one of the default filters
        self.mixin.set_default_filters({}, disabled_presets=[10, 4], enabled_presets=[1, 3, 4])
        expected = {'default_preset_1', 'default_preset_2', 'default_preset_3', 'default_preset_11',
                    'default_preset_12', 'default_preset_15', 'default_preset_16', 'default_preset_19'}
        self.assertEqual(expected, set(self.mixin.request.session.get('deal:filters').keys()))

    def test_set_default_filters_country(self):
        self.mixin.request.session['deal:set_default_filters'] = True
        # Test with some presets already set
        self.mixin.request.session['deal:filters'] = {
            'default_preset_1': {
                'name': 'default_preset_1',
                'preset_id': 1,
                'label': 'Exclude Mining',
                'hidden': False,
            },
            'country': {
                'name': 'country',
                'variable': 'country',
                'operator': 'is',
                'value': '104',
                'label': 'Country',
                'key': None,
                'display_value': 'Myanmar'
            },
        }
        self.mixin.disabled_presets = [10]
        # Enable one of the default filters
        self.mixin.enabled_presets = [2, 3]
        self.mixin.set_default_filters({})
        expected = {'country', 'default_preset_2', 'default_preset_3'}
        self.assertEqual(expected, set(self.mixin.request.session.get('deal:filters').keys()))

    def test_remove_default_filters(self):
        self.mixin.request.session['deal:filters'] = {
            'custom_filter': {
                'name': 'custom_filter',
                'variable': 'activity_identifier',
                'operator': 'is',
                'value': '1',
                'label': 'Deal ID',
                'key': None,
                'display_value': '1'
            },
            'default_preset_1': {
                'name': 'default_preset_1',
                'preset_id': 1,
                'label': 'Exclude Mining',
                'hidden': False,
            },
        }
        self.mixin.remove_default_filters()
        self.assertEqual({'custom_filter'}, set(self.mixin.request.session.get('deal:filters').keys()))

    def test_status(self):
        self.assertEqual({'1', '2', '3'}, set(self.mixin.status))


class GridFilterTestCase(TestCase):

    def test_get_activity_variable_table(self):
        variables = get_activity_variable_table()
        self.assertIsInstance(variables, dict)
        self.assertEqual(48, len(variables.keys()))

    def test_get_investor_variable_table(self):
        variables = get_investor_variable_table()
        self.assertIsInstance(variables, dict)
        self.assertEqual(3, len(variables.keys()))
