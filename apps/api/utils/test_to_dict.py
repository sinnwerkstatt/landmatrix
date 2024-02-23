# from datetime import datetime, timezone
# from typing import Type
#
# from django.contrib.auth import get_user_model
# from django.test import TestCase
#
# from apps.accounts.models import User
# from apps.landmatrix.models.abstracts import DRAFT_STATUS, STATUS
# from apps.landmatrix.models.country import Country
# from apps.landmatrix.models.deal import DealOld, DealVersion, DealWorkflowInfoOld
#
# from .to_dict import deal_to_dict
#
# UserModel: Type[User] = get_user_model()
#
#
# FIRST_OF_JANUARY_2022 = datetime(2022, 1, 1, tzinfo=timezone.utc)
# SECOND_OF_JANUARY_2022 = datetime(2022, 1, 2, tzinfo=timezone.utc)
#
#
# class ToDictTestCase(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         cls.maxDiff = None
#
#         cls.AGATHA = UserModel.objects.create(
#             id=1001,
#             username="agatha",
#             first_name="Agatha",
#             last_name="Christie",
#         )
#         cls.WILLIAM = UserModel.objects.create(
#             id=1002,
#             username="willi",
#             first_name="William",
#             last_name="Shakespeare",
#         )
#
#     def test_deal_to_dict(self):
#         ger = Country.objects.get(name="Germany")
#         # lookups = create_lookups()
#
#         deal = DealOld.objects.create(
#             id=1000,
#             country=ger,
#             created_at=FIRST_OF_JANUARY_2022,
#             created_by=self.AGATHA,
#             status=STATUS["DRAFT"],
#             draft_status=DRAFT_STATUS["DRAFT"],
#         )
#         version1 = DealVersion.objects.create(
#             id=2000,
#             created_at=FIRST_OF_JANUARY_2022,
#             created_by=self.AGATHA,
#             object=deal,
#             serialized_data=deal.serialize_for_version(),
#         )
#         version2 = DealVersion.objects.create(
#             id=2001,
#             created_at=SECOND_OF_JANUARY_2022,
#             created_by=self.WILLIAM,
#             object=deal,
#             serialized_data=deal.serialize_for_version(),
#         )
#         DealWorkflowInfoOld.objects.create(
#             id=3000,
#             timestamp=FIRST_OF_JANUARY_2022,
#             deal=deal,
#             deal_version=version1,
#             from_user=self.AGATHA,
#             draft_status_before=DRAFT_STATUS["DRAFT"],
#             draft_status_after=DRAFT_STATUS["REVIEW"],
#         )
#         DealWorkflowInfoOld.objects.create(
#             id=3001,
#             timestamp=SECOND_OF_JANUARY_2022,
#             deal=deal,
#             deal_version=version2,
#             from_user=self.WILLIAM,
#             to_user=self.AGATHA,
#             resolved=True,
#             draft_status_before=DRAFT_STATUS["REVIEW"],
#             draft_status_after=DRAFT_STATUS["REVIEW"],
#         )
#
#         self.assertDictEqual(
#             deal_to_dict(deal),  # noqa
#             {
#                 "id": 1000,
#                 "country": {
#                     "id": 276,
#                     "name": "Germany",
#                     "region": {
#                         "id": 150,
#                         "name": "Eastern Europe",
#                     },
#                 },
#                 "status": STATUS["DRAFT"],
#                 "draft_status": DRAFT_STATUS["DRAFT"],
#                 "created_at": FIRST_OF_JANUARY_2022,
#                 "created_by": {
#                     "id": 1001,
#                     "username": "agatha",
#                     "full_name": "Agatha Christie",
#                 },
#                 "modified_at": SECOND_OF_JANUARY_2022,
#                 "modified_by": {
#                     "id": 1002,
#                     "username": "willi",
#                     "full_name": "William Shakespeare",
#                 },
#                 "workflowinfos": [
#                     {
#                         "__typename": "DealWorkflowInfoOld",
#                         "comment": "",
#                         "draft_status_before": DRAFT_STATUS["DRAFT"],
#                         "draft_status_after": DRAFT_STATUS["REVIEW"],
#                         "from_user": {
#                             "full_name": "Agatha Christie",
#                             "id": 1001,
#                             "username": "agatha",
#                         },
#                         "id": 3000,
#                         "replies": [],
#                         "resolved": False,
#                         "timestamp": FIRST_OF_JANUARY_2022,
#                         "to_user": None,
#                     },
#                     {
#                         "__typename": "DealWorkflowInfoOld",
#                         "comment": "",
#                         "draft_status_before": DRAFT_STATUS["REVIEW"],
#                         "draft_status_after": DRAFT_STATUS["REVIEW"],
#                         "from_user": {
#                             "id": 1002,
#                             "username": "willi",
#                             "full_name": "William Shakespeare",
#                         },
#                         "to_user": {
#                             "full_name": "Agatha Christie",
#                             "id": 1001,
#                             "username": "agatha",
#                         },
#                         "id": 3001,
#                         "replies": [],
#                         "resolved": True,
#                         "timestamp": SECOND_OF_JANUARY_2022,
#                     },
#                 ],
#                 "deal_size": 0,
#                 "fully_updated_at": None,
#             },
#         )
