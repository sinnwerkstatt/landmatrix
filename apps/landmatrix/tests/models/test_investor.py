from datetime import datetime
from unittest.mock import patch

import pytz
from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.grid.tests.views.base import BaseDealTestCase
from apps.landmatrix.models.investor import *
from apps.landmatrix.tests.mixins import (
    ActivitiesFixtureMixin,
    InvestorsFixtureMixin,
    InvestorActivityInvolvementsFixtureMixin,
    InvestorVentureInvolvementsFixtureMixin,
)


class InvestorQuerySetTestCase(InvestorsFixtureMixin, TestCase):

    inv_fixtures = [
        {
            "id": 1,
            "investor_identifier": 1,
            "fk_status_id": 1,
            "name": "Test Investor #1",
        },
        {"id": 2, "investor_identifier": 2, "name": "Test Investor #2"},
        {
            "id": 3,
            "investor_identifier": 2,
            "fk_status_id": 3,
            "name": "Test Investor #2",
        },
        {
            "id": 4,
            "investor_identifier": 3,
            "fk_status_id": 4,
            "name": "Test Investor #3",
        },
        {
            "id": 5,
            "investor_identifier": 4,
            "fk_status_id": 5,
            "name": "Test Investor #4",
        },
        {
            "id": 6,
            "investor_identifier": 5,
            "fk_status_id": 6,
            "name": "Test Investor #5",
        },
        {
            "id": 7,
            "investor_identifier": 6,
            "fk_status_id": 2,
            "name": "Test Investor #6",
        },
        {
            "id": 8,
            "investor_identifier": 6,
            "fk_status_id": 1,
            "name": "Test Investor #6",
        },
    ]

    fixtures = ["countries_and_regions", "users_and_groups", "status"]

    def setUp(self):
        super().setUp()
        self.qs = HistoricalInvestor.objects

    def test_public_with_user(self):
        user = get_user_model().objects.get(username="reporter")
        qs = self.qs.public(user=user)
        self.assertGreater(qs.count(), 0)

    def test_public_without_user(self):
        qs = self.qs.public()
        self.assertGreater(qs.count(), 0)
        statuses = set(InvestorBase.PUBLIC_STATUSES)
        for status in set(qs.values_list("fk_status_id", flat=True)):
            self.assertIn(status, statuses)

    def test_public_or_deleted(self):
        qs = self.qs.public_or_deleted()
        self.assertGreater(qs.count(), 0)
        statuses = InvestorBase.PUBLIC_STATUSES + (InvestorBase.STATUS_DELETED,)
        for status in set(qs.values_list("fk_status_id", flat=True)):
            self.assertIn(status, statuses)

    def test_public_or_deleted_with_reporter(self):
        user = get_user_model().objects.get(username="reporter-2")
        qs = self.qs.public_or_deleted(user=user)
        self.assertGreater(qs.count(), 0)
        statuses = InvestorBase.PUBLIC_STATUSES + (InvestorBase.STATUS_DELETED,)
        for status in set(qs.values_list("fk_status_id", flat=True)):
            self.assertIn(status, statuses)

    def test_public_or_pending(self):
        qs = self.qs.public_or_pending()
        self.assertGreater(qs.count(), 0)
        statuses = InvestorBase.PUBLIC_STATUSES + (InvestorBase.STATUS_PENDING,)
        for status in set(qs.values_list("fk_status_id", flat=True)):
            self.assertIn(status, statuses)

    def test_public_deleted_or_pending(self):
        qs = self.qs.public_deleted_or_pending()
        self.assertGreater(qs.count(), 0)
        statuses = InvestorBase.PUBLIC_STATUSES + (
            InvestorBase.STATUS_DELETED,
            InvestorBase.STATUS_PENDING,
        )
        for status in set(qs.values_list("fk_status_id", flat=True)):
            self.assertIn(status, statuses)

    def test_pending(self):
        qs = self.qs.pending()
        self.assertGreater(qs.count(), 0)
        statuses = (InvestorBase.STATUS_PENDING, InvestorBase.STATUS_TO_DELETE)
        for status in set(qs.values_list("fk_status_id", flat=True)):
            self.assertIn(status, statuses)

    def test_pending_only(self):
        qs = self.qs.pending_only()
        self.assertGreater(qs.count(), 0)
        self.assertEqual(
            {InvestorBase.STATUS_PENDING},
            set(qs.values_list("fk_status_id", flat=True)),
        )

    def test_active(self):
        qs = self.qs.active()
        self.assertGreater(qs.count(), 0)
        self.assertEqual(
            {InvestorBase.STATUS_ACTIVE}, set(qs.values_list("fk_status_id", flat=True))
        )

    def test_overwritten(self):
        qs = self.qs.overwritten()
        self.assertGreater(qs.count(), 0)
        self.assertEqual(
            {InvestorBase.STATUS_OVERWRITTEN},
            set(qs.values_list("fk_status_id", flat=True)),
        )

    def test_to_delete(self):
        qs = self.qs.to_delete()
        self.assertGreater(qs.count(), 0)
        self.assertEqual(
            {InvestorBase.STATUS_TO_DELETE},
            set(qs.values_list("fk_status_id", flat=True)),
        )

    def test_deleted(self):
        qs = self.qs.deleted()
        self.assertGreater(qs.count(), 0)
        self.assertEqual(
            {InvestorBase.STATUS_DELETED},
            set(qs.values_list("fk_status_id", flat=True)),
        )

    def test_rejected(self):
        qs = self.qs.rejected()
        self.assertGreater(qs.count(), 0)
        self.assertEqual(
            {InvestorBase.STATUS_REJECTED},
            set(qs.values_list("fk_status_id", flat=True)),
        )


