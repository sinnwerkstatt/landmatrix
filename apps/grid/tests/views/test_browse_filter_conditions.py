from django.forms import ChoiceField, IntegerField
from django.test import TestCase

from apps.grid.views.browse_filter_conditions import *


class GridBrowserFilterConditionsTestCase(TestCase):
    def test_get_activity_field_by_key_with_activity_filter_form_field(self):
        field = get_activity_field_by_key("activity_identifier")
        self.assertIsInstance(field, IntegerField)

    def test_get_activity_field_by_key_with_deal_form_field(self):
        field = get_activity_field_by_key("level_of_accuracy")
        self.assertIsInstance(field, ChoiceField)

    def test_get_activity_field_by_key_with_investor_form_field(self):
        field = get_activity_field_by_key("operating_company_classification")
        self.assertIsInstance(field, ChoiceField)

    def test_get_activity_field_by_key_with_unknown_field(self):
        field = get_activity_field_by_key("unknown")
        self.assertEqual(None, field)

    def test_get_investor_field_by_key_with_investor_filter_form_field(self):
        field = get_investor_field_by_key("deal_count")
        self.assertIsInstance(field, IntegerField)

    def test_get_investor_field_by_key_with_parent_investor_form_field(self):
        field = get_investor_field_by_key("parent_stakeholder_classification")
        self.assertIsInstance(field, ChoiceField)

    def test_get_investor_field_by_key_with_unknown_field(self):
        field = get_investor_field_by_key("unknown")
        self.assertEqual(None, field)

    def test_get_activity_field_label_with_custom_field(self):
        label = get_activity_field_label("activity_identifier")
        self.assertEqual("Deal ID", label)

    def test_get_activity_field_label_with_investor_field(self):
        label = get_activity_field_label("operating_company_classification")
        self.assertEqual("Operating company Classification", label)

    def test_get_activity_field_label_with_unknown_field(self):
        label = get_activity_field_label("unknown")
        self.assertEqual(None, label)

    def test_get_investor_field_label_with_custom_field(self):
        label = get_investor_field_label("investor_identifier")
        self.assertEqual("Investor ID", label)

    def test_get_investor_field_label_with_parent_investor_field(self):
        label = get_investor_field_label("parent_stakeholder_classification")
        self.assertEqual("Parent company Classification", label)

    def test_get_investor_field_label_with_unknown_field(self):
        label = get_investor_field_label("unknown")
        self.assertEqual(None, label)
