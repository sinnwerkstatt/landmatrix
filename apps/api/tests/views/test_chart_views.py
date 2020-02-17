from decimal import Decimal

from django.core.management import call_command
from django.http import QueryDict
from django.test import TestCase, override_settings
from django.urls import reverse

from apps.api.elasticsearch import es_save
from apps.grid.forms.choices import INTENTION_MINING, NATURE_CONCESSION, NATURE_CONTRACT_FARMING, intention_choices, \
    INTENTION_BIOFUELS, intention_agriculture_choices, intention_forestry_choices, INTENTION_TIMBER_PLANTATION
from apps.landmatrix.models import Region, AgriculturalProduce, Crop, Animal, Mineral
from apps.landmatrix.models.activity import ActivityBase
from apps.landmatrix.tests.mixins import ActivitiesFixtureMixin, InvestorsFixtureMixin, \
    InvestorActivityInvolvementsFixtureMixin, InvestorVentureInvolvementsFixtureMixin, ElasticSearchFixtureMixin


class ChartViewTestCase(ElasticSearchFixtureMixin,
                        TestCase,
                        ActivitiesFixtureMixin,
                        InvestorsFixtureMixin,
                        InvestorActivityInvolvementsFixtureMixin,
                        InvestorVentureInvolvementsFixtureMixin):

    act_fixtures = [
    ]
    inv_fixtures = [
        {"id": 1},
        {"id": 2}
    ]
    act_inv_fixtures = {
    }
    inv_inv_fixtures = [
        {"fk_venture_id": "1", "fk_investor_id": "2"}
    ]


class NegotiationStatusChartViewTestCase(ChartViewTestCase):

    @classmethod
    def create_fixture(cls):
        cls.act_fixtures = []
        cls.act_inv_fixtures = {}
        for value, label in ActivityBase.NEGOTIATION_STATUS_CHOICES:
            if not value:
                continue
            id = len(cls.act_fixtures) + 1
            cls.act_fixtures.append({
                "id": id,
                "attributes": {
                    "target_country": {"value": "104"},
                    "intended_size": {"value": "1000"},
                    "contract_size": {"value": "1000"},
                    "production_size": {"value": "1000"},
                    "type": {"value": "Media report"},
                    "negotiation_status": {"value": value},  # Negotiation status tests
                    "intention": {"value": INTENTION_MINING},  # Mining tests
                    "nature": [
                        {"value": NATURE_CONCESSION},  # Logging tests
                        {"value": NATURE_CONTRACT_FARMING}  # Contract farming tests
                    ]
                }
            })
            cls.act_inv_fixtures[str(id)] = "1"

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_negotiation_status_list_view(self):
        response = self.client.get(reverse("negotiation_status_api"))
        self.assertEqual(200, response.status_code)
        response_dict = dict((d["name"], d) for d in response.data)
        for value, label in ActivityBase.NEGOTIATION_STATUS_CHOICES:
            if not value:
                continue
            self.assertEqual(1, response_dict[label]["deals"])
            self.assertEqual(1000, response_dict[label]["hectares"])

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_resource_extraction_view(self):
        response = self.client.get(reverse("resource_extraction_api"))
        self.assertEqual(200, response.status_code)
        response_dict = dict((d["name"], d) for d in response.data)
        for value, label in ActivityBase.NEGOTIATION_STATUS_CHOICES:
            if not value:
                continue
            self.assertEqual(1, response_dict[value]["deals"])
            self.assertEqual(1000, response_dict[value]["hectares"])

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_logging_view(self):
        response = self.client.get(reverse("logging_api"))
        self.assertEqual(200, response.status_code)
        response_dict = dict((d["name"], d) for d in response.data)
        for value, label in ActivityBase.NEGOTIATION_STATUS_CHOICES:
            if not value:
                continue
            self.assertEqual(1, response_dict[value]["deals"])
            self.assertEqual(1000, response_dict[value]["hectares"])

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_contract_farming_view(self):
        response = self.client.get(reverse("contract_farming_api"))
        self.assertEqual(200, response.status_code)
        response_dict = dict((d["name"], d) for d in response.data)
        for value, label in ActivityBase.NEGOTIATION_STATUS_CHOICES:
            if not value:
                continue
            self.assertEqual(1, response_dict[value]["deals"])
            self.assertEqual(1000, response_dict[value]["hectares"])