class InvestorBaseTestCase(
    ActivitiesFixtureMixin,
    InvestorsFixtureMixin,
    InvestorActivityInvolvementsFixtureMixin,
    InvestorVentureInvolvementsFixtureMixin,
    BaseDealTestCase,
):

    act_fixtures = [
        {"id": 10, "activity_identifier": 1, "attributes": {}},
        {"id": 20, "activity_identifier": 2, "attributes": {}},
        {"id": 21, "activity_identifier": 2, "fk_status_id": 1, "attributes": {}},
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
        {"id": 30, "investor_identifier": 3, "name": "Test Investor #3"},
        {
            "id": 31,
            "investor_identifier": 3,
            "fk_status_id": 6,
            "name": "Test Investor #3",
            "history_date": datetime(2000, 1, 2, 0, 0, tzinfo=pytz.utc),
        },
        {"id": 40, "investor_identifier": 4, "name": "Test Investor #4"},
        {
            "id": 50,
            "investor_identifier": 5,
            "fk_status_id": 5,
            "name": "Test Investor #5",
        },
        {
            "id": 60,
            "investor_identifier": 6,
            "fk_status_id": 6,
            "name": "Test Investor #6",
        },
        {
            "id": 70,
            "investor_identifier": 7,
            "fk_status_id": 2,
            "name": "Test Investor #7",
        },
        {
            "id": 80,
            "investor_identifier": 8,
            "fk_status_id": 2,
            "name": "Test Investor #8",
        },
    ]
    act_inv_fixtures = {"10": "10", "20": "20", "21": "20"}
    inv_inv_fixtures = [
        {"fk_venture_id": "10", "fk_investor_id": "30"},
        {"fk_venture_id": "40", "fk_investor_id": "40"},
        {"fk_venture_id": "30", "fk_investor_id": "70"},
        {"fk_venture_id": "10", "fk_investor_id": "80", "role": "IN"},
    ]

    def test_get_next_investor_identifier(self):
        investor_identifier = HistoricalInvestor.get_next_investor_identifier()
        self.assertGreater(investor_identifier, 1)
        self.assertNotEqual(
            investor_identifier, InvestorBase.INVESTOR_IDENTIFIER_DEFAULT
        )

    def test_save(self):
        investor = HistoricalInvestor(
            id=90,
            fk_status_id=HistoricalInvestor.STATUS_ACTIVE,
            investor_identifier=None,
        )
        investor.save()
        self.assertIsNotNone(investor.investor_identifier)
        self.assertNotEqual(
            investor.investor_identifier, InvestorBase.INVESTOR_IDENTIFIER_DEFAULT
        )
        self.assertEqual(f"Unknown (#{investor.investor_identifier})", investor.name)

    def test_save_with_operating_company(self):
        investor = HistoricalInvestor.objects.create(
            id=90, fk_status_id=HistoricalInvestor.STATUS_ACTIVE
        )
        investor.involvements.create(
            fk_activity_id=10,
            fk_status_id=HistoricalInvestorActivityInvolvement.STATUS_ACTIVE,
        )
        investor.save()
        self.assertIsNotNone(investor.investor_identifier)
        self.assertNotEqual(
            investor.investor_identifier, InvestorBase.INVESTOR_IDENTIFIER_DEFAULT
        )
        self.assertEqual(
            f"Unknown operating company (#{investor.investor_identifier})",
            investor.name,
        )

    def test_save_with_parent_company(self):
        investor = HistoricalInvestor.objects.create(
            id=90, fk_status_id=HistoricalInvestor.STATUS_ACTIVE
        )
        investor.investors.create(
            fk_venture_id=10, role=HistoricalInvestorVentureInvolvement.STAKEHOLDER_ROLE
        )
        investor.save()
        self.assertIsNotNone(investor.investor_identifier)
        self.assertNotEqual(
            investor.investor_identifier, InvestorBase.INVESTOR_IDENTIFIER_DEFAULT
        )
        self.assertEqual(
            f"Unknown parent company (#{investor.investor_identifier})", investor.name
        )

    def test_save_with_tertiary_investor_lender(self):
        investor = HistoricalInvestor.objects.create(
            id=90, fk_status_id=HistoricalInvestor.STATUS_ACTIVE
        )
        investor.investors.create(
            fk_venture_id=10, role=HistoricalInvestorVentureInvolvement.INVESTOR_ROLE
        )
        investor.save()
        self.assertIsNotNone(investor.investor_identifier)
        self.assertNotEqual(
            investor.investor_identifier, InvestorBase.INVESTOR_IDENTIFIER_DEFAULT
        )
        self.assertEqual(
            f"Unknown tertiary investor/lender (#{investor.investor_identifier})",
            investor.name,
        )

    def test_get_history(self):
        investor = HistoricalInvestor.objects.get(id=31)
        user = get_user_model().objects.get(username="reporter")
        self.assertGreater(len(investor.get_history(user=user)), 0)

    def test_is_operating_company(self):
        investor = HistoricalInvestor.objects.get(id=10)
        self.assertEqual(True, investor.is_operating_company)

    def test_is_parent_company(self):
        investor = HistoricalInvestor.objects.get(id=30)
        self.assertEqual(True, investor.is_parent_company)

    def test_is_parent_company_without_involvements(self):
        investor = HistoricalInvestor.objects.get(id=30)
        investor.investors.all().delete()
        self.assertEqual(False, investor.is_parent_company)

    def test_is_parent_investor(self):
        investor = HistoricalInvestor.objects.get(id=80)
        self.assertEqual(True, investor.is_parent_investor)

    def test_is_parent_investor_without_involvements(self):
        investor = HistoricalInvestor.objects.get(id=80)
        investor.investors.all().delete()
        self.assertEqual(False, investor.is_parent_investor)

    def test_get_latest_investor(self):
        investor = HistoricalInvestor.get_latest_investor(investor_identifier=3)
        self.assertEqual(31, investor.id)

    def test_get_latest_active_investor(self):
        investor = HistoricalInvestor.get_latest_active_investor(investor_identifier=3)
        self.assertEqual(30, investor.id)

    def test_get_top_investors(self):
        investor = HistoricalInvestor.objects.get(id=10)
        top_investor = HistoricalInvestor.objects.get(id=70)
        self.assertEqual({top_investor}, set(investor.get_top_investors()))

    def test_get_top_investors_with_self_reference(self):
        investor = HistoricalInvestor.objects.get(id=40)
        self.assertEqual({investor}, set(investor.get_top_investors()))

    def test_format_investors(self):
        investor = HistoricalInvestor.objects.get(id=10)
        self.assertEqual(
            "Test Investor 1#1#Cambodia", investor.format_investors([investor])
        )

    def test_get_deal_count(self):
        investor = HistoricalInvestor.objects.get(id=10)
        self.assertGreater(investor.get_deal_count(), 0)

    def test_get_roles(self):
        investor = HistoricalInvestor.objects.get(id=10)
        roles = {InvestorBase.ROLE_OPERATING_COMPANY}
        self.assertEqual(roles, set(investor.get_roles()))

    def test_get_latest(self):
        investor = HistoricalInvestor.objects.get(id=30)
        user = get_user_model().objects.get(username="reporter")
        latest = investor.get_latest(user=user)
        self.assertEqual(31, latest.id)

    def test_is_editable_old_version_with_superuser(self):
        investor = HistoricalInvestor.objects.get(id=30)
        user = get_user_model().objects.get(username="superuser")
        self.assertEqual(True, investor.is_editable(user=user))

    def test_is_editable_old_version_with_reporter(self):
        investor = HistoricalInvestor.objects.get(id=30)
        user = get_user_model().objects.get(username="reporter")
        self.assertEqual(False, investor.is_editable(user=user))

    def test_is_editable_new_version_with_reporter(self):
        investor = HistoricalInvestor.objects.get(id=31)
        user = get_user_model().objects.get(username="reporter-2")
        self.assertEqual(False, investor.is_editable(user=user))

    def test_is_editable_new_version_with_author(self):
        investor = HistoricalInvestor.objects.get(id=31)
        user = get_user_model().objects.get(username="reporter")
        self.assertEqual(False, investor.is_editable(user=user))

    def test_is_editable_new_version_with_rejected(self):
        investor = HistoricalInvestor.objects.get(id=31)
        investor.fk_status_id = HistoricalInvestor.STATUS_REJECTED
        investor.save()
        user = get_user_model().objects.get(username="reporter-2")
        self.assertEqual(False, investor.is_editable(user=user))

    def test_is_editable_new_version_with_editor(self):
        investor = HistoricalInvestor.objects.get(id=31)
        user = get_user_model().objects.get(username="editor")
        self.assertEqual(True, investor.is_editable(user=user))

    def test_is_editable_new_version_without_user(self):
        investor = HistoricalInvestor.objects.get(id=31)
        self.assertEqual(False, investor.is_editable(user=None))


