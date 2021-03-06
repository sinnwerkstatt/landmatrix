from datetime import datetime
from unittest.mock import patch

import pytz
from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.grid.tests.views.base import BaseDealTestCase
from apps.landmatrix.models import ActivityChangeset
from apps.landmatrix.models.activity import *
from apps.landmatrix.tests.mixins import (
    ActivitiesFixtureMixin,
    InvestorsFixtureMixin,
    InvestorActivityInvolvementsFixtureMixin,
    InvestorVentureInvolvementsFixtureMixin,
)


class ActivityQuerySetTestCase(ActivitiesFixtureMixin, TestCase):

    act_fixtures = [
        {"id": 10, "activity_identifier": 1, "fk_status_id": 1},
        {"id": 20, "activity_identifier": 2},
        {
            "id": 21,
            "activity_identifier": 2,
            "fk_status_id": 3,
            "history_date": datetime(2000, 1, 2, 0, 0, tzinfo=pytz.utc),
        },
        {"id": 30, "activity_identifier": 3},
        {
            "id": 31,
            "activity_identifier": 3,
            "fk_status_id": 1,
            "history_date": datetime(2000, 1, 2, 0, 0, tzinfo=pytz.utc),
        },
        {"id": 40, "activity_identifier": 4, "fk_status_id": 4},
        {"id": 50, "activity_identifier": 5, "fk_status_id": 5},
        {"id": 60, "activity_identifier": 6, "fk_status_id": 6},
        {"id": 70, "activity_identifier": 7, "fk_status_id": 2, "history_user_id": 2},
    ]

    def setUp(self):
        super().setUp()
        self.qs = HistoricalActivity.objects

    def test_public_with_user(self):
        user = get_user_model().objects.get(username="reporter")
        qs = self.qs.public(user=user)
        self.assertGreater(qs.count(), 0)

    def test_public_without_user(self):
        qs = self.qs.public()
        self.assertGreater(qs.count(), 0)
        self.assertEqual(
            set(ActivityBase.PUBLIC_STATUSES),
            set(qs.values_list("fk_status_id", flat=True)),
        )

    def test_public_or_deleted(self):
        qs = self.qs.public_or_deleted()
        self.assertGreater(qs.count(), 0)
        statuses = ActivityBase.PUBLIC_STATUSES + (ActivityBase.STATUS_DELETED,)
        self.assertEqual(set(statuses), set(qs.values_list("fk_status_id", flat=True)))

    def test_public_or_deleted_with_user(self):
        user = get_user_model().objects.get(username="reporter")
        qs = self.qs.public_or_deleted(user=user)
        self.assertGreater(qs.count(), 0)

    def test_public_or_pending(self):
        qs = self.qs.public_or_pending()
        self.assertGreater(qs.count(), 0)
        statuses = ActivityBase.PUBLIC_STATUSES + (ActivityBase.STATUS_PENDING,)
        self.assertEqual(set(statuses), set(qs.values_list("fk_status_id", flat=True)))

    def test_public_deleted_or_pending(self):
        qs = self.qs.public_deleted_or_pending()
        self.assertGreater(qs.count(), 0)
        statuses = ActivityBase.PUBLIC_STATUSES + (
            ActivityBase.STATUS_DELETED,
            ActivityBase.STATUS_PENDING,
        )
        self.assertEqual(set(statuses), set(qs.values_list("fk_status_id", flat=True)))

    def test_pending(self):
        qs = self.qs.pending()
        self.assertGreater(qs.count(), 0)
        statuses = (ActivityBase.STATUS_PENDING, ActivityBase.STATUS_TO_DELETE)
        self.assertEqual(set(statuses), set(qs.values_list("fk_status_id", flat=True)))

    def test_pending_only(self):
        qs = self.qs.pending_only()
        self.assertGreater(qs.count(), 0)
        self.assertEqual(
            {ActivityBase.STATUS_PENDING},
            set(qs.values_list("fk_status_id", flat=True)),
        )

    def test_active(self):
        qs = self.qs.active()
        self.assertGreater(qs.count(), 0)
        self.assertEqual(
            {ActivityBase.STATUS_ACTIVE}, set(qs.values_list("fk_status_id", flat=True))
        )

    def test_overwritten(self):
        qs = self.qs.overwritten()
        self.assertGreater(qs.count(), 0)
        self.assertEqual(
            {ActivityBase.STATUS_OVERWRITTEN},
            set(qs.values_list("fk_status_id", flat=True)),
        )

    def test_to_delete(self):
        qs = self.qs.to_delete()
        self.assertGreater(qs.count(), 0)
        self.assertEqual(
            {ActivityBase.STATUS_TO_DELETE},
            set(qs.values_list("fk_status_id", flat=True)),
        )

    def test_deleted(self):
        qs = self.qs.deleted()
        self.assertGreater(qs.count(), 0)
        self.assertEqual(
            {ActivityBase.STATUS_DELETED},
            set(qs.values_list("fk_status_id", flat=True)),
        )

    def test_rejected(self):
        qs = self.qs.rejected()
        self.assertGreater(qs.count(), 0)
        self.assertEqual(
            {ActivityBase.STATUS_REJECTED},
            set(qs.values_list("fk_status_id", flat=True)),
        )


