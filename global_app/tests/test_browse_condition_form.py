__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from landmatrix.models.browse_condition import BrowseCondition
from global_app.views.view_aux_functions import create_condition_formset, FILTER_VAR_ACT, FILTER_VAR_INV
from global_app.views.browse_condition_form import BrowseConditionForm
from global_app.views.browse_filter_conditions import BrowseFilterConditions, get_field_by_key, a_keys
from global_app.tests.test_view_base import extract_tag

from django.test import TestCase
from django.utils.datastructures import MultiValueDict
from pprint import pprint


class TestBrowseConditionForm(TestCase):

    def setUp(self):
        self.Formset = create_condition_formset()

    def test_first(self):
        form = self.Formset(
            MultiValueDict({'conditions_empty-MAX_NUM_FORMS': [''], 'conditions_empty-INITIAL_FORMS': [0], 'conditions_empty-TOTAL_FORMS': [0]}),
            prefix="conditions_empty"
        )

    def test_data_from_live(self):
        formset = self.Formset(
            MultiValueDict(
                {
                    'conditions_empty-MAX_NUM_FORMS': [''],
                    'conditions_empty-TOTAL_FORMS': [2],
                    'conditions_empty-INITIAL_FORMS': [2],
                    'conditions_empty-0-variable': ['negotiation_status'],
                    'conditions_empty-0-operator': ['in'],
                    'conditions_empty-0-value': ['30', '40'],
                    'conditions_empty-1-variable': ['-2'],
                    'conditions_empty-1-operator': ['is'],
                    'conditions_empty-1-value': ['20'],
                }
            ),
            prefix="conditions_empty"
        )
        self.assertEqual(2, len(formset.forms))
        self._check_all_forms_for_vars_and_ops(formset)

    def test_one_condition(self):
        formset = self.Formset(
            MultiValueDict(
                {
                    'conditions_empty-MAX_NUM_FORMS': [''],
                    'conditions_empty-TOTAL_FORMS': [1],
                    'conditions_empty-INITIAL_FORMS': [1],
                    'conditions_empty-0-variable': ['negotiation_status'],
                    'conditions_empty-0-operator': ['in'],
                    'conditions_empty-0-value': [],
                }
            ),
            prefix="conditions_empty"
        )
        self.assertEqual(1, len(formset.forms))
        self._check_all_forms_for_vars_and_ops(formset)

    def test_all_fields(self):
        for field in FILTER_VAR_ACT+FILTER_VAR_INV:
            formset = self.Formset(
                MultiValueDict(
                    {
                        'conditions_empty-MAX_NUM_FORMS': [''],
                        'conditions_empty-TOTAL_FORMS': [1],
                        'conditions_empty-INITIAL_FORMS': [1],
                        'conditions_empty-0-variable': [field],
                        'conditions_empty-0-operator': ['in'],
                        'conditions_empty-0-value': [],
                    }
                ),
                prefix="conditions_empty"
            )
            self.assertEqual(1, len(formset.forms))
            self._check_all_forms_for_vars_and_ops(formset)

    def test_all_fields_and_ops(self):
        from global_app.views.sql_generation.filter_to_sql import FilterToSQL
        for field in FILTER_VAR_ACT+FILTER_VAR_INV:
            for op in FilterToSQL.OPERATION_MAP.keys():
                formset = self.Formset(
                    MultiValueDict(
                        {
                            'conditions_empty-MAX_NUM_FORMS': [''],
                            'conditions_empty-TOTAL_FORMS': [1],
                            'conditions_empty-INITIAL_FORMS': [1],
                            'conditions_empty-0-variable': [field],
                            'conditions_empty-0-operator': [op],
                            'conditions_empty-0-value': [],
                        }
                    ),
                    prefix="conditions_empty"
                )
                self.assertEqual(1, len(formset.forms))
                self._check_all_forms_for_vars_and_ops(formset)

    def _check_all_forms_for_vars_and_ops(self, formset):
        for f in formset.forms:
            self._check_all_variables_present(extract_tag(f.as_ul(), '<select', '</select>'))
            self._check_all_operators_present(extract_tag(f.as_ul()[f.as_ul().find('<select')+1:], '<select', '</select>'))

    def _check_all_variables_present(self, variable_select):
        for var in FILTER_VAR_ACT:
            self.assertIn(var, variable_select)
        for var in FILTER_VAR_INV:
            self.assertIn(var, variable_select)

    def _check_all_operators_present(self, operator_select):
        from global_app.views.sql_generation.filter_to_sql import FilterToSQL
        for op in FilterToSQL.OPERATION_MAP.keys():
            self.assertIn(op, operator_select)
