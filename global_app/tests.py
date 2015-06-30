from django.test import TestCase
from landmatrix.models import *

class AllDealsViewTest(TestCase):

    ACT_ID = 1

    def make_involvement(self, i_r = 0):
        act = Activity(fk_status=Status.objects.get(id=1), activity_identifier=self.ACT_ID, version=1)
        act.save()
        pi = PrimaryInvestor(fk_status=Status.objects.get(id=1), primary_investor_identifier=1, version=1)
        pi.save()
        sh = Stakeholder(fk_status=Status.objects.get(id=1), stakeholder_identifier=1, version=1)
        sh.save()
        i = Involvement(fk_activity=act, fk_stakeholder=sh, fk_primary_investor = pi, investment_ratio=i_r)
        i.save()
        return i

    def _test_loads(self):
        i = self.make_involvement(1.23)
        response = self.client.get('/en/global/all')
        while response.status_code == 301: response = self.client.get(response.url)
        print(response.status_code, response.content)
        self.assertEqual(200, response.status_code)


from global_app.views import DummyActivityProtocol
from django.http import HttpRequest
import json
from django.conf import settings

class ActivityProtocolTest(TestCase):

    def setUp(self):
        settings.DEBUG = True
        self.request = HttpRequest()
        self.protocol = DummyActivityProtocol()

    def set_POST(self, options):
        self.request.POST = { 'data': json.dumps(options) }

    def test_execute_minimal(self):
        self.set_POST({ "filters": { "group_by": "all" }, "columns": ["primary_investor", "intention"] })
        response = self.protocol.dispatch(self.request, None)
        print(response.status_code, response.content)

    def test_execute_sql(self):
        self.set_POST( {
            "filters": {"starts_with": 'null', "group_value": "", "group_by": "all"},
            "columns": ["deal_id", "target_country", "primary_investor", "investor_name", "investor_country", "intention", "negotiation_status", "implementation_status", "intended_size", "contract_size"]
        } )
        response = self.protocol.dispatch(self.request, None)
        print(response.status_code, response.content)


