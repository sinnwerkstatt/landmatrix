from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase

from apps.api.filters import *


class FiltersTestCase(TestCase):

    fixtures = [
        'filters',
        'countries_and_regions',
        'users_and_groups',
    ]

    def setUp(self):
        pass

    def test_get_elasticsearch_match_operation(self):
        operators = FILTER_OPERATION_MAP.keys()
        for operator in operators:
            match_op = get_elasticsearch_match_operation(operator, 'key', 'value')
            self.assertIsInstance(match_op, (tuple, list))
            self.assertEqual(len(match_op), 2)
            self.assertIn(match_op[0], ('must', 'must_not', 'should'))
            self.assertIsInstance(match_op[1], dict)

    def test_load_statuses_from_url(self):
        status_tests = (
            (
                AnonymousUser(),
                (2, 3)
            ), (
                User.objects.get(username='administrator'),
                (2, 3)
            ), (
                User.objects.get(username='administrator-staff'),
                (1, 2, 3, 4, 5, 6)
            )
        )
        for status_test in status_tests:
            request = RequestFactory()
            request.user = status_test[0]
            request.GET = QueryDict('status=1&status=2&status=3&status=4&status=5&status=6')
            statuses = load_statuses_from_url(request)
            self.assertEqual(set(status_test[1]), set(statuses),
                             msg=f"Wrong statuses for user {status_test[0]}")

    def test_load_statuses_without_get_param(self):
        request = RequestFactory()
        request.user = User.objects.get(username='reporter'),
        request.GET = QueryDict('')
        statuses = load_statuses_from_url(request)
        self.assertEqual({2, 3}, set(statuses))

    def test_clean_filter_query_string(self):
        request = RequestFactory()
        request.GET = QueryDict('key1=value1&key2=value1&key2=value2')
        whitelist = clean_filter_query_string(request)
        self.assertEqual(whitelist.getlist('key1'), ['value1'])
        self.assertEqual(whitelist.getlist('key2'), ['value1', 'value2'])

    def test_get_list_element_by_key(self):
        value_tests = (
            ([], 'key', None, (None, None)),
            ([], 'key', '', (None, None)),
            ([{'key': ''}], 'key', 'value', (None, None)),
            ([{'key': 'value'}], 'key', 'value', ({'key': 'value'}, 0)),
        )
        for value_test in value_tests:
            result = get_list_element_by_key(value_test[0],
                                             key=value_test[1],
                                             value=value_test[2])
            self.assertEqual(result, value_test[3])

    def test_remove_all_dict_keys_from_mixed_dict(self):
        value_tests = (
            ({'key1': 'value1', 'key2': 'value2'}, 'key1', {'key2': 'value2'}),
            ([{'key1': 'value1', 'key2': 'value2'}], 'key1', [{'key2': 'value2'}]),
            ({'key1': 'value1', 'key2': {'key3': 'value3'}}, 'key3', {'key1': 'value1', 'key2': {}}),
        )
        for value_test in value_tests:
            result = value_test[0]
            remove_all_dict_keys_from_mixed_dict(result,
                                                 key_name=value_test[1])
            self.assertEqual(result, value_test[2])


class BaseFilterTestCase(TestCase):

    def setUp(self):
        pass

    def test_name(self):
        base_filter = BaseFilter(variable='operating_company_name', name='test')
        self.assertEqual(base_filter.name, 'test')

    def test_type_with_operating_company_name(self):
        base_filter = BaseFilter(variable='operating_company_name', name='test')
        self.assertEqual(base_filter.type, BaseFilter.INVESTOR_TYPE)

    def test_type_with_parent_stakeholder_name(self):
        base_filter = BaseFilter(variable='parent_stakeholder_name', name='test')
        self.assertEqual(base_filter.type, BaseFilter.INVESTOR_TYPE)

    def test_type_with_parent_investor_name(self):
        base_filter = BaseFilter(variable='parent_investor_name', name='test')
        self.assertEqual(base_filter.type, BaseFilter.INVESTOR_TYPE)

    def test_type_with_activity(self):
        base_filter = BaseFilter(variable='activity_identifier', name='test')
        self.assertEqual(base_filter.type, BaseFilter.ACTIVITY_TYPE)