class ImplementationStatusChartViewTestCase(ChartViewTestCase):

    @classmethod
    def create_fixture(cls):
        cls.act_fixtures = []
        cls.act_inv_fixtures = {}
        for value, label in ActivityBase.IMPLEMENTATION_STATUS_CHOICES:
            if not value:
                continue
            id = len(cls.act_fixtures) + 1
            cls.act_fixtures.append({
                "id": id,
                "attributes": {
                    "target_country": {"value": "104"},
                    "intended_size": {"value": "1000"},
                    "contract_size": {"value": "1000"},
                    "production_size": {"value": "1000"},
                    "type": {"value": "Media report"},
                    "negotiation_status": {"value": ActivityBase.NEGOTIATION_STATUS_CONTRACT_SIGNED},
                    "implementation_status": {"value": value},
                }
            })
            cls.act_inv_fixtures[str(id)] = "1"

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_implementation_status_list_view(self):
        response = self.client.get(reverse("implementation_status_api"))
        self.assertEqual(200, response.status_code)
        response_dict = dict((d["name"], d) for d in response.data)
        for value, label in ActivityBase.IMPLEMENTATION_STATUS_CHOICES:
            if not value:
                continue
            self.assertEqual(1, response_dict[value]["deals"])
            self.assertEqual(1000, response_dict[value]["hectares"])


class InvestmentIntentionChartViewTestCase(ChartViewTestCase):

    @classmethod
    def create_fixture(cls):
        cls.act_fixtures = []
        cls.act_inv_fixtures = {}
        for value, label in intention_choices:
            if not value:
                continue
            id = len(cls.act_fixtures) + 1
            cls.act_fixtures.append({
                "id": id,
                "attributes": {
                    "target_country": {"value": "104"},
                    "intended_size": {"value": "1000"},
                    "contract_size": {"value": "1000"},
                    "production_size": {"value": "1000"},
                    "type": {"value": "Media report"},
                    "negotiation_status": {"value": ActivityBase.NEGOTIATION_STATUS_CONTRACT_SIGNED},
                    "intention": {"value": value},
                }
            })
            cls.act_inv_fixtures[str(id)] = "1"
        # Multiple intentions
        id = len(cls.act_fixtures) + 1
        cls.act_fixtures.append({
            "id": id,
            "attributes": {
                "target_country": {"value": "104"},
                "intended_size": {"value": "1000"},
                "contract_size": {"value": "1000"},
                "production_size": {"value": "1000"},
                "type": {"value": "Media report"},
                "negotiation_status": {"value": ActivityBase.NEGOTIATION_STATUS_CONTRACT_SIGNED},
                "intention": [
                    {"value": INTENTION_BIOFUELS},
                    {"value": INTENTION_TIMBER_PLANTATION},
                ],
            }
        })
        cls.act_inv_fixtures[str(id)] = "1"

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_investment_intention_list_view(self):
        response = self.client.get(reverse("intention"))
        self.assertEqual(200, response.status_code)
        response_dict = dict((d["name"], d) for d in response.data)
        for value, label in intention_choices:
            if not value:
                continue
            self.assertEqual(1, response_dict[value]["deals"])
            self.assertEqual(1000, response_dict[value]["hectares"])
        value = "Multiple intentions"
        self.assertEqual(1, response_dict[value]["deals"])
        self.assertEqual(1000, response_dict[value]["hectares"])
        self.assertEqual("Other", response_dict[value]["parent"])

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_investment_intention_list_view_with_agriculture(self):
        data = QueryDict("intention=agriculture")
        response = self.client.get(reverse("intention"), data)
        self.assertEqual(200, response.status_code)
        response_dict = dict((d["name"], d) for d in response.data)
        for value, label in intention_agriculture_choices:
            if not value:
                continue
            self.assertEqual(1, response_dict[value]["deals"])
            self.assertEqual(1000, response_dict[value]["hectares"])
        value = "Multiple intentions"
        self.assertEqual(1, response_dict[value]["deals"])
        self.assertEqual(1000, response_dict[value]["hectares"])
        self.assertEqual("Other", response_dict[value]["parent"])

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_investment_intention_list_view_with_forestry(self):
        data = QueryDict("intention=forestry")
        response = self.client.get(reverse("intention"), data)
        response_dict = dict((d["name"], d) for d in response.data)
        self.assertEqual(200, response.status_code)
        for value, label in intention_forestry_choices:
            if not value:
                continue
            self.assertEqual(1, response_dict[value]["deals"])
            self.assertEqual(1000, response_dict[value]["hectares"])
        value = "Multiple intentions"
        self.assertEqual(1, response_dict[value]["deals"])
        self.assertEqual(1000, response_dict[value]["hectares"])
        self.assertEqual("Other", response_dict[value]["parent"])