class HistoricalInvestorQuerySetTestCase(InvestorsFixtureMixin, TestCase):

    inv_fixtures = [
        {"id": 1, "investor_identifier": 1, "name": "Test Investor #1"},
        {"id": 2, "investor_identifier": 2, "name": "Test Investor #2"},
        {
            "id": 3,
            "investor_identifier": 2,
            "fk_status_id": 1,
            "name": "Test Investor #2",
        },
    ]

    fixtures = ["countries_and_regions", "users_and_groups", "status"]

    def setUp(self):
        super().setUp()
        self.qs = HistoricalInvestor.objects

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
        self.assertGreater(len(latest_ids), 0)

    def test_latest_only(self):
        qs = self.qs.latest_only()
        self.assertGreater(qs.count(), 0)

    def test_latest_public_or_pending(self):
        qs = self.qs.latest_public_or_pending()
        self.assertGreater(qs.count(), 0)

    def test_latest_public_and_pending(self):
        qs = self.qs.latest_public_and_pending()
        self.assertGreater(qs.count(), 0)


class HistoricalInvestorTestCase(
    InvestorsFixtureMixin, InvestorVentureInvolvementsFixtureMixin, BaseDealTestCase
):

    inv_fixtures = [
        {"id": 10, "investor_identifier": 1, "name": "Test Investor #1"},
        {"id": 20, "investor_identifier": 2, "name": "Test Investor #2"},
        {
            "id": 21,
            "investor_identifier": 2,
            "fk_status_id": 1,
            "name": "Test Investor #2",
        },
        {"id": 30, "investor_identifier": 3, "name": "Test Investor #3"},
        {
            "id": 31,
            "investor_identifier": 3,
            "fk_status_id": 6,
            "name": "Test Investor #3",
        },
        {"id": 40, "investor_identifier": 4, "name": "Test Investor #4"},
        {
            "id": 50,
            "investor_identifier": 5,
            "fk_status_id": 5,
            "name": "Test Investor #5",
        },
        {
            "id": 60,
            "investor_identifier": 6,
            "fk_status_id": 6,
            "name": "Test Investor #6",
        },
    ]
    inv_inv_fixtures = [
        {"fk_venture_id": "10", "fk_investor_id": "30"},
        {"fk_venture_id": "40", "fk_investor_id": "40"},
    ]

    def test_approve_change(self):
        investor = HistoricalInvestor.objects.get(id=21)
        user = get_user_model().objects.get(username="administrator")
        investor.approve_change(user=user, comment="Test approve change")
        self.assertEqual(HistoricalInvestor.STATUS_OVERWRITTEN, investor.fk_status_id)

    def test_reject_change(self):
        investor = HistoricalInvestor.objects.get(id=21)
        user = get_user_model().objects.get(username="administrator")
        investor.reject_change(user=user, comment="Test reject change")
        self.assertEqual(HistoricalInvestor.STATUS_REJECTED, investor.fk_status_id)

    def test_approve_delete(self):
        investor = HistoricalInvestor.objects.get(id=31)
        user = get_user_model().objects.get(username="administrator")
        investor.approve_delete(user=user, comment="Test approve delete")
        self.assertEqual(HistoricalInvestor.STATUS_DELETED, investor.fk_status_id)

    def test_reject_delete(self):
        investor = HistoricalInvestor.objects.get(id=31)
        user = get_user_model().objects.get(username="administrator")
        investor.reject_delete(user=user, comment="Test reject delete")
        self.assertEqual(HistoricalInvestor.STATUS_REJECTED, investor.fk_status_id)

    def test_get_top_investors(self):
        investor = HistoricalInvestor.objects.get(id=10)
        top_investor = HistoricalInvestor.objects.get(id=30)
        self.assertEqual({top_investor}, set(investor.get_top_investors()))

    def test_get_top_investors_with_self_reference(self):
        investor = HistoricalInvestor.objects.get(id=40)
        self.assertEqual({investor}, set(investor.get_top_investors()))

    def test_update_public_investor_with_pending(self):
        investor = HistoricalInvestor.objects.get(id=31)
        investor.update_public_investor()
        # self.assertEqual(HistoricalInvestor.STATUS_OVERWRITTEN, investor.fk_status_id)

    def test_update_public_investor_with_to_delete(self):
        investor = HistoricalInvestor.objects.get(id=60)
        investor.update_public_investor()
        self.assertEqual(HistoricalInvestor.STATUS_DELETED, investor.fk_status_id)

    def test_update_public_investor_with_rejected(self):
        investor = HistoricalInvestor.objects.get(id=50)
        investor.update_public_investor()
        self.assertEqual(HistoricalInvestor.STATUS_REJECTED, investor.fk_status_id)

    def test_update_current_involvements(self):
        hinvestor = HistoricalInvestor.objects.get(id=31)
        hinvestor.update_current_involvements()

        hinvolvements = (
            HistoricalInvestorActivityInvolvement.objects.for_current_activities()
        )
        hinvolvements = hinvolvements.filter(
            fk_investor__investor_identifier=hinvestor.investor_identifier
        )
        hinvolvements = hinvolvements.exclude(fk_investor_id=hinvestor.id)
        self.assertEqual(0, hinvolvements.count())

    @patch("django.db.transaction.on_commit")
    def test_save(self, mock_on_commit):
        investor = HistoricalInvestor.objects.get(id=30)
        # removing "update_elasticsearch=True" here, because it defaults to true
        investor.save()
        mock_on_commit.assert_called_once()


