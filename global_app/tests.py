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

    PI_NAME = 'Investor'
    INTENTION = 'Livestock'
    MINIMAL_POST = { "filters": { "group_by": "all" }, "columns": ["primary_investor", "intention"] }
    LIST_POST = { "filters": { }, "columns": ["primary_investor", "intention"] }
    TYPICAL_POST = {
        "filters": {"starts_with": 'null', "group_value": "", "group_by": "all"},
        "columns": ["deal_id", "target_country", "primary_investor", "investor_name", "investor_country", "intention", "negotiation_status", "implementation_status", "intended_size", "contract_size"]
    }

    def setUp(self):
        settings.DEBUG = False
        self.request = HttpRequest()
        self.protocol = DummyActivityProtocol()

    def test_minimal_view_executes(self):
        return self.get_and_check_response(self.MINIMAL_POST)

    def test_all_deal_sql_executes(self):
        return self.get_and_check_response(self.TYPICAL_POST)

    def test_subquery_result(self):

        self.create_data()

        sql = """
            SELECT DISTINCT
                a.id                                                    AS id,
                'all deals'                                             AS name,
                array_to_string(array_agg(DISTINCT p.name), '##!##')    AS primary_investor,
                array_to_string(array_agg(DISTINCT intention.attributes->'intention' ORDER BY intention.attributes->'intention'), '##!##') AS intention,
                'dummy'                                                 AS dummy
            FROM landmatrix_activity                        AS a
                JOIN landmatrix_status                                    ON (landmatrix_status.id = a.fk_status_id)
                LEFT JOIN landmatrix_involvement            AS i          ON (i.fk_activity_id = a.id)
                LEFT JOIN landmatrix_stakeholder            AS s          ON (i.fk_stakeholder_id = s.id)
                LEFT JOIN landmatrix_primaryinvestor        AS p          ON (i.fk_primary_investor_id = p.id)
                LEFT JOIN landmatrix_activityattributegroup AS intention  ON (a.id = intention.fk_activity_id AND intention.attributes ? 'intention')
                LEFT JOIN landmatrix_activityattributegroup AS pi_deal    ON (a.id = pi_deal.fk_activity_id AND pi_deal.attributes ? 'pi_deal')
                LEFT JOIN landmatrix_activityattributegroup AS deal_scope ON (a.id = deal_scope.fk_activity_id AND deal_scope.attributes ? 'deal_scope')
            WHERE a.version = (
                    SELECT max(version)
                    FROM landmatrix_activity AS amax, landmatrix_status AS st
                    WHERE amax.fk_status_id = st.id AND amax.activity_identifier = a.activity_identifier AND st.name IN ('active', 'overwritten', 'deleted')
                )
                AND landmatrix_status.name IN ('active', 'overwritten')
                AND pi_deal.attributes->'pi_deal' = 'True'
                AND (NOT DEFINED(intention.attributes, 'intention') OR intention.attributes->'intention' != 'Mining')
            GROUP BY a.id"""
        result = self.execute_sql(sql)
        self.assert_contains_created_record(result)
        self.assertIn(Activity.objects.last().id, result[-1])

    def test_minimal_view_returns_stuff(self):
        self.create_data()
        result = self.test_minimal_view_executes()
        self.assertListEqual([], result['errors'])
        self.assert_contains_created_record(result['activities'])

    def test_all_deals_view_returns_stuff(self):
        self.create_data()
        result = self.test_all_deal_sql_executes()
        self.assertListEqual([], result['errors'])
        self.assert_contains_created_record(result['activities'])

    def test_list_view_executes(self):
        settings.DEBUG = True
        return self.get_and_check_response(self.LIST_POST)

    def assert_contains_created_record(self, records):
        self.assertGreaterEqual(1, len(records))
        self.assertTrue(isinstance(records[-1], list) or isinstance(records[-1], tuple) and not isinstance(records[-1], str))
        self.assertIn(self.PI_NAME, records[-1])
        self.assertIn(self.INTENTION, records[-1])

    def set_POST(self, options):
        self.request.POST = { 'data': json.dumps(options) }

    def get_and_check_response(self, post=None):
        if post: self.set_POST(post)
        response = self.protocol.dispatch(self.request, None)
        self.assertEqual(200, response.status_code)
        return json.loads(response.content.decode('utf-8'))

    def execute_sql(self, sql):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def make_involvement(self, i_r = 0.):
        act = Activity(fk_status=Status.objects.get(id=2), activity_identifier=1, version=1)
        act.save()
        pi = PrimaryInvestor(fk_status=Status.objects.get(id=2), primary_investor_identifier=1, version=1, name=self.PI_NAME)
        pi.save()
        sh = Stakeholder(fk_status=Status.objects.get(id=2), stakeholder_identifier=1, version=1)
        sh.save()
        i = Involvement(fk_activity=act, fk_stakeholder=sh, fk_primary_investor = pi, investment_ratio=i_r)
        i.save()
        return i

    def create_data(self):
        from datetime import date
        self.make_involvement(1.23)
        lang = Language(english_name='English', local_name='Dinglisch', locale='en')
        lang.save()
        aag = ActivityAttributeGroup(
            fk_activity = Activity.objects.last(),
            fk_language=lang,
            date=date.today(),
            attributes={ 'intention': self.INTENTION, 'pi_deal': 'True', 'deal_scope': 'transnational'}
        )
        aag.save()


