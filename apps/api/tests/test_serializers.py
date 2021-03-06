from collections import OrderedDict

from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from rest_framework_gis.fields import GeoJsonDict

from apps.api.serializers import *
from apps.landmatrix.tests.mixins import (
    InvestorVentureInvolvementsFixtureMixin,
    InvestorsFixtureMixin,
)
from apps.wagtailcms.models import RegionPage


class UserSerializerTestCase(TestCase):
    fixtures = ["countries_and_regions", "users_and_groups"]

    def test_get_full_name(self):
        user = get_user_model().objects.get(username="reporter")
        serializer = UserSerializer(instance=user)
        self.assertEqual("Reporter Reporter", serializer.get_full_name(user))


class RegionSerializerTestCase(TestCase):
    fixtures = ["countries_and_regions"]

    def test_to_representation(self):
        region_page = RegionPage.objects.create(
            title="Africa Page", region_id=2, path="/", depth=0
        )
        serializer = RegionSerializer(instance=region_page)
        self.assertEqual(
            [2, "africa", "Africa Page"], serializer.to_representation(region_page)
        )


class DealLocationSerializerTestCase(TestCase):
    def test_to_representation(self):
        location = {
            "point_lat": 0,
            "point_lon": 0,
            "contract_area": "POINT(0 1)",
            "intended_area": GEOSGeometry("POINT(0 1)"),
            "production_area": GEOSGeometry("POINT(0 1)"),
        }
        serializer = DealLocationSerializer()
        location_repr = serializer.to_representation(location)
        self.assertEqual("0.00000000", location_repr.get("point_lat"))
        self.assertEqual(
            GeoJsonDict([("type", "Point"), ("coordinates", [0.0, 1.0])]),
            location_repr.get("contract_area"),
        )
        self.assertEqual(
            GeoJsonDict([("type", "Point"), ("coordinates", [0.0, 1.0])]),
            location_repr.get("intended_area"),
        )


class DealSerializerTestCase(TestCase):
    def test_to_representation(self):
        location = {
            "deal_id": "1",
            "intention": "test",
            "contract_size": "1000",
            "intended_size": "2000.0",
            "production_size": "not-a-number",
            "investor": "test",
            "point_lat": "0",
            "point_lon": "0",
            "contract_area": "POINT(0 1)",
            "intended_area": "POINT(0 1)",
            "production_area": "POINT(0 1)",
        }
        serializer = DealSerializer()
        location_repr = serializer.to_representation(location)
        self.assertEqual(1, location_repr.get("deal_id"))
        self.assertEqual(1000, location_repr.get("contract_size"))
        self.assertEqual(2000, location_repr.get("intended_size"))
        self.assertEqual(None, location_repr.get("production_size"))
        self.assertEqual(
            [
                OrderedDict(
                    [
                        ("point_lat", "0.00000000"),
                        ("point_lon", "0.00000000"),
                        (
                            "contract_area",
                            GeoJsonDict(
                                [("type", "Point"), ("coordinates", [0.0, 1.0])]
                            ),
                        ),
                        (
                            "intended_area",
                            GeoJsonDict(
                                [("type", "Point"), ("coordinates", [0.0, 1.0])]
                            ),
                        ),
                        (
                            "production_area",
                            GeoJsonDict(
                                [("type", "Point"), ("coordinates", [0.0, 1.0])]
                            ),
                        ),
                    ]
                )
            ],
            location_repr.get("locations"),
        )


class HistoricalInvestorNetworkSerializerTestCase(
    InvestorsFixtureMixin, InvestorVentureInvolvementsFixtureMixin, TestCase
):
    inv_fixtures = [
        {"id": 10, "investor_identifier": 1, "name": "Test Investor #1"},
        {"id": 20, "investor_identifier": 2, "name": "Test Investor #2"},
    ]
    inv_inv_fixtures = [{"fk_venture_id": "10", "fk_investor_id": "20"}]

    def test_to_representation(self):
        investor = HistoricalInvestor.objects.get(id=10)
        serializer = DealInvestorNetworkSerializer(user=AnonymousUser())
        investor_network = serializer.to_representation(investor)
        self.assertEqual("I1", investor_network.get("id"))
        self.assertEqual(1, investor_network.get("identifier"))
        self.assertEqual("Test Investor #1", investor_network.get("name"))
        self.assertEqual("Cambodia", investor_network.get("country"))
        self.assertEqual("Private company", investor_network.get("classification"))
        self.assertEqual("/legacy/investor/1/", investor_network.get("url"))
        investors = investor_network.get("investors")
        self.assertIsInstance(investors, (tuple, list))
        self.assertEqual(1, len(investors))
        self.assertEqual("I2", investors[0].get("id"))
        self.assertEqual(2, investors[0].get("identifier"))
        self.assertEqual("Test Investor #2", investors[0].get("name"))
        self.assertEqual("Cambodia", investors[0].get("country"))
        self.assertEqual("Private company", investors[0].get("classification"))
        self.assertEqual("/legacy/investor/2/", investors[0].get("url"))
