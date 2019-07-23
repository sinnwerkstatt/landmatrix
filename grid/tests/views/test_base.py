from collections import OrderedDict

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.http import QueryDict
from django.test import TestCase, override_settings, RequestFactory

from api.elasticsearch import es_save
from grid.views.base import TableGroupView
from wagtailcms.models import WagtailRootPage


class TableGroupViewTestCase(TestCase):

    @classmethod
    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def setUpClass(cls):
        super().setUpClass()

        fixtures = [
            'countries_and_regions',
            'users_and_groups',
            'status',
            'crops',
            'animals',
            'minerals',
            'investors',
            'activities',
            'activity_involvements',
            'venture_involvements',
        ]
        for fixture in fixtures:
            call_command('loaddata', fixture)
        es_save.create_index(delete=True)
        es_save.index_activity_documents()
        es_save.index_investor_documents()
        es_save.refresh_index()

        WagtailRootPage.objects.create(title='Root', path='/', depth=0,
                                       data_introduction='Data introduction')

    def setUp(self):
        self.view = TableGroupView()
        self.view.group = 'all'
        self.view.request = RequestFactory()
        self.view.request.user = get_user_model().objects.get(username='reporter')
        self.view.request.GET = QueryDict('')
        self.view.request.session = {
            'deal:set_default_filters': False,
            'deal:filters': [],
            'deal:enabled_presets': [],
            'deal:disabled_presets': [],
        }

        self.deal_results = [
            {
                'activity_identifier': 1,
                'is_public': 'True',
                'deal_scope': 'transnational',
                'deal_size': 1000,
                'current_contract_size': 1000,
                'current_production_size': 0,
                'current_negotiation_status': 'Contract signed',
                'current_implementation_status': 'In operation (production)',
                'init_date': '2000',
                'top_investors': 'Test Investor 6#6#Cambodia',
                'intention': ['Mining'],
                'intention_attr': [
                    {'value': 'Mining', 'value2': None, 'date': None, 'is_current': False}
                ],
                'target_country': [104],
                'target_country_display': ['Myanmar'],
                'target_region': [142],
                'target_region_display': ['Asia']
            }
        ]
        self.group_results = [
            {
                'key': 'Myanmar',
                'doc_count': 3,
                'all': {
                    'buckets': [
                        {
                            'key': 'Myanmar',
                            'doc_count': 3
                        }
                    ]
                },
                'target_region_display': {
                    'buckets': [
                        {
                            'key': 'Asia',
                            'doc_count': 3
                        }
                    ]
                },
                'deal_size': {
                    'buckets': [
                        {
                            'key': 1000,
                            'doc_count': 3
                        }
                    ]
                },
                'intention': {
                    'buckets': [
                        {
                            'key': 'Mining',
                            'doc_count': 2
                        }
                    ]
                },
                'target_country': {
                    'buckets': [
                        {
                            'key': '104',
                            'doc_count': 3
                        }
                    ]
                }
            }
        ]

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_get_context_data(self):
        self.view.LOAD_MORE_AMOUNT = 1
        context_data = self.view.get_context_data(group='all')
        keys = {'view', 'data', 'name', 'columns', 'default_columns',
                'load_more', 'group_slug', 'group_value', 'group'}
        for key in keys:
            self.assertIn(key, context_data.keys())
        self.assertGreater(context_data.get('load_more'), 0)

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_get_records_with_all(self):
        results = self.view.get_records()
        self.assertIsInstance(results, (list, tuple))
        self.assertGreater(len(results), 0)
        self.assertIsInstance(results[0], dict)
        self.assertIn('activity_identifier', results[0].keys())

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_get_records_with_group(self):
        self.view.group = 'target_country'
        results = self.view.get_records()
        self.assertGreater(len(results), 0)
        self.assertIsInstance(results, (list, tuple))
        self.assertGreater(len(results), 0)
        self.assertIsInstance(results[0], dict)
        self.assertIn('target_country', results[0].keys())

    @override_settings(ELASTICSEARCH_INDEX_NAME='landmatrix_test')
    def test_get_records_with_group_value(self):
        self.view.group = 'investor_name'
        results = self.view.get_records()
        self.assertGreater(len(results), 0)
        self.assertIsInstance(results, (list, tuple))
        self.assertGreater(len(results), 0)
        self.assertIsInstance(results[0], dict)
        self.assertIn('key', results[0].keys())

    def test_get_group_value_query_with_country(self):
        self.view.group = 'target_country'
        self.view.group_value = 'myanmar'
        expected = {
            'bool': {
                'filter': [
                    {
                        'bool': {
                            'filter': {
                                'term': {
                                    'target_country': 104
                                }
                            }
                        }
                    }
                ]
            }
        }
        self.assertEqual(expected, self.view.get_group_value_query({}))

    def test_get_group_value_query_with_region(self):
        self.view.group = 'target_region'
        self.view.group_value = 'asia'
        expected = {
            'bool': {
                'filter': [
                    {
                        'bool': {
                            'filter': {
                                'term': {
                                    'target_region': 142
                                }
                            }
                        }
                    }
                ]
            }
        }
        self.assertEqual(expected, self.view.get_group_value_query({}))

    def test_get_group_value_query_with_crop(self):
        self.view.group = 'crop'
        self.view.group_value = 'accacia'
        expected = {
            'bool': {
                'filter': [
                    {
                        'bool': {
                            'filter': {
                                'term': {
                                    'crops': 1
                                }
                            }
                        }
                    }
                ]
            }
        }
        self.assertEqual(expected, self.view.get_group_value_query({}))

    def test_get_group_value_query_with_investor(self):
        self.view.group = 'investor_name'
        self.view.group_value = 'Test Investor #1'
        expected = {
            'bool': {
                'filter': [
                    {
                        'bool': {
                            'filter': {
                                'term': {
                                    'investor_id': 'Test Investor #1'
                                }
                            }
                        }
                    }
                ]
            }
        }
        self.assertEqual(expected, self.view.get_group_value_query({}))

    def test_get_group_aggs(self):
        query, aggs = self.view.get_group_aggs({})
        expected = {
            'bool': {
                'must_not': [
                    {
                        'term': {
                            'activity_identifier': ''
                        }
                    }
                ]
            }
        }
        self.assertEqual(expected, query)
        self.assertEqual({'all'}, set(aggs.keys()))
        self.assertEqual({'terms', 'aggs'}, set(aggs['all'].keys()))
        self.assertEqual({'all', 'target_country_display', 'top_investors', 'intention',
                          'current_implementation_status_display', 'current_negotiation_status_display', 'deal_size'},
                         set(aggs['all']['aggs'].keys()))

    def test_limit_query_with_target_country_and_group_value(self):
        self.view.group = 'target_country'
        self.view.group_value = '104'
        self.assertEqual(True, self.view.limit_query())

    def test_limit_query_with_target_region(self):
        self.view.group = 'target_region'
        self.assertEqual(False, self.view.limit_query())

    def test_limit_query_with_starts_with(self):
        self.view.request.GET = QueryDict('starts_with=50')
        self.assertEqual(False, self.view.limit_query())

    def test_get_columns_with_request(self):
        self.view.request.GET = QueryDict('columns=activity_identifier&columns=deal_size')
        self.assertEqual(['activity_identifier', 'deal_size'], self.view.get_columns())

    def test_get_columns_with_group_value(self):
        self.view.group = 'target_country'
        self.view.group_value = '104'
        self.assertEqual(set(self.view.COLUMN_GROUPS['all']), set(self.view.get_columns()))

    def test_get_columns_with_group(self):
        self.view.group = 'target_country'
        self.assertEqual(set(self.view.COLUMN_GROUPS['target_country']), set(self.view.get_columns()))

    def test_columns(self):
        keys = set(k.replace('_display', '') for k in self.view.COLUMN_GROUPS['all'])
        self.assertEqual(keys, set(self.view.columns))

    def test_get_columns_dict(self):
        columns = self.view.get_columns_dict()
        self.assertIsInstance(columns, OrderedDict)
        keys = set(k.replace('_display', '') for k in self.view.COLUMN_GROUPS['all'])
        self.assertEqual(keys, set(columns.keys()))
        order_dict = {
            'label': 'ID',
            'name': 'activity_identifier',
            'order_by': '-activity_identifier',
        }
        self.assertEqual(order_dict, columns.get('activity_identifier'))

    def test_get_columns_dict_with_group(self):
        self.view.group = 'target_country'
        columns = self.view.get_columns_dict()
        self.assertIsInstance(columns, OrderedDict)
        keys = set(k.replace('_display', '') for k in self.view.COLUMN_GROUPS['target_country'])
        self.assertEqual(keys, set(columns.keys()))
        order_dict = {
            'label': 'Target country',
            'name': 'target_country',
            'order_by': '-target_country',
        }
        self.assertEqual(order_dict, columns.get('target_country'))

    def test_get_field_label(self):
        field_label = self.view.get_field_label('activity_identifier')
        self.assertEqual('Deal ID', field_label)

    def test_columns_dict(self):
        self.assertIsInstance(self.view.columns_dict, dict)
        self.assertGreater(len(self.view.columns_dict), 0)

    def test_default_columns_dict(self):
        self.assertIsInstance(self.view.columns_dict, dict)
        self.assertGreater(len(self.view.columns_dict), 0)

    def test_get_items(self):
        items = self.view.get_items(self.deal_results)
        self.assertIsInstance(items, (list, tuple))
        self.assertGreater(len(items), 0)
        self.assertIsInstance(items[0], dict)
        self.assertIn('activity_identifier', items[0].keys())

    def test_get_items_with_group(self):
        self.view.group = 'target_country'
        items = self.view.get_items(self.group_results)
        self.assertIsInstance(items, (list, tuple))
        self.assertGreater(len(items), 0)
        self.assertIsInstance(items[0], dict)
        self.assertIn('target_country', items[0].keys())

    def test_get_deal_item(self):
        expected = OrderedDict([
            ('activity_identifier', [1]),
            ('target_country', ['Myanmar']),
            ('top_investors', [{'id': '6', 'name': 'Test Investor 6'}]),
            ('intention', [{'value': 'Mining', 'slug': 'Mining', 'order_by': 'Mining'}]),
            ('current_negotiation_status', [None]),
            ('current_implementation_status', [None]),
            ('deal_size', [1000])
        ])
        self.assertEqual(expected, self.view.get_deal_item(self.deal_results[0]))

    def test_get_group_item(self):
        self.view.group = 'target_country'
        expected = OrderedDict([
            ('target_country', {'display': 'Myanmar', 'value': '104'}),
            ('target_region', ['Asia']),
            ('intention', [{'value': 'Mining', 'slug': 'Mining', 'order_by': 'Mining'}]),
            ('deal_count', ['']),
            ('deal_size', [1000]),
            ('availability', [''])
        ])
        self.assertEqual(expected, self.view.get_group_item(self.group_results[0]))

    def test_get_order_by_field(self):
        self.assertEqual(['activity_identifier'], self.view.get_order_by_field())

    def test_get_order_by_field_with_request(self):
        self.view.request.GET = QueryDict('order_by=activity_identifier')
        self.assertEqual(['activity_identifier'], self.view.get_order_by_field())

    def test_get_order_by_field_with_group(self):
        self.view.group = 'target_country'
        self.assertEqual(['target_country'], self.view.get_order_by_field())

    def test_order_by(self):
        self.view.request.GET = QueryDict('order_by=activity_identifier')
        self.assertEqual({'activity_identifier': 'asc'}, self.view.order_by)

    def test_order_by_with_desc(self):
        self.view.request.GET = QueryDict('order_by=-activity_identifier')
        self.assertEqual({'activity_identifier': 'desc'}, self.view.order_by)

    def test_order_by_with_group(self):
        self.view.group = 'target_country'
        self.assertEqual({'_term': 'asc'}, self.view.order_by)

    def test_clean_parent_companies(self):
        value = 'Test investor 1#1|Test investor 2#2'
        self.assertEqual([{'id': '1', 'name': 'Test investor 1'},
                          {'id': '2', 'name': 'Test investor 2'}],
                         self.view.clean_parent_companies(value, {}))

    def test_clean_top_investors(self):
        value = 'Test investor 1#1|Test investor 2#2'
        self.assertEqual([{'id': '1', 'name': 'Test investor 1'},
                          {'id': '2', 'name': 'Test investor 2'}],
                         self.view.clean_top_investors(value, {}))

    def test_clean_intention_with_list(self):
        value = [
            'Mining',
            'Timber plantation',
            'Invalid',
        ]
        expected = [
            {
                'value': 'Mining',
                'slug': 'Mining',
                'order_by': 'Mining'
            },
            {
                'value': 'Timber plantation (for wood and fibre)',
                'slug': 'Timber%20plantation',
                'order_by': 'Timber plantation (for wood and fibre)'
            }
        ]
        self.assertEqual(expected, self.view.clean_intention(value, {}))

    def test_clean_intention_with_dict(self):
        value = {
            'value': 'Timber plantation'
        }
        self.assertEqual({
            'value': 'Timber%20plantation',
            'display': 'Timber plantation (for wood and fibre)',
            'is_parent': False,
        }, self.view.clean_intention(value, {}))

    def test_clean_intention_with_dict_parent(self):
        value = {
            'value': 'Agriculture'
        }
        intention = self.view.clean_intention(value, {})
        self.assertEqual(True, intention.get('is_parent'))

    def test_clean_crops_with_dict(self):
        crop = self.view.clean_crops({'value': '1'}, {})
        self.assertEqual({'value': 'Accacia', 'display': 'Accacia'}, crop)

    def test_clean_crops_with_list(self):
        crops = self.view.clean_crops(['1', '2'], {})
        self.assertEqual({'Accacia', 'Alfalfa'}, set(crops))

    def test_clean_crops_with_pk(self):
        crop = self.view.clean_crops('1', {})
        self.assertEqual('Accacia', crop)

    def test_clean_investor_name(self):
        value = {'value': '1'}
        result = {'key': '1'}
        investor_name = self.view.clean_investor_name(value, result)
        self.assertEqual(value, investor_name)

    def test_clean_investor_name_with_group_values(self):
        self.view.group_values = {
            '1': {
                'name': 'Test investor #1',
                'fk_country_display': 'Myanmar',
            }
        }
        value = {'value': '1'}
        investor_name = self.view.clean_investor_name(value, {'key': '1'})
        self.assertEqual('Test investor #1', investor_name)

        investor_name = self.view.clean_investor_name(value, {'key': '2'})
        self.assertEqual('', investor_name)

        self.view.group_values = None
        investor_name = self.view.clean_investor_name(value, {'key': '1'})
        self.assertEqual(value, investor_name)

    def test_clean_investor_country(self):
        self.view.group_values = {
            '1': {
                'name': 'Test investor #1',
                'fk_country_display': 'Myanmar',
            }
        }
        value = {'value': '1'}
        investor_name = self.view.clean_investor_country(value, {'key': '1'})
        self.assertEqual('Myanmar', investor_name)

        investor_name = self.view.clean_investor_country(value, {'key': '2'})
        self.assertEqual('', investor_name)

        self.view.group_values = None
        investor_name = self.view.clean_investor_country(value, {'key': '1'})
        self.assertEqual(value, investor_name)
