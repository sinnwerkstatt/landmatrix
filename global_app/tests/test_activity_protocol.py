__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django.test import TestCase
from django.conf import settings
from django.http import HttpRequest
import json

from .deals_test_data import DealsTestData
from global_app.views import DummyActivityProtocol
from landmatrix.models import Activity

class TestActivityProtocol(TestCase, DealsTestData):

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
        from django.db.utils import ProgrammingError
        from django.db import connection
        try:
            if post: self._set_POST(post)
            response = self.protocol.dispatch(self.request, None)
            self.assertEqual(200, response.status_code)
            return json.loads(response.content.decode('utf-8'))
        except ProgrammingError as e:
            self.fail(str(e) + str(e.__cause__) + str(connection.queries[-1]['sql']))

    def _execute_sql(self, sql):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute(sql)
        return cursor.fetchall()
