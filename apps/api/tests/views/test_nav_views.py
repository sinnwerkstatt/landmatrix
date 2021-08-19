from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse

from apps.api.elasticsearch import es_save
from apps.landmatrix.models import Country
from apps.landmatrix.tests.mixins import ElasticSearchFixtureMixin
from apps.wagtailcms.models import CountryPage, RegionPage


class CountryListViewTestCase(TestCase):

    fixtures = ["countries_and_regions"]

    def test(self):
        response = self.client.get(reverse("countries_api"))
        self.assertEqual(200, response.status_code)
        self.assertEqual(Country.objects.all().count(), len(response.data))
        expected = [4, "afghanistan", "Afghanistan"]
        self.assertEqual(expected, response.data[0])


class TargetCountryListViewTestCase(TestCase):

    fixtures = ["countries_and_regions"]

    def setUp(self):
        CountryPage.objects.create(
            title="Cambodia Page", country_id=116, path="/", depth=0
        )

    def test(self):
        response = self.client.get(reverse("target_countries_api"))
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.data))
        self.assertEqual("Observatories", response.data[0]["text"])
        expected = [[116, "cambodia-page", "Cambodia Page"]]
        self.assertEqual(expected, response.data[0]["children"])
        self.assertEqual("Other", response.data[1]["text"])


class RegionListViewTestCase(TestCase):

    fixtures = ["countries_and_regions"]

    def setUp(self):
        RegionPage.objects.create(title="Asia Page", region_id=142, path="/", depth=0)

    def test(self):
        response = self.client.get(reverse("regions_api"))
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.data))
        expected = [142, "asia", "Asia Page"]
        self.assertEqual(expected, response.data[0])


class InvestorListViewTestCase(ElasticSearchFixtureMixin, TestCase):

    inv_fixtures = [{"id": 10, "investor_identifier": 1, "name": "Test Investor #1"}]

    @override_settings(ELASTICSEARCH_INDEX_NAME="landmatrix_test")
    def test(self):
        response = self.client.get(reverse("investors_api"), data={"q": "test"})
        self.assertEqual(200, response.status_code)
        self.assertGreater(response.data.get("count"), 0)
        self.assertGreater(len(response.data.get("results")), 0)
        self.assertIn("next", response.data.keys())
        self.assertIn("previous", response.data.keys())
