from psycopg2._psycopg import ProgrammingError

from .deals_test_data import DealsTestData
from landmatrix.models.activity import Activity, ActivityProtocol

from django.test import TestCase
from django.conf import settings
from django.http import HttpRequest
import json

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class TestActivityProtocol(TestCase, DealsTestData):

    def setUp(self):
        self.old_setting = settings.DEBUG
        settings.DEBUG = False
        self.request = self._prepare_request_with_session()
        self.protocol = ActivityProtocol()

    def _prepare_request_with_session(self):
        from django.conf import settings
        from django.utils.importlib import import_module

        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        session_key = None
        request.session = engine.SessionStore(session_key)
        return request

    def tearDown(self):
        settings.DEBUG = self.old_setting

    def test_minimal_view_executes(self):
        response = self.get_and_check_response(self.MINIMAL_POST)
        return response

    def test_all_deal_sql_executes(self):
        return self.get_and_check_response(self.TYPICAL_POST)

    def test_subquery_result(self):

        self.create_data()

        sql = """
            SELECT DISTINCT
                a.id                                                    AS id,
                'all deals'                                             AS name,
                array_to_string(array_agg(DISTINCT operational_stakeholder.name), '##!##')    AS operational_stakeholder,
                array_to_string(array_agg(DISTINCT intention.value ORDER BY intention), '##!##') AS intention,
                'dummy'                                                 AS dummy
            FROM landmatrix_activity                             AS a
                LEFT JOIN landmatrix_publicinterfacecache        AS pi          ON a.id = pi.fk_activity_id
                LEFT JOIN landmatrix_status                      AS status      ON status.id = a.fk_status_id
                LEFT JOIN landmatrix_investoractivityinvolvement AS iai         ON iai.fk_activity_id = a.id
                LEFT JOIN landmatrix_investor                    AS operational_stakeholder ON iai.fk_investor_id = operational_stakeholder.id
                LEFT JOIN landmatrix_investorventureinvolvement  AS ivi         ON ivi.fk_venture_id = operational_stakeholder.id
                LEFT JOIN landmatrix_investor                    AS stakeholder ON ivi.fk_investor_id = stakeholder.id
                LEFT JOIN landmatrix_activityattribute           AS intention   ON (a.id = intention.fk_activity_id AND intention.name = 'intention')
            WHERE
--            a.version = (
--                    SELECT max(version)
--                    FROM landmatrix_activity AS amax, landmatrix_status AS st
--                    WHERE amax.fk_status_id = st.id AND amax.activity_identifier = a.activity_identifier AND st.name IN ('active', 'overwritten', 'deleted')
--                )
--                AND
                a.is_public = 't' 
                AND status.name IN ('active', 'overwritten')
                AND (NOT DEFINED(intention.value) OR intention.value NOT LIKE '%Mining%')
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
        self._assert_element_present_verbatim_or_as_list(self.OS_NAME, records[-1])
        self._assert_element_present_verbatim_or_as_list(self.INTENTION, records[-1])

    def _assert_element_present_verbatim_or_as_list(self, element, record):
        self.assertTrue([element] in record or element in record)

    def _set_POST(self, options):
        self.request.POST = { 'data': json.dumps(options) }

    def get_and_check_response(self, post=None):
        from django.db.utils import ProgrammingError
        try:
            if post: self._set_POST(post)
            response = self.protocol.dispatch(self.request, None)
            self.assertEqual(200, response.status_code)
            return json.loads(response.content.decode('utf-8'))
        except ProgrammingError as e:
            self.fail(str(e) + str(e.__cause__) + self._sql())

    def _execute_sql(self, sql):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def _sql(self):
        from django.db import connection
        return str(connection.queries[-1]['sql'])
