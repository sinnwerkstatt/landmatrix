from django.contrib.auth import get_user_model
from django.test import TestCase
from datetime import datetime, timezone

from typing import Type
from apps.accounts.models import User
from apps.landmatrix.models.deal import Deal, DealVersion, DealWorkflowInfo
from apps.landmatrix.models.investor import (
    Investor,
    InvestorVersion,
    InvestorWorkflowInfo,
)
from apps.landmatrix.models.abstracts import DRAFT_STATUS, STATUS
from apps.landmatrix.models.country import Country

from .utils import (
    user_to_dict,
    workflowinfo_to_dict,
    deal_to_dict,
    version_to_dict,
)

UserModel: Type[User] = get_user_model()


FIRST_OF_JANUARY_2022 = datetime(2022, 1, 1, tzinfo=timezone.utc)
SECOND_OF_JANUARY_2022 = datetime(2022, 1, 2, tzinfo=timezone.utc)


class ToDictTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.maxDiff = None

        cls.AGATHA = UserModel.objects.create_user(
            id=1001,
            username="agatha",
            first_name="Agatha",
            last_name="Christie",
        )
        cls.WILLIAM = UserModel.objects.create_user(
            id=1002,
            username="willi",
            first_name="William",
            last_name="Shakespeare",
        )

    def test_user_to_dict(self):
        self.assertDictEqual(
            user_to_dict(self.AGATHA),
            {
                "id": 1001,
                "username": "agatha",
                "full_name": "Agatha Christie",
            },
        )

        self.assertIsNone(
            user_to_dict(None),
        )

    def test_deal_workflowinfos_to_dict(self):
        deal = Deal.objects.create(
            id=1000,
            created_at=FIRST_OF_JANUARY_2022,
        )
        version = DealVersion.objects.create(
            id=2000,
            created_at=FIRST_OF_JANUARY_2022,
            object=deal,
            serialized_data=deal.serialize_for_version(),
        )
        wfi = DealWorkflowInfo.objects.create(
            id=3000,
            timestamp=FIRST_OF_JANUARY_2022,
            deal=deal,
            deal_version=version,
            from_user=self.AGATHA,
            to_user=self.WILLIAM,
            draft_status_before=DRAFT_STATUS["DRAFT"],
            draft_status_after=DRAFT_STATUS["REVIEW"],
        )

        self.assertDictEqual(
            workflowinfo_to_dict(wfi),
            {
                "id": 3000,
                "from_user": {
                    "id": 1001,
                    "username": "agatha",
                    "full_name": "Agatha Christie",
                },
                "to_user": {
                    "id": 1002,
                    "username": "willi",
                    "full_name": "William Shakespeare",
                },
                "draft_status_before": DRAFT_STATUS["DRAFT"],
                "draft_status_after": DRAFT_STATUS["REVIEW"],
                "obj_version_id": 2000,
                "timestamp": FIRST_OF_JANUARY_2022,
                "comment": "",
                "resolved": False,
                "replies": [],
                "__typename": "DealWorkflowInfo",
            },
        )

    def test_investor_workflowinfos_to_dict(self):
        investor = Investor.objects.create(
            id=1000,
            created_at=FIRST_OF_JANUARY_2022,
        )
        version = InvestorVersion.objects.create(
            id=2000,
            created_at=FIRST_OF_JANUARY_2022,
            object=investor,
            serialized_data=investor.serialize_for_version(),
        )
        wfi = InvestorWorkflowInfo.objects.create(
            id=3000,
            timestamp=FIRST_OF_JANUARY_2022,
            investor=investor,
            investor_version=version,
            from_user=self.AGATHA,
            to_user=self.WILLIAM,
            draft_status_before=DRAFT_STATUS["DRAFT"],
            draft_status_after=DRAFT_STATUS["REVIEW"],
        )

        self.assertDictEqual(
            workflowinfo_to_dict(wfi),
            {
                "id": 3000,
                "from_user": {
                    "id": 1001,
                    "username": "agatha",
                    "full_name": "Agatha Christie",
                },
                "to_user": {
                    "id": 1002,
                    "username": "willi",
                    "full_name": "William Shakespeare",
                },
                "draft_status_before": DRAFT_STATUS["DRAFT"],
                "draft_status_after": DRAFT_STATUS["REVIEW"],
                "obj_version_id": 2000,
                "timestamp": FIRST_OF_JANUARY_2022,
                "comment": "",
                "resolved": False,
                "replies": [],
                "__typename": "InvestorWorkflowInfo",
            },
        )

    def test_deal_version_to_dict(self):
        deal = Deal.objects.create(
            id=1000,
        )
        version = DealVersion.objects.create(
            id=2000,
            created_at=FIRST_OF_JANUARY_2022,
            created_by=self.AGATHA,
            object=deal,
            serialized_data=deal.serialize_for_version(),
        )

        self.assertDictEqual(
            version_to_dict(version),
            {
                "id": 2000,
                "created_at": FIRST_OF_JANUARY_2022,
                "created_by": {
                    "id": 1001,
                    "username": "agatha",
                    "full_name": "Agatha Christie",
                },
                "modified_at": None,
                "modified_by": None,
            },
        )

    def test_investor_version_to_dict(self):
        investor = Investor.objects.create(
            id=1000,
        )
        version = InvestorVersion.objects.create(
            id=2000,
            created_at=FIRST_OF_JANUARY_2022,
            created_by=self.AGATHA,
            object=investor,
            serialized_data=investor.serialize_for_version(),
        )

        self.assertDictEqual(
            version_to_dict(version),
            {
                "id": 2000,
                "created_at": FIRST_OF_JANUARY_2022,
                "created_by": {
                    "id": 1001,
                    "username": "agatha",
                    "full_name": "Agatha Christie",
                },
                "modified_at": None,
                "modified_by": None,
            },
        )

    def test_deal_to_dict(self):
        ger = Country.objects.get(name="Germany")

        deal = Deal.objects.create(
            id=1000,
            country=ger,
            created_at=FIRST_OF_JANUARY_2022,
            created_by=self.AGATHA,
            status=STATUS["DRAFT"],
            draft_status=DRAFT_STATUS["DRAFT"],
        )
        version1 = DealVersion.objects.create(
            id=2000,
            created_at=FIRST_OF_JANUARY_2022,
            created_by=self.AGATHA,
            object=deal,
            serialized_data=deal.serialize_for_version(),
        )
        version2 = DealVersion.objects.create(
            id=2001,
            created_at=SECOND_OF_JANUARY_2022,
            created_by=self.WILLIAM,
            object=deal,
            serialized_data=deal.serialize_for_version(),
        )

        self.assertDictEqual(
            deal_to_dict(deal),
            {
                "id": 1000,
                "country_id": ger.id,
                "status": STATUS["DRAFT"],
                "draft_status": DRAFT_STATUS["DRAFT"],
                "created_at": FIRST_OF_JANUARY_2022,
                "created_by": {
                    "id": 1001,
                    "username": "agatha",
                    "full_name": "Agatha Christie",
                },
                "last_version": {
                    "id": 2001,
                    "created_at": SECOND_OF_JANUARY_2022,
                    "created_by": {
                        "id": 1002,
                        "username": "willi",
                        "full_name": "William Shakespeare",
                    },
                    "modified_at": None,
                    "modified_by": None,
                },
                "workflowinfos": [],
            },
        )

        wfi1_1 = DealWorkflowInfo.objects.create(
            id=3000,
            timestamp=FIRST_OF_JANUARY_2022,
            deal=deal,
            deal_version=version1,
            from_user=self.AGATHA,
            draft_status_before=DRAFT_STATUS["DRAFT"],
            draft_status_after=DRAFT_STATUS["REVIEW"],
        )
        wfi1_2 = DealWorkflowInfo.objects.create(
            id=3001,
            timestamp=FIRST_OF_JANUARY_2022,
            deal=deal,
            deal_version=version1,
            from_user=self.AGATHA,
            draft_status_before=DRAFT_STATUS["REVIEW"],
            draft_status_after=DRAFT_STATUS["ACTIVATION"],
        )
        wfi2_1 = DealWorkflowInfo.objects.create(
            id=3002,
            timestamp=SECOND_OF_JANUARY_2022,
            deal=deal,
            deal_version=version2,
            from_user=self.AGATHA,
            draft_status_before=DRAFT_STATUS["DRAFT"],
            draft_status_after=DRAFT_STATUS["REVIEW"],
        )
        wfi2_2 = DealWorkflowInfo.objects.create(
            id=3003,
            timestamp=SECOND_OF_JANUARY_2022,
            deal=deal,
            deal_version=version2,
            from_user=self.AGATHA,
            draft_status_before=DRAFT_STATUS["REVIEW"],
            draft_status_after=DRAFT_STATUS["ACTIVATION"],
        )

        self.assertListEqual(
            deal_to_dict(deal)["workflowinfos"],
            list(map(workflowinfo_to_dict, [wfi1_1, wfi1_2, wfi2_1, wfi2_2])),
        )
