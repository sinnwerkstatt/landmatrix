from django.forms import modelformset_factory
from django.test import TestCase

from apps.grid.forms.parent_investor_formset import *
from apps.landmatrix.models import HistoricalInvestor
from apps.landmatrix.tests.mixins import (
    InvestorVentureInvolvementsFixtureMixin,
    InvestorsFixtureMixin,
)


class InvestorVentureInvolvementFormTestCase(InvestorsFixtureMixin, TestCase):
    fixtures = ["countries_and_regions", "users_and_groups", "status"]

    inv_fixtures = [
        {"id": 1, "investor_identifier": 1, "name": "Test Investor #1"},
        {"id": 2, "investor_identifier": 2, "name": "Test Investor #2"},
    ]

    def setUp(self):
        super().setUp()
        self.data = {
            "fk_venture": "1",
            "fk_investor": "2",
            "percentage": 100,
            "loans_amount": 0,
            "loans_date": None,
            "comment": "Test comment",
            "role": HistoricalInvestorVentureInvolvement.STAKEHOLDER_ROLE,
            "fk_status": HistoricalInvestorVentureInvolvement.STATUS_PENDING,
        }
        self.form = InvestorVentureInvolvementForm(data=self.data)

    def test_get_display_properties(self):
        doc = self.data
        values_dict = InvestorVentureInvolvementForm.get_display_properties(doc)
        display_keys = {
            "fk_venture_display",
            "fk_investor_display",
            "role_display",
            "investment_type_display",
            "percentage_display",
            "loans_amount_display",
            "loans_currency_display",
            "loans_date_display",
            "comment_display",
            "fk_status_display",
        }
        self.assertEqual(display_keys, set(values_dict.keys()))
        self.assertEqual("1", values_dict.get("fk_venture_display"))
        self.assertEqual("2", values_dict.get("fk_investor_display"))

    def test_clean_fk_venture(self):
        self.assertEqual(True, self.form.is_valid())
        hinvestor = self.form.clean_fk_venture()
        self.assertIsInstance(hinvestor, HistoricalInvestor)
        self.assertEqual(1, hinvestor.id)

    def test_clean_fk_investor(self):
        self.assertEqual(True, self.form.is_valid())
        hinvestor = self.form.clean_fk_investor()
        self.assertIsInstance(hinvestor, HistoricalInvestor)
        self.assertEqual(2, hinvestor.id)


class ParentCompanyFormTestCase(InvestorsFixtureMixin, TestCase):
    fixtures = ["countries_and_regions", "users_and_groups", "status"]

    inv_fixtures = [
        {"id": 1, "investor_identifier": 1, "name": "Test Investor #1"},
        {"id": 2, "investor_identifier": 2, "name": "Test Investor #2"},
    ]

    def setUp(self):
        super().setUp()
        self.data = {
            "fk_venture": "1",
            "fk_investor": "2",
            "percentage": 100,
            "loans_amount": 0,
            "loans_date": None,
            "comment": "Test comment",
            "id": "",
        }
        self.form = ParentCompanyForm(initial=self.data)

    def test_init(self):
        investor_field = self.form.fields["fk_investor"]
        self.assertEqual({2}, set(investor_field.queryset.values_list("pk", flat=True)))
        self.assertEqual({"2"}, set(investor_field.widget.data.keys()))
        self.assertEqual(
            {"investor-identifier": 2}, investor_field.widget.data.get("2")
        )


class ParentInvestorFormTestCase(InvestorsFixtureMixin, TestCase):
    fixtures = ["countries_and_regions", "users_and_groups", "status"]

    inv_fixtures = [
        {"id": 1, "investor_identifier": 1, "name": "Test Investor #1"},
        {"id": 2, "investor_identifier": 2, "name": "Test Investor #2"},
    ]

    def setUp(self):
        super().setUp()
        self.data = {
            "fk_venture": "1",
            "fk_investor": "2",
            "percentage": 100,
            "loans_amount": 0,
            "loans_date": None,
            "comment": "Test comment",
            "id": "",
        }
        self.form = ParentInvestorForm(initial=self.data)

    def test_init(self):
        investor_field = self.form.fields["fk_investor"]
        self.assertEqual({2}, set(investor_field.queryset.values_list("pk", flat=True)))
        self.assertEqual({"2"}, set(investor_field.widget.data.keys()))
        self.assertEqual(
            {"investor-identifier": 2}, investor_field.widget.data.get("2")
        )


class BaseInvolvementFormSetTestCase(
    InvestorsFixtureMixin, InvestorVentureInvolvementsFixtureMixin, TestCase
):
    fixtures = ["countries_and_regions", "users_and_groups", "status"]

    inv_fixtures = [
        {"id": 1, "investor_identifier": 1, "name": "Test Investor #1"},
        {"id": 2, "investor_identifier": 2, "name": "Test Investor #2"},
    ]

    inv_inv_fixtures = [
        {
            "id": 1,
            "fk_venture_id": "1",
            "fk_investor_id": "2",
            "percentage": 100,
            "comment": "Test comment",
            "fk_status_id": 1,
        }
    ]

    def setUp(self):
        super().setUp()
        self.data = {
            "involvement-TOTAL_FORMS": 2,
            "involvement-INITIAL_FORMS": 1,
            "involvement-MIN_NUM_FORMS": 1,
            "involvement-MAX_NUM_FORMS": 1,
            "involvement-0-fk_venture": "1",
            "involvement-0-fk_investor": "2",
            "involvement-0-percentage": 100,
            "involvement-0-loans_amount": 0,
            "involvement-0-loans_date": None,
            "involvement-0-comment": "Test comment",
            "involvement-0-role": HistoricalInvestorVentureInvolvement.STAKEHOLDER_ROLE,
            "involvement-0-fk_status": HistoricalInvestorVentureInvolvement.STATUS_PENDING,
            "involvement-0-id": "1",
            "involvement-0-DELETE": "on",
            "involvement-1-fk_venture": "1",
            "involvement-1-fk_investor": "2",
            "involvement-1-percentage": 100,
            "involvement-1-loans_amount": 0,
            "involvement-1-loans_date": None,
            "involvement-1-comment": "Test comment",
            "involvement-1-role": HistoricalInvestorVentureInvolvement.STAKEHOLDER_ROLE,
            "involvement-1-fk_status": HistoricalInvestorVentureInvolvement.STATUS_PENDING,
            "involvement-1-id": "",
            "involvement-1-DELETE": None,
        }
        self.formset_class = modelformset_factory(
            HistoricalInvestorVentureInvolvement,
            form=InvestorVentureInvolvementForm,
            formset=BaseInvolvementFormSet,
            extra=1,
            min_num=0,
            max_num=1,
            can_delete=True,
        )
        self.formset = self.formset_class(data=self.data, prefix="involvement")

    def test_save(self):
        self.assertEqual(True, self.formset.is_valid())
        hinvestor = HistoricalInvestor.objects.get(pk=1)

        involvements = self.formset.save(fk_venture=hinvestor)
        self.assertGreater(len(involvements), 0)
        for involvement in involvements:
            self.assertEqual(
                HistoricalInvestor.STATUS_PENDING, involvement.fk_status_id
            )
            self.assertEqual(BaseInvolvementFormSet.ROLE, involvement.role)
            self.assertEqual(hinvestor, involvement.fk_venture)

        deleted_involvements = self.formset.deleted_objects
        self.assertGreater(len(deleted_involvements), 0)
        for involvement in deleted_involvements:
            self.assertEqual(
                HistoricalInvestor.STATUS_DELETED, involvement.fk_status_id
            )