class FilterTestCase(TestCase):

    fixtures = [
        'countries_and_regions',
    ]

    def setUp(self):
        self.filter_dict = {
            'variable': 'activity_identifier',
            'operator': 'is',
            'value': '1',
            'name': 'Activity ID',
            'label': 'Activity ID',
            'key': 'value',
            'display_value': 'One',
        }

    def test_invalid_operator(self):
        self.assertRaises(ValueError, lambda: Filter(variable='activity_identifier',
                                                     operator='is_not',
                                                     value='1'))

    def test_no_display_value(self):
        filter_obj = Filter(variable='activity_identifier',
                            operator='is',
                            value='1')
        self.assertEqual(filter_obj['display_value'], '1')

    def test_from_session(self):
        filter_obj = Filter.from_session(self.filter_dict)
        for key, value in self.filter_dict.items():
            self.assertEqual(filter_obj.get(key), value)

    def test_to_sql_format(self):
        filter_obj = Filter(**self.filter_dict)
        formatted_filter = filter_obj.to_sql_format()
        self.assertEqual(list(formatted_filter.keys())[0], 'activity_identifier__value__is')
        self.assertEqual(list(formatted_filter.values())[0], '1')
        filter_obj['operator'] = 'in'
        formatted_filter = filter_obj.to_sql_format()
        self.assertEqual(list(formatted_filter.keys())[0], 'activity_identifier__value__in')
        self.assertEqual(list(formatted_filter.values())[0], ['1'])

    def test_parse_value(self):
        value_tests = (
            (['value'], 'value'),
            (['value', 'value'], ['value', 'value']),
            ([], ''),
            ('value', 'value'),
            ('["value","value"]', ['value', 'value']),
        )
        filter_obj = Filter(**self.filter_dict)
        for value_test in value_tests:
            parsed_value = filter_obj.parse_value(value_test[0])
            self.assertEqual(parsed_value, value_test[1])

        parsed_value = filter_obj.parse_value('Myanmar', variable='target_country', key='value')
        self.assertEqual(parsed_value, '104')

    def test_to_elasticsearch_match_in_list(self):
        filter_obj = Filter(**self.filter_dict)
        filter_obj['operator'] = 'in'
        filter_obj['value'] = ['1', '2']
        match = filter_obj.to_elasticsearch_match()
        self.assertEqual(match, ('must',
                                 {'_filter_name': 'activity_identifier__value__in',
                                  'bool': {'minimum_should_match': 1,
                                           'should': [
                                               {'match_phrase': {'activity_identifier': '1'}},
                                               {'match_phrase': {'activity_identifier': '2'}}]}}))

    def test_to_elasticsearch_match_in_str(self):
        filter_obj = Filter(**self.filter_dict)
        filter_obj['operator'] = 'in'
        filter_obj['value'] = '1'
        match = filter_obj.to_elasticsearch_match()
        self.assertEqual(match, ('must',
                                 {'_filter_name': 'activity_identifier__value__in',
                                  'match_phrase': {'activity_identifier': '1'}}))

    def test_to_elasticsearch_match_is_list(self):
        filter_obj = Filter(**self.filter_dict)
        filter_obj['value'] = ['1', '2']
        match = filter_obj.to_elasticsearch_match()
        self.assertEqual(match, ('must',
                                 {'_filter_name': 'activity_identifier__value__is',
                                  'match_phrase': {'activity_identifier': '1'}}))

    def test_to_elasticsearch_match_is_false(self):
        filter_obj = Filter(**self.filter_dict)
        filter_obj['value'] = 'False'
        match = filter_obj.to_elasticsearch_match()
        self.assertEqual(match, ('must_not',
                                 {'_filter_name': 'activity_identifier__value__is',
                                  'match_phrase': {'activity_identifier': 'True'}}))


class PresetFilterTestCase(TestCase):

    fixtures = [
        'filters'
    ]

    def setUp(self):
        self.preset_dict = {
            'preset': 1,
            'name': 'Intention',
            'label': 'Intention is Mining',
            'hidden': False
        }

    def test_init_with_object(self):
        preset_dict = self.preset_dict
        preset_dict['preset'] = FilterPreset.objects.get(id=preset_dict['preset'])
        preset_obj = PresetFilter(**preset_dict)
        for key, value in preset_dict.items():
            if key != 'preset':
                self.assertEqual(preset_obj.get(key), value)

    def test_init_with_id(self):
        preset_obj = PresetFilter(**self.preset_dict)
        for key, value in self.preset_dict.items():
            if key != 'preset':
                self.assertEqual(preset_obj.get(key), value)

    def test_init_without_label(self):
        preset_dict = self.preset_dict
        del preset_dict['label']
        preset_obj = PresetFilter(**preset_dict)
        name = FilterPreset.objects.get(id=preset_dict['preset']).name
        self.assertEqual(preset_obj.get('label'), name)

    def test_from_session(self):
        preset_dict = self.preset_dict
        preset_dict['preset_id'] = preset_dict.pop('preset')
        preset_obj = PresetFilter.from_session(preset_dict)
        for key, value in self.preset_dict.items():
            if key != 'preset':
                self.assertEqual(preset_obj.get(key), value)