class CountriesChartViewTestCase(ChartViewTestCase):

    @classmethod
    def create_fixture(cls):
        cls.act_fixtures = []
        cls.act_inv_fixtures = {}
        id = len(cls.act_fixtures) + 1
        cls.act_fixtures.append({
            "id": id,
            "attributes": {
                "target_country": {"value": "104"},
                "intended_size": {"value": "1000"},
                "contract_size": {"value": "1000"},
                "production_size": {"value": "1000"},
                "type": {"value": "Media report"},
                "negotiation_status": {"value": ActivityBase.NEGOTIATION_STATUS_CONTRACT_SIGNED},
            }
        })
        cls.act_inv_fixtures[str(id)] = "1"

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_investor_country_summary_view(self):
        response = self.client.get(reverse("investor_country_summaries_api"))
        self.assertEqual(200, response.status_code)
        expected = [
            {
                "country": "Cambodia",
                "country_id": "116",
                "country_slug": "cambodia",
                "deals": 1,
                "domestic": 0,
                "lat": Decimal("12.565679000000"),
                "lat_max": Decimal("14.705078125000"),
                "lat_min": Decimal("10.411230468700"),
                "lon": Decimal("104.990963000000"),
                "lon_max": Decimal("107.605468750000"),
                "lon_min": Decimal("102.319726563000"),
                "name": "Cambodia",
                "region": "Asia",
                "region_slug": "asia",
                "transnational": 1,
                "url": "/data/by-investor-country/cambodia/",
            }
        ]
        self.assertEqual(expected, response.data)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_investor_countries_for_target_country_view(self):
        data = QueryDict("country_id=104")
        response = self.client.get(
            reverse("investor_countries_for_target_country_api"), data
        )
        self.assertEqual(200, response.status_code)
        expected = [
            {
                "country": "Cambodia",
                "country_id": "116",
                "country_slug": "cambodia",
                "deals": 1,
                "domestic": 0,
                "lat": Decimal("12.565679000000"),
                "lat_max": Decimal("14.705078125000"),
                "lat_min": Decimal("10.411230468700"),
                "lon": Decimal("104.990963000000"),
                "lon_max": Decimal("107.605468750000"),
                "lon_min": Decimal("102.319726563000"),
                "name": "Cambodia",
                "region": "Asia",
                "region_slug": "asia",
                "transnational": 1,
                "url": "/data/by-investor-country/cambodia/",
            }
        ]
        self.assertEqual(expected, response.data)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_target_country_summary_view(self):
        response = self.client.get(reverse("target_country_summaries_api"))
        self.assertEqual(200, response.status_code)
        expected = [
            {
                "country": "Myanmar",
                "country_id": "104",
                "country_slug": "myanmar",
                "deals": 1,
                "domestic": 0,
                "lat": Decimal("21.913965000000"),
                "lat_max": Decimal("28.517041015600"),
                "lat_min": Decimal("9.875390625000"),
                "lon": Decimal("95.956223000000"),
                "lon_max": Decimal("101.147265625000"),
                "lon_min": Decimal("92.179589843800"),
                "name": "Myanmar",
                "region": "Asia",
                "region_slug": "asia",
                "transnational": 1,
                "url": "/data/by-target-country/myanmar/",
            }
        ]
        self.assertEqual(expected, response.data)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_target_countries_for_investor_country_view_with_country(self):
        data = QueryDict("country=116")
        response = self.client.get(
            reverse("target_countries_for_investor_country_api"), data
        )
        self.assertEqual(200, response.status_code)
        expected = [
            {
                "country": "Myanmar",
                "country_id": "104",
                "country_slug": "myanmar",
                "deals": 1,
                "domestic": 0,
                "lat": Decimal("21.913965000000"),
                "lat_max": Decimal("28.517041015600"),
                "lat_min": Decimal("9.875390625000"),
                "lon": Decimal("95.956223000000"),
                "lon_max": Decimal("101.147265625000"),
                "lon_min": Decimal("92.179589843800"),
                "name": "Myanmar",
                "region": "Asia",
                "region_slug": "asia",
                "transnational": 1,
                "url": "/data/by-target-country/myanmar/",
            }
        ]
        self.assertEqual(expected, response.data)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_target_countries_for_investor_country_view_with_region(self):
        data = QueryDict("region=142")
        response = self.client.get(
            reverse("target_countries_for_investor_country_api"), data
        )
        self.assertEqual(200, response.status_code)
        expected = [
            {
                "country": "Myanmar",
                "country_id": "104",
                "country_slug": "myanmar",
                "deals": 1,
                "domestic": 0,
                "lat": Decimal("21.913965000000"),
                "lat_max": Decimal("28.517041015600"),
                "lat_min": Decimal("9.875390625000"),
                "lon": Decimal("95.956223000000"),
                "lon_max": Decimal("101.147265625000"),
                "lon_min": Decimal("92.179589843800"),
                "name": "Myanmar",
                "region": "Asia",
                "region_slug": "asia",
                "transnational": 1,
                "url": "/data/by-target-country/myanmar/",
            }
        ]
        self.assertEqual(expected, response.data)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_top_10_countries_view(self):
        response = self.client.get(reverse("top_10_countries_api"))
        self.assertEqual(200, response.status_code)
        investor_country = [
            {
                "id": "116",
                "name": "Cambodia",
                "hectares": 1000.0,
                "slug": "cambodia",
                "deals": 1,
            }
        ]
        self.assertEqual(investor_country, response.data.get("investor_country"))
        target_country = [
            {
                "id": "104",
                "name": "Myanmar",
                "hectares": 1000.0,
                "slug": "myanmar",
                "deals": 1,
            }
        ]
        self.assertEqual(target_country, response.data.get("target_country"))

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_transnational_deal_list_view(self):
        response = self.client.get(reverse("transnational_deals_api"))
        self.assertEqual(200, response.status_code)
        expected = [
            {
                "id": "104",
                "imports": ["142.Cambodia"],
                "name": "142.Myanmar",
                "size": 1,
                "slug": "myanmar",
            },
            {
                "id": "116",
                "imports": [],
                "name": "142.Cambodia",
                "size": 1,
                "slug": "cambodia",
            },
        ]
        self.assertEqual(expected, response.data)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_transnational_deal_list_view_with_region(self):
        data = QueryDict("region=142")
        response = self.client.get(reverse("transnational_deals_api"), data)
        self.assertEqual(200, response.status_code)
        expected = [
            {
                "id": "104",
                "imports": ["-1.Cambodia"],
                "name": "-1.Myanmar",
                "size": 1,
                "slug": "myanmar",
            },
            {
                "id": "116",
                "imports": [],
                "name": "-1.Cambodia",
                "size": 1,
                "slug": "cambodia",
            },
        ]
        self.assertEqual(expected, response.data)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_transnational_deals_by_country_view_with_target_country(self):
        response = self.client.get(
            reverse("transnational_deals_by_country_api"), data={"country": 104}
        )
        self.assertEqual(200, response.status_code)
        target_country = [
            {
                "region_id": "142",
                "slug": "asia",
                "region": "Asia",
                "hectares": 1000.0,
                "deals": 1,
            }
        ]
        self.assertEqual(target_country, response.data.get("target_country"))
        self.assertEqual([], response.data.get("investor_country"))

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_transnational_deals_by_country_view_with_investor_country(self):
        response = self.client.get(
            reverse("transnational_deals_by_country_api"), data={"country": 116}
        )
        self.assertEqual(200, response.status_code)
        investor_country = [
            {
                "region_id": "142",
                "slug": "asia",
                "region": "Asia",
                "hectares": 1000.0,
                "deals": 1,
            }
        ]
        self.assertEqual(investor_country, response.data.get("investor_country"))
        self.assertEqual([], response.data.get("target_country"))

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_transnational_deals_by_country_view_without_country(self):
        response = self.client.get(reverse("transnational_deals_by_country_api"))
        self.assertEqual(400, response.status_code)

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_hectares_view(self):
        response = self.client.get(reverse("hectares_api"))
        self.assertEqual(200, response.status_code)
        expected = {"deals": 1, "hectares": 1000}
        self.assertEqual(expected, response.data)


