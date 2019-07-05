from collections import OrderedDict

from django.test import TestCase, RequestFactory
from django.urls import reverse

from api.views.filter_views import *
from landmatrix.models import FilterPreset


class FilterDocTypeMixinTestCase(TestCase):

    def test_dispatch(self):
        request = RequestFactory()
        request.method = 'OPTIONS'
        request.path = '/'
        mixin = FilterDocTypeMixin()
        response = mixin.dispatch(request, doc_type='investor')
        self.assertEqual('investor', mixin.doc_type)


class FilterCreateViewTestCase(TestCase):

    fixtures = [
        'filters'
    ]

    def test(self):
        data = {
            'variable': 'activity_identifier',
            'operator': 'is',
            'value': '1'
        }
        response = self.client.post(reverse('api_filter_create', kwargs={'doc_type': 'deal'}), data=data)
        self.assertEqual(200, response.status_code)
        stored_filters = self.client.session.get('deal:filters')
        new_filter = list(stored_filters.values())[0]
        self.assertEqual('activity_identifier', new_filter.get('variable'))
        self.assertEqual('is', new_filter.get('operator'))
        self.assertEqual('1', new_filter.get('value'))
        self.assertEqual('Deal ID', new_filter.get('label'))


class FilterDeleteViewTestCase(TestCase):

    def test(self):
        custom_filter = {'name': 'custom_filter', 'variable': 'activity_identifier', 'operator': 'is', 'value': '1',
                         'label': 'Deal ID', 'key': None, 'display_value': '1'}
        session = self.client.session
        session['deal:filters'] = {'custom_filter': custom_filter}
        session.save()
        data = {
            'name': 'custom_filter'
        }
        response = self.client.post(reverse('api_filter_delete', kwargs={'doc_type': 'deal'}), data=data)
        self.assertEqual(200, response.status_code)
        stored_filters = self.client.session.get('deal:filters')
        self.assertEqual({}, stored_filters)


class SetDefaultFiltersViewTestCase(TestCase):

    fixtures = [
        'filters'
    ]

    def test(self):
        data = {
            'set_default_filters': '1'
        }
        response = self.client.post(reverse('api_filter_set_default_filters', kwargs={'doc_type': 'deal'}), data=data)
        set_default_filters = self.client.session.get('deal:set_default_filters')
        self.assertEqual(True, set_default_filters)


class FilterListViewTestCase(TestCase):

    def test(self):
        custom_filter = {'name': 'custom_filter', 'variable': 'activity_identifier', 'operator': 'is', 'value': '1',
                         'label': 'Deal ID', 'key': None, 'display_value': '1'}
        session = self.client.session
        session['deal:filters'] = {'custom_filter': custom_filter}
        session.save()
        response = self.client.get(reverse('api_filter_list', kwargs={'doc_type': 'deal'}))
        self.assertEqual(200, response.status_code)
        self.assertEqual({'custom_filter': custom_filter}, response.data)


class FilterClearViewTestCase(TestCase):

    def test(self):
        custom_filter = {'name': 'custom_filter', 'variable': 'activity_identifier', 'operator': 'is', 'value': '1',
                         'label': 'Deal ID', 'key': None, 'display_value': '1'}
        session = self.client.session
        session['deal:filters'] = {'custom_filter': custom_filter}
        session.save()
        response = self.client.get(reverse('api_filter_clear', kwargs={'doc_type': 'deal'}))
        stored_filters = self.client.session.get('deal:filters')
        self.assertEqual({}, stored_filters)


class FilterPresetViewTestCase(TestCase):

    fixtures = [
        'filters'
    ]

    def test(self):
        response = self.client.get(reverse('api_filter_preset', kwargs={'doc_type': 'deal'}))
        self.assertEqual(200, response.status_code)
        response_dict = dict((d['name'], d) for d in response.data)
        for preset in FilterPreset.objects.all():
            self.assertIn(preset.name, response_dict.keys())
            self.assertEqual(preset.id, response_dict[preset.name]['id'])
            self.assertEqual(preset.is_hidden, response_dict[preset.name]['is_hidden'])