class InvestorVentureQuerySetTestCase(
    InvestorsFixtureMixin, InvestorVentureInvolvementsFixtureMixin, TestCase
):

    inv_fixtures = [
        {"id": 10, "investor_identifier": 1, "name": "Test Investor #1"},
        {"id": 20, "investor_identifier": 2, "name": "Test Investor #2"},
        {"id": 30, "investor_identifier": 3, "name": "Test Investor #3"},
    ]
    inv_inv_fixtures = [
        {
            "fk_venture_id": "10",
            "fk_investor_id": "20",
            "role": "ST",
            "fk_status_id": 2,
        },
        {
            "fk_venture_id": "10",
            "fk_investor_id": "20",
            "role": "IN",
            "fk_status_id": 2,
        },
    ]

    def setUp(self):
        super().setUp()
        self.qs = HistoricalInvestorVentureInvolvement.objects

    def test_active(self):
        qs = self.qs.active()
        self.assertGreater(qs.count(), 0)
        statuses = HistoricalInvestorVentureInvolvement.PUBLIC_STATUSES + (
            HistoricalInvestorVentureInvolvement.STATUS_PENDING,
        )
        for status in set(qs.values_list("fk_status_id", flat=True)):
            self.assertIn(status, statuses)

    def test_latest_only(self):
        qs = self.qs.latest_only()
        self.assertGreater(qs.count(), 0)

    def test_stakeholders(self):
        qs = self.qs.stakeholders()
        self.assertGreater(qs.count(), 0)
        self.assertEqual(
            {HistoricalInvestorVentureInvolvement.STAKEHOLDER_ROLE},
            set(qs.values_list("role", flat=True)),
        )

    def test_investors(self):
        qs = self.qs.investors()
        self.assertGreater(qs.count(), 0)
        self.assertEqual(
            {HistoricalInvestorVentureInvolvement.INVESTOR_ROLE},
            set(qs.values_list("role", flat=True)),
        )

    def test_parent_companies(self):
        qs = self.qs.parent_companies()
        self.assertGreater(qs.count(), 0)
        self.assertEqual(
            {HistoricalInvestorVentureInvolvement.STAKEHOLDER_ROLE},
            set(qs.values_list("role", flat=True)),
        )

    def test_tertiary_investors(self):
        qs = self.qs.tertiary_investors()
        self.assertGreater(qs.count(), 0)
        self.assertEqual(
            {HistoricalInvestorVentureInvolvement.INVESTOR_ROLE},
            set(qs.values_list("role", flat=True)),
        )


class InvestorActivityInvolvementManagerTestCase(
    ActivitiesFixtureMixin,
    InvestorsFixtureMixin,
    InvestorActivityInvolvementsFixtureMixin,
    TestCase,
):

    act_fixtures = [{"id": 10, "activity_identifier": 1, "attributes": {}}]
    inv_fixtures = [{"id": 10, "investor_identifier": 1, "name": "Test Investor #1"}]
    act_inv_fixtures = {"10": "10"}

    def setUp(self):
        super().setUp()
        self.qs = HistoricalInvestorActivityInvolvement.objects

    def test_for_current_activities(self):
        involvements = self.qs.for_current_activities()
        self.assertGreater(involvements.count(), 0)
