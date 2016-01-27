from api.query_sets.sql_generation.record_reader import RecordReader

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django.test import TestCase

from global_app.tests.deals_test_data import DealsTestData
from global_app.tests.generate_old_sql import GenerateOldSQL

null = None

class TestRecordReader(TestCase, DealsTestData, GenerateOldSQL):

    GROUP_VIEW_PARAMETERS = [
        {"columns": ["deal_id", "target_country", "operational_stakeholder", "stakeholder_name", "stakeholder_country", "intention", "negotiation_status", "implementation_status", "intended_size", "contract_size"],
         "filters": {"deal_scope": "transnational", "order_by": ["deal_id"], "group_by": "all", "limit": "",
                     "activity": {"tags": {"pi_negotiation_status__in": ["Concluded (Oral Agreement)", "Concluded (Contract signed)"]}}, "group_value": "",
                     "stakeholder": {"tags": {}}, "starts_with": null}},
        {"columns": ["crop", "intention", "deal_count", "availability"],
         "filters": {"deal_scope": "transnational", "order_by": ["crop"], "group_by": "crop", "limit": "",
                     "activity": {"tags": {"pi_negotiation_status__in": ["Concluded (Oral Agreement)", "Concluded (Contract signed)"]}}, "group_value": "",
                     "stakeholder": {"tags": {}}, "starts_with": null}},
        {"columns": ["data_source_type", "intention", "deal_count", "availability"],
         "filters": {"deal_scope": "transnational", "order_by": ["data_source_type"], "group_by": "data_source_type", "limit": "",
                     "activity": {"tags": {"pi_negotiation_status__in": ["Concluded (Oral Agreement)", "Concluded (Contract signed)"]}}, "group_value": "",
                     "stakeholder": {"tags": {}}, "starts_with": null}},
        {"columns": ["intention", "deal_count", "availability"],
         "filters": {"deal_scope": "transnational", "order_by": ["intention"], "group_by": "intention", "limit": "",
                     "activity": {"tags": {"pi_negotiation_status__in": ["Concluded (Oral Agreement)", "Concluded (Contract signed)"]}}, "group_value": "",
                     "stakeholder": {"tags": {}}, "starts_with": null}},
        {"columns": ["stakeholder_name", "stakeholder_country", "intention", "deal_count", "availability"],
         "filters": {"deal_scope": "transnational", "order_by": ["stakeholder_name"], "group_by": "stakeholder_name", "limit": "",
                     "activity": {"tags": {"pi_negotiation_status__in": ["Concluded (Oral Agreement)", "Concluded (Contract signed)"]}}, "group_value": "",
                     "stakeholder": {"tags": {}}, "starts_with": null}},
        {"columns": ["stakeholder_country", "stakeholder_region", "intention", "deal_count", "availability"],
         "filters": {"deal_scope": "transnational", "order_by": ["stakeholder_country"], "group_by": "stakeholder_country", "limit": "",
                     "activity": {"tags": {"pi_negotiation_status__in": ["Concluded (Oral Agreement)", "Concluded (Contract signed)"]}}, "group_value": "",
                     "stakeholder": {"tags": {}}, "starts_with": null}},
        {"columns": ["stakeholder_region", "intention", "deal_count", "availability"],
         "filters": {"deal_scope": "transnational", "order_by": ["stakeholder_region"], "group_by": "stakeholder_region", "limit": "",
                     "activity": {"tags": {"pi_negotiation_status__in": ["Concluded (Oral Agreement)", "Concluded (Contract signed)"]}}, "group_value": "",
                     "stakeholder": {"tags": {}}, "starts_with": null}},
        {"columns": ["target_country", "target_region", "intention", "deal_count", "availability"],
         "filters": {"deal_scope": "transnational", "order_by": ["target_country"], "group_by": "target_country", "limit": "",
                     "activity": {"tags": {"pi_negotiation_status__in": ["Concluded (Oral Agreement)", "Concluded (Contract signed)"]}}, "group_value": "",
                     "stakeholder": {"tags": {}}, "starts_with": null}},
        {"columns": ["target_region", "intention", "deal_count", "availability"],
         "filters": {"deal_scope": "transnational", "order_by": ["target_region"], "group_by": "target_region", "limit": "",
                     "activity": {"tags": {"pi_negotiation_status__in": ["Concluded (Oral Agreement)", "Concluded (Contract signed)"]}}, "group_value": "",
                     "stakeholder": {"tags": {}}, "starts_with": null}},
    ]

    def test_parameters_sql_syntax(self):
        from django.db.utils import ProgrammingError
        for parameters in self.GROUP_VIEW_PARAMETERS:
            reader = RecordReader(parameters['filters'], parameters['columns'])
            for column in parameters['columns']:
                try:
                    reader.get_column(column)
                except ProgrammingError as e:
                    self.fail('SQL for column "%s" failed:\n%s' % (column, reader.get_column_sql(column)))

    def test_get_all_columns(self):
        for parameters in self.GROUP_VIEW_PARAMETERS:
            reader = RecordReader(parameters['filters'], parameters['columns'])

    def test_slap_columns_together(self):
        for parameters in self.GROUP_VIEW_PARAMETERS:
            reader = RecordReader(parameters['filters'], parameters['columns'])

    def test_order_by(self):
        self._check_order_by('deal_id', 'deal_id  ASC')
        self._check_order_by('-deal_id', 'deal_id  DESC')
        self._check_order_by('deal_id+0', 'deal_id +0 ASC')
        self._check_order_by('-deal_id+0', 'deal_id +0 DESC')

    def test_limit(self):
        post = self.MINIMAL_POST
        post['filters']['limit'] = 10
        reader = RecordReader(post['filters'], post['columns'])
        self.assertIn('LIMIT 10', reader.get_all_at_once_sql())

    def DISABLED_test_filters(self):
        post = self.MINIMAL_POST
        to_test = [
            { "activity": {"tags": {"pi_negotiation_status__in": ["Concluded (Oral Agreement)", "Concluded (Contract signed)"]}} },
            { "stakeholder": {"tags": {"24055__is": ["0"]}} },
        ]

        old_filters = post['filters']
        for test in to_test:
            post['filters'] = test
            reader = RecordReader(post['filters'], post['columns'])
            self.assertIn(self._browse_filters_to_sql(post['filters'])['activity']['from'], reader.get_all_at_once_sql())
            self.assertIn(self._browse_filters_to_sql(post['filters'])['stakeholder']['from'], reader.get_all_at_once_sql())
            self.assertIn(self._browse_filters_to_sql(post['filters'])['activity']['where'], reader.get_all_at_once_sql())
            self.assertIn(self._browse_filters_to_sql(post['filters'])['stakeholder']['where'], reader.get_all_at_once_sql())
        post['filters'] = old_filters

    def _check_order_by(self, column, expected):
        post = self.MINIMAL_POST
        post['filters']['order_by'] = [column]
        reader = RecordReader(post['filters'], post['columns'])
        self.assertIn('ORDER BY', reader.get_all_at_once_sql())
        self.assertIn(expected, reader.get_all_at_once_sql())