class AgriculturalProduceChartViewTestCase(ChartViewTestCase):

    @classmethod
    def create_fixture(cls):
        cls.act_fixtures = []
        cls.act_inv_fixtures = {}
        for region in Region.objects.all():
            target_country_id = region.country_set.filter(high_income=False).first().id
            for ap in AgriculturalProduce.objects.all():
                id = len(cls.act_fixtures) + 1
                crop_id = ap.crop_set.first().id
                cls.act_fixtures.append({
                    "id": id,
                    "attributes": {
                        "target_country": {"value": target_country_id},
                        "intended_size": {"value": "1000"},
                        "contract_size": {"value": "1000"},
                        "production_size": {"value": "1000"},
                        "type": {"value": "Media report"},
                        "negotiation_status": {"value": ActivityBase.NEGOTIATION_STATUS_CONTRACT_SIGNED},
                        "crops": [
                            {"value": crop_id},
                        ]
                    }
                })
                cls.act_inv_fixtures[str(id)] = "1"
            # Multiple use
            id = len(cls.act_fixtures) + 1
            cls.act_fixtures.append({
                "id": id,
                "attributes": {
                    "target_country": {"value": target_country_id},
                    "intended_size": {"value": "1000"},
                    "contract_size": {"value": "1000"},
                    "production_size": {"value": "1000"},
                    "type": {"value": "Media report"},
                    "negotiation_status": {"value": ActivityBase.NEGOTIATION_STATUS_CONTRACT_SIGNED},
                    "crops": [
                        {"value": ap.crop_set.first().id}
                        for ap in AgriculturalProduce.objects.all()
                    ]
                }
            })
            cls.act_inv_fixtures[str(id)] = "1"

    def slugify(self, ap):
        return ap.lower().replace("-", "_").replace(" ", "_") if ap else None

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_agricultural_produce_list_view(self):
        response = self.client.get(reverse("agricultural_produce_api"))
        self.assertEqual(200, response.status_code)
        response_dict = dict((d["region"], d) for d in response.data)
        ap_ratio = 100.0 / (AgriculturalProduce.objects.count() + 1)
        for region in Region.objects.all():
            self.assertIn(region.slug, response_dict.keys())
            region_dict = response_dict[region.slug]
            for ap in AgriculturalProduce.objects.all():
                slug = self.slugify(ap.name)
                self.assertEqual(ap_ratio, region_dict["agricultural_produce"][slug])
                self.assertEqual(1000, region_dict["hectares"][slug])
            # Multiple use
            self.assertEqual(ap_ratio, region_dict["agricultural_produce"]["multiple_use"])
            self.assertEqual(1000, region_dict["hectares"]["multiple_use"])
        # Overall
        overall_dict = response_dict["overall"]
        for ap in AgriculturalProduce.objects.all():
            slug = self.slugify(ap.name)
            self.assertEqual(ap_ratio, overall_dict["agricultural_produce"][slug])
            self.assertEqual(6000, overall_dict["hectares"][slug])
        # Multiple use
        self.assertEqual(ap_ratio, overall_dict["agricultural_produce"]["multiple_use"])
        self.assertEqual(6000, overall_dict["hectares"]["multiple_use"])