class ActivityBaseTestCase(
    ActivitiesFixtureMixin,
    InvestorsFixtureMixin,
    InvestorActivityInvolvementsFixtureMixin,
    InvestorVentureInvolvementsFixtureMixin,
    BaseDealTestCase,
):

    act_fixtures = [
        {
            "id": 10,
            "activity_identifier": 1,
            "fully_updated": True,
            "attributes": {
                "negotiation_status": {"value": "Contract signed", "date": "2000"},
                "implementation_status": {
                    "value": ActivityBase.IMPLEMENTATION_STATUS_IN_OPERATION,
                    "date": "2000",
                },
            },
        },
        {"id": 20, "activity_identifier": 2, "attributes": {}},
        {"id": 21, "activity_identifier": 2, "fk_status_id": 1, "attributes": {}},
        {"id": 30, "activity_identifier": 3, "attributes": {}},
        {"id": 40, "activity_identifier": 4, "attributes": {}},
        {
            "id": 50,
            "activity_identifier": 5,
            "attributes": {"target_country": {"value": "20"}},
        },
    ]
    inv_fixtures = [
        {"id": 10, "investor_identifier": 1, "name": "Test Investor #1"},
        {"id": 20, "investor_identifier": 2, "name": "Test Investor #2"},
        {
            "id": 21,
            "investor_identifier": 2,
            "fk_status_id": 1,
            "name": "Test Investor #2",
        },
        {
            "id": 30,
            "investor_identifier": 3,
            "name": "Test Investor #3",
            "fk_country_id": "104",
        },
        {"id": 40, "investor_identifier": 4, "name": "Unknown"},
        {"id": 50, "investor_identifier": 5, "name": "Test investor #5"},
    ]
    act_inv_fixtures = {
        "10": "10",
        "20": "20",
        "21": "20",
        "30": "30",
        "40": "40",
        "50": "50",
    }
    inv_inv_fixtures = [
        {"fk_venture_id": "10", "fk_investor_id": "20"},
        {"fk_venture_id": "50", "fk_investor_id": "40"},
    ]

    def test_save(self):
        activity = HistoricalActivity()
        activity.save()
        self.assertIsNotNone(activity.activity_identifier)
        self.assertNotEqual(
            activity.activity_identifier, ActivityBase.ACTIVITY_IDENTIFIER_DEFAULT
        )

    def test_get_next_activity_identifier(self):
        activity_identifier = HistoricalActivity.get_next_activity_identifier()
        self.assertGreater(activity_identifier, 1)
        self.assertNotEqual(
            activity_identifier, ActivityBase.ACTIVITY_IDENTIFIER_DEFAULT
        )

    def test_get_latest_activity(self):
        activity = HistoricalActivity.get_latest_activity(activity_identifier=2)
        self.assertEqual(21, activity.id)

    def test_get_latest_active_activity(self):
        activity = HistoricalActivity.get_latest_active_activity(activity_identifier=2)
        self.assertEqual(20, activity.id)

    def test_operational_stakeholder(self):
        activity = HistoricalActivity.objects.get(id=10)
        self.assertEqual(10, activity.operational_stakeholder.id)

    def test_stakeholders(self):
        activity = HistoricalActivity.objects.get(id=10)
        self.assertEqual({20}, set(activity.stakeholders))

    def test_stakeholders_without_operating_company(self):
        activity = HistoricalActivity.objects.get(id=10)
        activity.involvements.all().delete()
        self.assertEqual([], activity.stakeholders)

    def test_get_history(self):
        activity = HistoricalActivity.objects.get(id=21)
        user = get_user_model().objects.get(username="reporter")
        self.assertGreater(len(activity.get_history(user=user)), 0)

    def test_get_latest(self):
        activity = HistoricalActivity.objects.get(id=20)
        user = get_user_model().objects.get(username="reporter")
        latest = activity.get_latest(user=user)
        self.assertEqual(21, latest.id)

    def test_is_editable_old_version_with_superuser(self):
        activity = HistoricalActivity.objects.get(id=20)
        user = get_user_model().objects.get(username="superuser")
        self.assertEqual(True, activity.is_editable(user=user))

    def test_is_editable_old_version_with_reporter(self):
        activity = HistoricalActivity.objects.get(id=20)
        user = get_user_model().objects.get(username="reporter")
        self.assertEqual(False, activity.is_editable(user=user))

    def test_is_editable_new_version_with_reporter(self):
        activity = HistoricalActivity.objects.get(id=21)
        user = get_user_model().objects.get(username="reporter-2")
        self.assertEqual(False, activity.is_editable(user=user))

    def test_is_editable_new_version_with_author(self):
        activity = HistoricalActivity.objects.get(id=21)
        user = get_user_model().objects.get(username="reporter")
        self.assertEqual(False, activity.is_editable(user=user))

    def test_is_editable_new_version_with_rejected(self):
        activity = HistoricalActivity.objects.get(id=21)
        activity.fk_status_id = HistoricalActivity.STATUS_REJECTED
        activity.save()
        user = get_user_model().objects.get(username="reporter-2")
        self.assertEqual(False, activity.is_editable(user=user))

    def test_is_editable_new_version_with_editor(self):
        activity = HistoricalActivity.objects.get(id=21)
        user = get_user_model().objects.get(username="editor")
        self.assertEqual(True, activity.is_editable(user=user))

    def test_is_editable_new_version_without_user(self):
        activity = HistoricalActivity.objects.get(id=21)
        self.assertEqual(False, activity.is_editable(user=None))

    def test_target_country(self):
        activity = HistoricalActivity.objects.get(id=10)
        target_country = activity.target_country
        self.assertEqual(104, target_country.id)

    def test_attributes_as_dict(self):
        activity = HistoricalActivity.objects.get(id=10)
        attr_dict = activity.attributes_as_dict
        self.assertIsInstance(attr_dict, dict)
        self.assertGreater(len(attr_dict.keys()), 0)

    def test_get_top_investors(self):
        activity = HistoricalActivity.objects.get(id=10)
        top_investor = HistoricalInvestor.objects.get(id=20)
        self.assertEqual({top_investor}, set(activity.get_top_investors()))

    def test_get_parent_companies(self):
        activity = HistoricalActivity.objects.get(id=10)
        investor = HistoricalInvestor.objects.get(id=20)
        self.assertEqual({investor}, set(activity.get_parent_companies()))

    def test_get_investor_countries(self):
        activity = HistoricalActivity.objects.get(id=10)
        investor_country = Country.objects.get(id=116)
        self.assertEqual({investor_country}, set(activity.get_investor_countries()))

    def test_get_deal_size_with_intended(self):
        activity = HistoricalActivity.objects.get(id=10)
        activity.attributes.filter(name="negotiation_status").update(
            value=HistoricalActivity.NEGOTIATION_STATUS_UNDER_NEGOTIATION
        )
        activity.attributes.create(name="intended_size", value="2000")
        self.assertEqual(2000, activity.get_deal_size())

    def test_get_deal_size_with_concluded(self):
        activity = HistoricalActivity.objects.get(id=10)
        self.assertEqual(200, activity.get_deal_size())

    def test_get_deal_size_with_failed(self):
        activity = HistoricalActivity.objects.get(id=10)
        activity.attributes.filter(name="negotiation_status").update(
            value=HistoricalActivity.NEGOTIATION_STATUS_NEGOTIATIONS_FAILED
        )
        activity.attributes.create(name="intended_size", value="2000")
        self.assertEqual(2000, activity.get_deal_size())

    def test_get_deal_size_with_cancelled(self):
        activity = HistoricalActivity.objects.get(id=10)
        activity.attributes.filter(name="negotiation_status").update(
            value=HistoricalActivity.NEGOTIATION_STATUS_CONTRACT_CANCELLED
        )
        self.assertEqual(200, activity.get_deal_size())

    def test_get_deal_size_with_expired(self):
        activity = HistoricalActivity.objects.get(id=10)
        activity.attributes.filter(name="negotiation_status").update(
            value=HistoricalActivity.NEGOTIATION_STATUS_CONTRACT_EXPIRED
        )
        self.assertEqual(200, activity.get_deal_size())

    def test_get_deal_size_with_change_of_ownership(self):
        activity = HistoricalActivity.objects.get(id=10)
        activity.attributes.filter(name="negotiation_status").update(
            value=HistoricalActivity.NEGOTIATION_STATUS_CHANGE_OF_OWNERSHIP
        )
        self.assertEqual(200, activity.get_deal_size())

    def test_get_deal_size_with_comma(self):
        activity = HistoricalActivity.objects.get(id=10)
        activity.attributes.filter(name="contract_size").update(value="2000,0")
        self.assertEqual(2000, activity.get_deal_size())

    def test_get_deal_size_with_dot(self):
        activity = HistoricalActivity.objects.get(id=10)
        activity.attributes.filter(name="contract_size").update(value="2000.0")
        self.assertEqual(2000, activity.get_deal_size())

    def test_get_negotiation_status(self):
        activity = HistoricalActivity.objects.get(id=10)
        self.assertEqual("Contract signed", activity.get_negotiation_status())

    def test_get_implementation_status(self):
        activity = HistoricalActivity.objects.get(id=10)
        self.assertEqual(
            HistoricalActivity.IMPLEMENTATION_STATUS_IN_OPERATION,
            activity.get_implementation_status(),
        )

    def test_get_contract_size(self):
        activity = HistoricalActivity.objects.get(id=10)
        self.assertEqual(200, activity.get_contract_size())

    def test_get_production_size(self):
        activity = HistoricalActivity.objects.get(id=10)
        self.assertEqual(3, activity.get_production_size())

    def test_get_agricultural_produce(self):
        activity = HistoricalActivity.objects.get(id=10)
        self.assertEqual({"Non-Food"}, set(activity.get_agricultural_produce()))

    def test_get_agricultural_produce_with_multi(self):
        activity = HistoricalActivity.objects.get(id=10)
        activity.attributes.create(name="crops", value="4")
        self.assertEqual(
            activity.AGRICULTURAL_PRODUCE_MULTI, activity.get_agricultural_produce()
        )

    def test_is_public_deal_with_has_flag_not_public(self):
        activity = HistoricalActivity.objects.get(id=10)
        activity.attributes.filter(name="not_public").update(value="True")
        self.assertEqual(False, activity.is_public_deal())
        activity.attributes.filter(name="not_public").update(value="False")

    def test_is_public_deal__with_missing_information(self):
        activity = HistoricalActivity.objects.get(id=10)
        activity.attributes.filter(name="target_country").delete()
        self.assertEqual(False, activity.is_public_deal())

    def test_is_public_deal__with_involvements_missing(self):
        activity = HistoricalActivity.objects.get(id=10)
        activity.involvements.all().delete()
        self.assertEqual(False, activity.is_public_deal())

    def test_is_public_deal_with_invalid_investors(self):
        activity = HistoricalActivity.objects.get(id=40)
        self.assertEqual(False, activity.is_public_deal())

    def test_is_public_deal_with_high_income_country(self):
        activity = HistoricalActivity.objects.get(id=50)
        self.assertEqual(False, activity.is_public_deal())

    def test_is_public_deal_with_filters_passed(self):
        activity = HistoricalActivity.objects.get(id=10)
        self.assertEqual(True, activity.is_public_deal())

    def test_get_not_public_reason_with_has_flag_not_public(self):
        activity = HistoricalActivity.objects.get(id=10)
        activity.attributes.filter(name="not_public").update(value="True")
        self.assertEqual("1. Flag not public set", activity.get_not_public_reason())
        activity.attributes.filter(name="not_public").update(value="False")

    def test_get_not_public_reason_with_missing_information(self):
        activity = HistoricalActivity.objects.get(id=10)
        activity.attributes.filter(name="target_country").delete()
        self.assertEqual(
            "2. Minimum information missing", activity.get_not_public_reason()
        )

    def test_get_not_public_reason_with_involvements_missing(self):
        activity = HistoricalActivity.objects.get(id=10)
        activity.involvements.all().delete()
        self.assertEqual("3. involvements missing", activity.get_not_public_reason())

    def test_get_not_public_reason_with_invalid_investors(self):
        activity = HistoricalActivity.objects.get(id=40)
        self.assertEqual(
            "4. Invalid Operating company name and Invalid Parent companies/investors",
            activity.get_not_public_reason(),
        )

    def test_get_not_public_reason_with_high_income_country(self):
        activity = HistoricalActivity.objects.get(id=50)
        self.assertEqual("5. High income country", activity.get_not_public_reason())

    def test_get_not_public_reason_with_filters_passed(self):
        activity = HistoricalActivity.objects.get(id=10)
        self.assertEqual("Filters passed (public)", activity.get_not_public_reason())

    def test_is_high_income_target_country_with_high(self):
        activity = HistoricalActivity.objects.get(id=50)
        self.assertEqual(True, activity.is_high_income_target_country())

    def test_is_high_income_target_country_without_high(self):
        activity = HistoricalActivity.objects.get(id=10)
        self.assertEqual(False, activity.is_high_income_target_country())

    def test_has_invalid_operating_company_with_valid(self):
        activity = HistoricalActivity.objects.get(id=10)
        involvements = activity.involvements.all()
        self.assertEqual(False, activity.has_invalid_operating_company(involvements))

    def test_has_invalid_operating_company_with_invalid(self):
        activity = HistoricalActivity.objects.get(id=40)
        involvements = activity.involvements.all()
        self.assertEqual(True, activity.has_invalid_operating_company(involvements))

    def test_has_invalid_parents_with_valid(self):
        activity = HistoricalActivity.objects.get(id=10)
        involvements = activity.involvements.all()
        self.assertEqual(False, activity.has_invalid_parents(involvements))

    def test_has_invalid_parents_with_invalid(self):
        activity = HistoricalActivity.objects.get(id=50)
        involvements = activity.involvements.all()
        self.assertEqual(True, activity.has_invalid_parents(involvements))

    def test_missing_information(self):
        activity = HistoricalActivity.objects.get(id=10)
        self.assertEqual(False, activity.missing_information())

    def test_has_flag_not_public(self):
        activity = HistoricalActivity.objects.get(id=10)
        self.assertEqual(False, activity.has_flag_not_public())

    def test_get_init_date(self):
        activity = HistoricalActivity.objects.get(id=10)
        self.assertEqual("2000", activity.get_init_date())

    def test_get_deal_scope_transnational(self):
        activity = HistoricalActivity.objects.get(id=10)
        self.assertEqual("transnational", activity.get_deal_scope())

    def test_get_deal_scope_domestic_and_self_reference(self):
        activity = HistoricalActivity.objects.get(id=30)
        self.assertEqual("domestic", activity.get_deal_scope())

    def test_format_investors(self):
        activity = HistoricalActivity.objects.get(id=10)
        investor = HistoricalInvestor.objects.get(id=10)
        self.assertEqual(
            "Test Investor 1#1#Cambodia", activity.format_investors([investor])
        )

    def test_get_availability(self):
        activity = HistoricalActivity.objects.get(id=10)
        self.assertGreater(activity.get_availability(), 0)

    def test_get_availability_total(self):
        activity = HistoricalActivity.objects.get(id=10)
        self.assertGreater(activity.get_availability_total(), 0)

    def test_get_forest_concession(self):
        activity = HistoricalActivity.objects.get(id=10)
        self.assertEqual(0, activity.get_forest_concession())

    def test_get_updated_date(self):
        activity = HistoricalActivity.objects.get(id=10)
        self.assertEqual(
            datetime(2000, 1, 1, 0, 0, tzinfo=pytz.utc), activity.get_updated_date()
        )

    def test_get_updated_user(self):
        activity = HistoricalActivity.objects.get(id=10)
        self.assertEqual(1, activity.get_updated_user())

    def test_get_fully_updated_date(self):
        activity = HistoricalActivity.objects.get(id=10)
        self.assertEqual(
            datetime(2000, 1, 1, 0, 0, tzinfo=pytz.utc),
            activity.get_fully_updated_date(),
        )

    def test_get_fully_updated_user(self):
        activity = HistoricalActivity.objects.get(id=10)
        self.assertEqual(1, activity.get_fully_updated_user())


