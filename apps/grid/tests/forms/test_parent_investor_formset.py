from django.forms import modelformset_factory
from django.test import TestCase

from apps.grid.forms.parent_investor_formset import *
from apps.landmatrix.models import HistoricalInvestor, InvestorVentureInvolvement


class InvestorVentureInvolvementFormTestCase(TestCase):

    fixtures = [
        "countries_and_regions",
        "users_and_groups",
        "status",
    ]

    def setUp(self):
        self.data = {
            "fk_venture": "10",
            "fk_investor": "20",
            "percentage": 100,
            "loans_amount": 0,
            "loans_date": None,
            "comment": "Test comment",
            "role": InvestorVentureInvolvement.STAKEHOLDER_ROLE,
            "fk_status": InvestorVentureInvolvement.STATUS_PENDING,
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
        self.assertEqual(10, hinvestor.id)

    def test_clean_fk_investor(self):
        self.assertEqual(True, self.form.is_valid())
        hinvestor = self.form.clean_fk_investor()
        self.assertIsInstance(hinvestor, HistoricalInvestor)
        self.assertEqual(20, hinvestor.id)


class ParentCompanyFormTestCase(TestCase):

    fixtures = [
        "countries_and_regions",
        "users_and_groups",
        "status",
    ]

    def setUp(self):
        self.data = {
            "fk_venture": "10",
            "fk_investor": "20",
            "percentage": 100,
            "loans_amount": 0,
            "loans_date": None,
            "comment": "Test comment",
            "id": "",
        }
        self.form = ParentCompanyForm(initial=self.data)

    def test_init(self):
        investor_field = self.form.fields["fk_investor"]
        self.assertEqual(
            {20}, set(investor_field.queryset.values_list("pk", flat=True))
        )
        self.assertEqual({"20"}, set(investor_field.widget.data.keys()))
        self.assertEqual(
            {"investor-identifier": 2}, investor_field.widget.data.get("20")
        )


class ParentInvestorFormTestCase(TestCase):

    fixtures = [
        "countries_and_regions",
        "users_and_groups",
        "status",
    ]

    def setUp(self):
        self.data = {
            "fk_venture": "10",
            "fk_investor": "20",
            "percentage": 100,
            "loans_amount": 0,
            "loans_date": None,
            "comment": "Test comment",
            "id": "",
        }
        self.form = ParentInvestorForm(initial=self.data)

    def test_init(self):
        investor_field = self.form.fields["fk_investor"]
        self.assertEqual(
            {20}, set(investor_field.queryset.values_list("pk", flat=True))
        )
        self.assertEqual({"20"}, set(investor_field.widget.data.keys()))
        self.assertEqual(
            {"investor-identifier": 2}, investor_field.widget.data.get("20")
        )


class BaseInvolvementFormSetTestCase(TestCase):

    fixtures = [
        "countries_and_regions",
        "users_and_groups",
        "status",
    ]

    def setUp(self):
        self.data = {
            "involvement-TOTAL_FORMS": 2,
            "involvement-INITIAL_FORMS": 1,
            "involvement-MIN_NUM_FORMS": 1,
            "involvement-MAX_NUM_FORMS": 1,
            "involvement-0-fk_venture": "10",
            "involvement-0-fk_investor": "20",
            "involvement-0-percentage": 100,
            "involvement-0-loans_amount": 0,
            "involvement-0-loans_date": None,
            "involvement-0-comment": "Test comment",
            "involvement-0-role": InvestorVentureInvolvement.STAKEHOLDER_ROLE,
            "involvement-0-fk_status": InvestorVentureInvolvement.STATUS_PENDING,
            "involvement-0-id": "60",
            "involvement-0-DELETE": "on",
            "involvement-1-fk_venture": "10",
            "involvement-1-fk_investor": "20",
            "involvement-1-percentage": 100,
            "involvement-1-loans_amount": 0,
            "involvement-1-loans_date": None,
            "involvement-1-comment": "Test comment",
            "involvement-1-role": InvestorVentureInvolvement.STAKEHOLDER_ROLE,
            "involvement-1-fk_status": InvestorVentureInvolvement.STATUS_PENDING,
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
        hinvestor = HistoricalInvestor.objects.get(pk=10)

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
