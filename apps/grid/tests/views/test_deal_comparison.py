from datetime import datetime

import pytz
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.grid.forms.deal_general_form import DealGeneralForm
from apps.grid.forms.deal_spatial_form import DealSpatialFormSet
from apps.grid.views.deal_comparison import *
from apps.landmatrix.models import HistoricalActivity
from apps.landmatrix.tests.mixins import (
    ActivitiesFixtureMixin,
    InvestorsFixtureMixin,
    InvestorActivityInvolvementsFixtureMixin,
)


class DealComparisonViewTestCase(
    ActivitiesFixtureMixin,
    InvestorsFixtureMixin,
    InvestorActivityInvolvementsFixtureMixin,
    TestCase,
):

    act_fixtures = [
        {"id": 1, "activity_identifier": 1, "attributes": {}},
        {"id": 2, "activity_identifier": 2, "attributes": {}},
        {
            "id": 3,
            "activity_identifier": 2,
            "fk_status_id": 1,
            "history_date": datetime(2000, 1, 2, 0, 0, tzinfo=pytz.utc),
            "attributes": {"contract_size": {"value": "300"}},
        },
    ]
    inv_fixtures = [{"id": 1, "investor_identifier": 1}]
    act_inv_fixtures = {"1": "1", "2": "1", "3": "1"}

    def assert_comparison(self, context_data):
        deals = context_data.get("deals", [])
        self.assertEqual(2, len(deals))
        self.assertEqual(3, deals[0].pk)
        self.assertEqual(2, deals[1].pk)
        forms = context_data.get("forms", [])
        self.assertEqual(True, forms[0][2])
        self.assertEqual(False, forms[1][2])

    def test_with_one_activity(self):
        self.client.login(username="reporter", password="test")
        response = self.client.get(reverse("compare_deals", kwargs={"activity_1": "3"}))
        self.client.logout()
        self.assertEqual(200, response.status_code)
        self.assert_comparison(response.context_data)

    def test_with_reporter(self):
        self.client.login(username="reporter", password="test")
        response = self.client.get(
            reverse("compare_deals", kwargs={"activity_1": "3", "activity_2": "2"})
        )
        self.client.logout()
        self.assertEqual(200, response.status_code)
        self.assert_comparison(response.context_data)

    def test_with_editor(self):
        self.client.login(username="editor", password="test")
        response = self.client.get(
            reverse("compare_deals", kwargs={"activity_1": "3", "activity_2": "2"})
        )
        self.client.logout()
        self.assertEqual(200, response.status_code)
        self.assert_comparison(response.context_data)

    def test_with_administrator(self):
        self.client.login(username="administrator", password="test")
        response = self.client.get(
            reverse("compare_deals", kwargs={"activity_1": "3", "activity_2": "2"})
        )
        self.client.logout()
        self.assertEqual(200, response.status_code)
        self.assert_comparison(response.context_data)


class GridDealComparisonViewTestCase(
    ActivitiesFixtureMixin,
    InvestorsFixtureMixin,
    InvestorActivityInvolvementsFixtureMixin,
    TestCase,
):

    act_fixtures = [
        {"id": 1, "activity_identifier": 1, "attributes": {}},
        {"id": 2, "activity_identifier": 2, "attributes": {}},
        {
            "id": 3,
            "activity_identifier": 3,
            "fk_status_id": 1,
            "attributes": {"contract_size": {"value": "300"}},
        },
    ]
    inv_fixtures = [{"id": 1, "investor_identifier": 1}]
    act_inv_fixtures = {"1": "1", "2": "1", "3": "1"}

    fixtures = ["countries_and_regions", "users_and_groups", "status"]

    def test_get_comparison(self):
        user = get_user_model().objects.get(username="reporter")
        deal_1 = HistoricalActivity.objects.get(id=2)
        deal_2 = HistoricalActivity.objects.get(id=3)
        forms = get_comparison(deal_1, deal_2, user=user)
        self.assertEqual(True, forms[0][2])
        self.assertEqual(False, forms[1][2])

    def test_is_equal_with_formset_changed(self):
        form_1 = DealSpatialFormSet(
            data={
                "location-TOTAL_FORMS": 1,
                "location-INITIAL_FORMS": 0,
                "location-MIN_NUM_FORMS": 1,
                "location-MAX_NUM_FORMS": 1,
                "location-0-target_country": 104,
            },
            prefix="location",
        )
        form_2 = DealSpatialFormSet(
            data={
                "location-TOTAL_FORMS": 1,
                "location-INITIAL_FORMS": 0,
                "location-MIN_NUM_FORMS": 1,
                "location-MAX_NUM_FORMS": 1,
                "location-0-target_country": 20,
            },
            prefix="location",
        )
        self.assertEqual(False, is_equal(form_1, form_2))

    def test_is_equal_with_formset_not_changed(self):
        form_1 = DealSpatialFormSet(
            data={
                "location-TOTAL_FORMS": 1,
                "location-INITIAL_FORMS": 0,
                "location-MIN_NUM_FORMS": 1,
                "location-MAX_NUM_FORMS": 1,
                "location-0-target_country": 104,
            },
            prefix="location",
        )
        form_2 = DealSpatialFormSet(
            data={
                "location-TOTAL_FORMS": 1,
                "location-INITIAL_FORMS": 0,
                "location-MIN_NUM_FORMS": 1,
                "location-MAX_NUM_FORMS": 1,
                "location-0-target_country": 104,
            },
            prefix="location",
        )
        self.assertEqual(True, is_equal(form_1, form_2))

    def test_is_equal_with_form_changed(self):
        form_1 = DealGeneralForm(data={"intended_size": "0.0"})
        form_2 = DealGeneralForm(data={"intended_size": "1.0"})
        self.assertEqual(False, is_equal(form_1, form_2))

    def test_is_equal_with_form_not_changed(self):
        form_1 = DealGeneralForm(data={"intended_size": "0.0"})
        form_2 = DealGeneralForm(data={"intended_size": "0.0"})
        self.assertEqual(True, is_equal(form_1, form_2))

    def test_is_equal_with_formset_diff_count(self):
        form_1 = DealSpatialFormSet(
            data={
                "location-TOTAL_FORMS": 1,
                "location-INITIAL_FORMS": 0,
                "location-MIN_NUM_FORMS": 1,
                "location-MAX_NUM_FORMS": 1,
                "location-0-id": 1,
                "location-0-target_country": 104,
            },
            prefix="location",
        )
        form_2 = DealSpatialFormSet(
            data={
                "location-TOTAL_FORMS": 2,
                "location-INITIAL_FORMS": 0,
                "location-MIN_NUM_FORMS": 2,
                "location-MAX_NUM_FORMS": 2,
                "location-0-id": 1,
                "location-0-target_country": 20,
                "location-1-target_country": 20,
            },
            prefix="location",
        )
        self.assertEqual(False, is_equal(form_1, form_2))

    def test_is_equal_with_invalid_form(self):
        form_1 = DealGeneralForm(data={"intended_size": "foo"})
        form_2 = DealGeneralForm(data={"intended_size": "0.0"})
        self.assertEqual(False, is_equal(form_1, form_2))
