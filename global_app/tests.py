from django.test import TestCase
from landmatrix.models import *


class DealsTestData:

    PI_NAME = 'This should be a darn unique investor name, right?'
    INTENTION = 'Livestock'
    MINIMAL_POST = { "filters": { "group_by": "all" }, "columns": ["primary_investor", "intention"] }
    LIST_POST = { "filters": { }, "columns": ["primary_investor", "intention"] }
    TYPICAL_POST = {
        "filters": {"starts_with": 'null', "group_value": "", "group_by": "all"},
        "columns": ["deal_id", "target_country", "primary_investor", "investor_name", "investor_country", "intention", "negotiation_status", "implementation_status", "intended_size", "contract_size"]
    }
    ACT_ID = 1

    def make_involvement(self, i_r = 0.):
        act = Activity(fk_status=Status.objects.get(id=2), activity_identifier=self.ACT_ID, version=1)
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
        Region(
            name='South-East Asia', slug='south-east-asia', point_lat=0., point_lon=120.
        ).save()
        Country(
            fk_region=Region.objects.last(), code_alpha2='LA', code_alpha3='LAO',
            name="Lao People's Democratic Republic", slug='lao-peoples-democratic-republic',
            point_lat=18.85627, point_lon=106.495496,
            democracy_index=2.10, corruption_perception_index=2.1, high_income=False
        ).save()
        aag = ActivityAttributeGroup(
            fk_activity = Activity.objects.last(),
            fk_language=lang,
            date=date.today(),
            attributes={
                'intention': self.INTENTION, 'pi_deal': 'True', 'deal_scope': 'transnational',
                'target_country': Country.objects.last().id
            }
        )
        aag.save()


class AllDealsViewTest(TestCase, DealsTestData):

    # we use global_app as defined in landmatrix.url here because django-cms pages are not configured in test db
    ALL_DEALS_URL = '/en/global_app/all'

    # disabled because no django-cms pages configured, but redirects are applied
    def _test_anything_loads(self):
        response = self.get_url_following_redirects('/')
        print(response.content.decode('utf-8'))
        self.assertEqual(200, response.status_code)

    def test_view_loads(self):
        self.create_data()
        response = self.get_url_following_redirects(self.ALL_DEALS_URL)
        self.assertEqual(200, response.status_code)

    def test_view_contains_data(self):
        self.create_data()
        content = self.get_url_following_redirects(self.ALL_DEALS_URL).content.decode('utf-8')
        if True or settings.DEBUG: print(content, file=open('/tmp/testresult.html', 'w'))
        self.assertIn(self.PI_NAME, content)

    def get_url_following_redirects(self, url):
        response = self.client.get(url)
        while response.status_code in range(300, 308):
            print('redirect:', response.url)
            response = self.client.get(response.url)
        return response


from global_app.views import DummyActivityProtocol
from django.http import HttpRequest
import json
from django.conf import settings

class ActivityProtocolTest(TestCase, DealsTestData):

    def setUp(self):
        self.old_setting = settings.DEBUG
        settings.DEBUG = False
        self.request = HttpRequest()
        self.protocol = DummyActivityProtocol()

    def tearDown(self):
        settings.DEBUG = self.old_setting

    def test_minimal_view_executes(self):
        return self.get_and_check_response(self.MINIMAL_POST)

    def test_all_deal_sql_executes(self):
        settings.DEBUG=True
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
        result = self._execute_sql(sql)
        self._assert_contains_created_record(result)
        self.assertIn(Activity.objects.last().id, result[-1])

    def test_minimal_view_returns_stuff(self):
        self._assert_view_returns_stuff(self.test_minimal_view_executes)

    def test_all_deals_view_returns_stuff(self):
        self._assert_view_returns_stuff(self.test_all_deal_sql_executes)

    def test_list_view_executes(self):
        return self.get_and_check_response(self.LIST_POST)

    def test_list_view_returns_stuff(self):
        self._assert_view_returns_stuff(self.test_list_view_executes)

    def _assert_view_returns_stuff(self, function):
        self.create_data()
        result = function()
        self.assertListEqual([], result['errors'])
        self._assert_contains_created_record(result['activities'])

    def _assert_contains_created_record(self, records):
        self.assertGreaterEqual(1, len(records))
        self.assertTrue(isinstance(records[-1], list) or isinstance(records[-1], tuple) and not isinstance(records[-1], str))
        self.assertIn(self.PI_NAME, records[-1])
        self.assertIn(self.INTENTION, records[-1])

    def _set_POST(self, options):
        self.request.POST = { 'data': json.dumps(options) }

    def get_and_check_response(self, post=None):
        if post: self._set_POST(post)
        response = self.protocol.dispatch(self.request, None)
        self.assertEqual(200, response.status_code)
        return json.loads(response.content.decode('utf-8'))

    def _execute_sql(self, sql):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

from global_app.views.sql_builder import join_expression
class SQLBuilderTest(TestCase):

    def test_join_expression(self):
        self.assertTrue(
            'LEFT JOIN landmatrix_activity AS a ON local.fk_activity_id = a.id' in
            join_expression(Activity, 'a', 'local.fk_activity_id', 'id')
        )
        self.assertTrue(join_expression(Activity, 'a', 'local.fk_activity_id', 'id').endswith(' '))


class OldData:

    URL_VALUES = {
        '/api/statistics.json':
            {"total": {"acquired_land": 0, "acquired_africa": 0, "deals": 0, "hectares": 0, "year": 0, "investor_account": "30"}},
        '/api/statistics.json?deal_scope=transnational&negotiation_status=failed&negotiation_status=intended&negotiation_status=concluded':
            {"concluded": {"deals": 1046, "hectares": 38243154.0, "deals_percentage": 79.0, "hectares_percentage": 62.0}, "failed": {"deals": 86, "hectares": 7443148.0, "deals_percentage": 6.0, "hectares_percentage": 12.0}, "total": {"acquired_land": 93, "acquired_africa": 260, "deals": 1328, "hectares": 62021259.0, "year": 2000, "investor_account": "30"}, "intended": {"deals": 196, "hectares": 16334957.0, "deals_percentage": 15.0, "hectares_percentage": 26.0}},
        '/api/latest_deals.json?limit=3&deal_scope=transnational&negotiation_status=failed&negotiation_status=intended&negotiation_status=concluded':
            [{"timestamp": "23 March 2015 12:01", "state": "overwritten", "deal_id": 3858, "target_country": "Sri Lanka"}, {"timestamp": "23 March 2015 11:26", "state": "overwritten", "deal_id": 404, "target_country": "Philippines"}, {"timestamp": "23 March 2015 09:57", "state": "overwritten", "deal_id": 4630, "target_country": "Nicaragua"}]
    }