class HistoricalActivityQuerySetTestCase(
    ActivitiesFixtureMixin,
    InvestorsFixtureMixin,
    InvestorActivityInvolvementsFixtureMixin,
    TestCase,
):

    act_fixtures = [
        {"id": 10, "activity_identifier": 1, "history_user_id": 1, "attributes": {}},
        {"id": 20, "activity_identifier": 2, "fk_status_id": 2, "attributes": {}},
        {"id": 21, "activity_identifier": 2, "fk_status_id": 1, "attributes": {}},
        {"id": 30, "activity_identifier": 3, "fk_status_id": 1, "attributes": {}},
    ]
    inv_fixtures = [
        {"id": 10, "investor_identifier": 1, "name": "Test Investor #1"},
        {"id": 20, "investor_identifier": 2, "name": "Test Investor #2"},
        {"id": 30, "investor_identifier": 3, "name": "Test Investor #3"},
    ]
    act_inv_fixtures = {"10": "10", "20": "20", "30": "30"}

    def setUp(self):
        super().setUp()
        self.qs = HistoricalActivity.objects

    def test_get_for_user(self):
        user = get_user_model().objects.get(username="reporter")
        qs = self.qs.get_for_user(user=user)
        self.assertGreater(qs.count(), 0)
        self.assertEqual({user.id}, set(qs.values_list("history_user_id", flat=True)))

    def test_with_multiple_revisions(self):
        qs = self.qs.with_multiple_revisions()
        self.assertGreater(qs.count(), 0)

    def test_without_multiple_revisions(self):
        qs = self.qs.without_multiple_revisions()
        self.assertGreater(qs.count(), 0)

    def test_latest_ids(self):
        latest_ids = self.qs.latest_ids()
        self.assertEqual(len(latest_ids), 3)
        latest_ids = self.qs.latest_ids(status=HistoricalActivity.PUBLIC_STATUSES)
        self.assertEqual(len(latest_ids), 1)

    def test_latest_only(self):
        qs = self.qs.latest_only()
        self.assertGreater(qs.count(), 0)


