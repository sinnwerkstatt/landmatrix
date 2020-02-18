from django.test import TestCase
from django.urls import reverse


class APIDealInvestorNetworkViewTestCase(TestCase):

    fixtures = [
        "status",
        "countries_and_regions",
        "users_and_groups",
        "investors",
        "venture_involvements",
    ]

    def test(self):
        response = self.client.get(
            reverse("api_deal_investor_network"), data={"investor_id": 7}
        )
        self.assertEqual(200, response.status_code)
        investor_network = response.data
        self.assertEqual("I7", investor_network.get("id"))
        self.assertEqual(7, investor_network.get("identifier"))
        self.assertEqual("Test Investor #7", investor_network.get("name"))
        self.assertEqual("Cambodia", investor_network.get("country"))
        self.assertEqual("Private company", investor_network.get("classification"))
        self.assertEqual("/investor/7/", investor_network.get("url"))
        investors = investor_network.get("investors")
        self.assertIsInstance(investors, (tuple, list))
        self.assertEqual(1, len(investors))
        self.assertEqual("I1", investors[0].get("id"))
        self.assertEqual(1, investors[0].get("identifier"))
        self.assertEqual("Test Investor #1", investors[0].get("name"))
        self.assertEqual("Cambodia", investors[0].get("country"))
        self.assertEqual("Private company", investors[0].get("classification"))
        self.assertEqual("/investor/1/", investors[0].get("url"))

    def test_with_history_id(self):
        response = self.client.get(
            reverse("api_deal_investor_network"), data={"history_id": 70}
        )
        self.assertEqual(200, response.status_code)
        investor_network = response.data
        self.assertEqual("I7", investor_network.get("id"))
        self.assertEqual(7, investor_network.get("identifier"))

    def test_with_invalid_investor(self):
        response = self.client.get(
            reverse("api_deal_investor_network"), data={"investor_id": 9999}
        )
        self.assertEqual(404, response.status_code)