class ProduceInfoChartViewTestCase(ChartViewTestCase):

    produce_info = None

    @classmethod
    def create_fixture(cls):
        cls.act_fixtures = []
        cls.act_inv_fixtures = {}
        cls.produce_info = {
            "crops": Crop.objects.first(),
            "animals": Animal.objects.first(),
            "minerals": Mineral.objects.first()
        }
        for key, value in cls.produce_info.items():
            id = len(cls.act_fixtures) + 1
            attributes = {
                "target_country": {"value": "104"},
                "intended_size": {"value": "1000"},
                "contract_size": {"value": "1000"},
                "production_size": {"value": "1000"},
                "type": {"value": "Media report"},
                "negotiation_status": {"value": ActivityBase.NEGOTIATION_STATUS_CONTRACT_SIGNED},
                "crops": None,
                "animals": None,
                "minerals": None,
                key: {"value": value.id},
            }
            cls.act_fixtures.append({
                "id": id,
                "attributes": attributes
            })
            cls.act_inv_fixtures[str(id)] = "1"

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test_produce_info_view(self):
        response = self.client.get(reverse("produce_info_api"))
        self.assertEqual(200, response.status_code)
        for key, value in self.produce_info.items():
            response_dict = response.data.get(key)
            self.assertEqual([{"name": value.name, "size": 1000}], response_dict)
