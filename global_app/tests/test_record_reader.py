__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from global_app.views.record_reader import RecordReader

from django.test import TestCase

null = None

class TestRecordReader(TestCase):

    GROUP_VIEW_PARAMETERS = [
        {"columns": ["deal_id", "target_country", "primary_investor", "investor_name", "investor_country", "intention", "negotiation_status", "implementation_status", "intended_size", "contract_size"],
         "filters": {"deal_scope": "transnational", "order_by": ["deal_id"], "group_by": "all", "limit": "",
                     "activity": {"tags": {"pi_negotiation_status__in": ["Concluded (Oral Agreement)", "Concluded (Contract signed)"]}}, "group_value": "",
                     "investor": {"tags": {}}, "starts_with": null}},
        {"columns": ["crop", "intention", "deal_count", "availability"],
         "filters": {"deal_scope": "transnational", "order_by": ["crop"], "group_by": "crop", "limit": "",
                     "activity": {"tags": {"pi_negotiation_status__in": ["Concluded (Oral Agreement)", "Concluded (Contract signed)"]}}, "group_value": "",
                     "investor": {"tags": {}}, "starts_with": null}},
        {"columns": ["data_source_type", "intention", "deal_count", "availability"],
         "filters": {"deal_scope": "transnational", "order_by": ["data_source_type"], "group_by": "data_source_type", "limit": "",
                     "activity": {"tags": {"pi_negotiation_status__in": ["Concluded (Oral Agreement)", "Concluded (Contract signed)"]}}, "group_value": "",
                     "investor": {"tags": {}}, "starts_with": null}},
        {"columns": ["intention", "deal_count", "availability"],
         "filters": {"deal_scope": "transnational", "order_by": ["intention"], "group_by": "intention", "limit": "",
                     "activity": {"tags": {"pi_negotiation_status__in": ["Concluded (Oral Agreement)", "Concluded (Contract signed)"]}}, "group_value": "",
                     "investor": {"tags": {}}, "starts_with": null}},
        {"columns": ["investor_name", "investor_country", "intention", "deal_count", "availability"],
         "filters": {"deal_scope": "transnational", "order_by": ["investor_name"], "group_by": "investor_name", "limit": "",
                     "activity": {"tags": {"pi_negotiation_status__in": ["Concluded (Oral Agreement)", "Concluded (Contract signed)"]}}, "group_value": "",
                     "investor": {"tags": {}}, "starts_with": null}},
        {"columns": ["investor_country", "investor_region", "intention", "deal_count", "availability"],
         "filters": {"deal_scope": "transnational", "order_by": ["investor_country"], "group_by": "investor_country", "limit": "",
                     "activity": {"tags": {"pi_negotiation_status__in": ["Concluded (Oral Agreement)", "Concluded (Contract signed)"]}}, "group_value": "",
                     "investor": {"tags": {}}, "starts_with": null}},
        {"columns": ["investor_region", "intention", "deal_count", "availability"],
         "filters": {"deal_scope": "transnational", "order_by": ["investor_region"], "group_by": "investor_region", "limit": "",
                     "activity": {"tags": {"pi_negotiation_status__in": ["Concluded (Oral Agreement)", "Concluded (Contract signed)"]}}, "group_value": "",
                     "investor": {"tags": {}}, "starts_with": null}},
        {"columns": ["target_country", "target_region", "intention", "deal_count", "availability"],
         "filters": {"deal_scope": "transnational", "order_by": ["target_country"], "group_by": "target_country", "limit": "",
                     "activity": {"tags": {"pi_negotiation_status__in": ["Concluded (Oral Agreement)", "Concluded (Contract signed)"]}}, "group_value": "",
                     "investor": {"tags": {}}, "starts_with": null}},
        {"columns": ["target_region", "intention", "deal_count", "availability"],
         "filters": {"deal_scope": "transnational", "order_by": ["target_region"], "group_by": "target_region", "limit": "",
                     "activity": {"tags": {"pi_negotiation_status__in": ["Concluded (Oral Agreement)", "Concluded (Contract signed)"]}}, "group_value": "",
                     "investor": {"tags": {}}, "starts_with": null}},
    ]

    def _test_parameters_sql(self):
        for parameters in self.GROUP_VIEW_PARAMETERS:
            reader = RecordReader(parameters['filters'], parameters['columns'])
            for column in parameters['columns']:
                print('--', column)
                print(reader.get_column_sql(column), ';')

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
            print(reader.get_all_columns())

    def test_slap_columns_together(self):
        for parameters in self.GROUP_VIEW_PARAMETERS:
            reader = RecordReader(parameters['filters'], parameters['columns'])
            print(reader.get_all())