class HistoricalActivityTestCase(
    ActivitiesFixtureMixin,
    InvestorsFixtureMixin,
    InvestorActivityInvolvementsFixtureMixin,
    BaseDealTestCase,
):

    act_fixtures = [
        {"id": 10, "activity_identifier": 1, "attributes": {}},
        {"id": 20, "activity_identifier": 2, "attributes": {}},
        {
            "id": 21,
            "activity_identifier": 2,
            "fk_status_id": 1,
            "attributes": {"production_size": {"value": "100"}},
        },
        {"id": 30, "activity_identifier": 3, "attributes": {}},
        {"id": 31, "activity_identifier": 3, "fk_status_id": 6, "attributes": {}},
        {"id": 40, "activity_identifier": 4, "fk_status_id": 4, "attributes": {}},
        {"id": 50, "activity_identifier": 5, "fk_status_id": 5, "attributes": {}},
        {"id": 60, "activity_identifier": 6, "fk_status_id": 6, "attributes": {}},
    ]
    inv_fixtures = [
        {"id": 10, "investor_identifier": 1, "name": "Test Investor #1"},
        {"id": 20, "investor_identifier": 2, "name": "Test Investor #2"},
        {"id": 30, "investor_identifier": 3, "name": "Test Investor #3"},
        {"id": 40, "investor_identifier": 4, "name": "Test Investor #4"},
        {"id": 50, "investor_identifier": 5, "name": "Test Investor #5"},
        {"id": 60, "investor_identifier": 6, "name": "Test Investor #6"},
    ]
    act_inv_fixtures = {
        "10": "10",
        "20": "20",
        "30": "30",
        "31": "30",
        "40": "40",
        "50": "50",
        "60": "60",
    }

    def test_approve_change(self):
        activity = HistoricalActivity.objects.get(id=21)
        user = get_user_model().objects.get(username="administrator")
        activity.approve_change(user=user, comment="Test approve change")
        self.assertEqual(HistoricalActivity.STATUS_OVERWRITTEN, activity.fk_status_id)
        self.assertGreater(activity.changesets.count(), 0)
        changeset = activity.changesets.latest()
        self.assertEqual("Test approve change", changeset.comment)

    def test_reject_change(self):
        activity = HistoricalActivity.objects.get(id=21)
        user = get_user_model().objects.get(username="administrator")
        activity.reject_change(user=user, comment="Test reject change")
        self.assertEqual(HistoricalActivity.STATUS_REJECTED, activity.fk_status_id)
        self.assertGreater(activity.changesets.count(), 0)
        changeset = activity.changesets.latest()
        self.assertEqual("Test reject change", changeset.comment)

    def test_approve_delete(self):
        activity = HistoricalActivity.objects.get(id=31)
        user = get_user_model().objects.get(username="administrator")
        activity.approve_delete(user=user, comment="Test approve delete")
        self.assertEqual(HistoricalActivity.STATUS_DELETED, activity.fk_status_id)
        self.assertGreater(activity.changesets.count(), 0)
        changeset = activity.changesets.latest()
        self.assertEqual("Test approve delete", changeset.comment)

    def test_reject_delete(self):
        activity = HistoricalActivity.objects.get(id=31)
        user = get_user_model().objects.get(username="administrator")
        activity.reject_delete(user=user, comment="Test reject delete")
        self.assertEqual(HistoricalActivity.STATUS_REJECTED, activity.fk_status_id)
        self.assertGreater(activity.changesets.count(), 0)
        changeset = activity.changesets.latest()
        self.assertEqual("Test reject delete", changeset.comment)

    def test_compare_attributes_to(self):
        current_version = HistoricalActivity.objects.get(id=21)
        previous_version = HistoricalActivity.objects.get(id=20)
        changed_attrs = current_version.compare_attributes_to(previous_version)
        expected = [(1, "production_size", "100", "3")]
        self.assertEqual(expected, changed_attrs)

    def test_update_public_activity_with_pending(self):
        activity = HistoricalActivity.objects.get(id=21)
        activity.update_public_activity(),
        self.assertEqual(HistoricalActivity.STATUS_OVERWRITTEN, activity.fk_status_id)

    def test_update_public_activity_with_to_delete(self):
        activity = HistoricalActivity.objects.get(id=60)
        activity.update_public_activity()
        self.assertEqual(HistoricalActivity.STATUS_DELETED, activity.fk_status_id)

    def test_update_public_activity_with_rejected(self):
        activity = HistoricalActivity.objects.get(id=50)
        activity.update_public_activity()
        self.assertEqual(HistoricalActivity.STATUS_REJECTED, activity.fk_status_id)

    def test_changeset_comment(self):
        ActivityChangeset.objects.create(
            fk_activity_id=31, fk_user_id=2, comment="Test changeset"
        )
        activity = HistoricalActivity.objects.get(id=31)
        comment = activity.changeset_comment
        self.assertEqual("Test changeset", comment)

    @patch("django.db.transaction.on_commit")
    def test_save(self, mock_on_commit):
        activity = HistoricalActivity.objects.get(id=21)
        # removing "update_elasticsearch=True" here, because it defaults to true
        activity.save()

        mock_on_commit.assert_called_once()
