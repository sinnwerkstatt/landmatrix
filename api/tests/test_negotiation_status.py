__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from .api_test_functions import ApiTestFunctions
from api.tests.deals_test_data import DealsTestData


class TestNegotiationStatus(ApiTestFunctions, DealsTestData):

    PREFIX = '/api/'
    POSTFIX = '.json?deal_scope=transnational&deal_scope=domestic'
    DEAL_SCOPE = 'transnational'
    DEAL_SIZE = 12345
    RELEVANT_ATTRIBUTES = {
        'pi_negotiation_status': 'Concluded (Contract signed)'
    }

    RAW_SQL = """SELECT
    sub.negotiation_status                AS negotiation_status,
    COUNT(DISTINCT a.activity_identifier) AS deal_count,
    ROUND(SUM(a.deal_size)) AS deal_size
FROM landmatrix_activity AS a
LEFT JOIN landmatrix_publicinterfacecache      AS pi               ON a.id = pi.fk_activity_id,
(
    SELECT DISTINCT
        a.id,
        a.negotiation_status AS negotiation_status,
        a.implementation_status AS implementation_status
    FROM landmatrix_activity AS a
    JOIN      landmatrix_status                                        ON landmatrix_status.id = a.fk_status_id
    LEFT JOIN landmatrix_publicinterfacecache      AS pi               ON a.id = pi.fk_activity_id
    LEFT JOIN landmatrix_investoractivityinvolvement AS iai            ON iai.fk_activity_id = a.id
    LEFT JOIN landmatrix_investor                  AS operational_stakeholder ON iai.fk_investor_id = operational_stakeholder.id
    LEFT JOIN landmatrix_investorventureinvolvement AS ivi             ON ivi.fk_venture_id = operational_stakeholder.id
    LEFT JOIN landmatrix_investor                  AS stakeholder      ON ivi.fk_investor_id = stakeholder.id
    LEFT JOIN landmatrix_country                   AS investor_country ON stakeholder.fk_country_id = investor_country.id
    LEFT JOIN landmatrix_region                    AS investor_region  ON investor_country.fk_region_id = investor_region.id
    LEFT JOIN landmatrix_activityattribute         AS intention        ON a.id = intention.fk_activity_id AND intention.name = 'intention'
    LEFT JOIN landmatrix_activityattribute         AS target_country   ON a.id = target_country.fk_activity_id AND target_country.name = 'target_country'
    LEFT JOIN landmatrix_country                   AS deal_country     ON CAST(target_country.value AS NUMERIC) = deal_country.id
    LEFT JOIN landmatrix_region                    AS deal_region      ON  deal_country.fk_region_id = deal_region.id
    WHERE
--        a.version = (
--            SELECT MAX(version) FROM landmatrix_activity AS amax
--            WHERE amax.activity_identifier = a.activity_identifier AND amax.fk_status_id IN (2, 3, 4)
--        ) AND
        a.is_public = 't'
        AND a.fk_status_id IN (2, 3)
--        AND a.deal_scope = 'transnational'
--        AND a.deal_scope = 'domestic'
) AS sub
WHERE sub.id = a.id
GROUP BY sub.negotiation_status ORDER BY sub.negotiation_status"""

    EXPECTED_DEAL_COUNT = 2
    EXPECTED_SIZE = 14690

    def test_empty(self):
        self.assertListEqual([], self.get_content('negotiation_status'))

    def test_with_data(self):
        self._generate_negotiation_status_data(123, self.DEAL_SIZE, self.DEAL_SCOPE, self.RELEVANT_ATTRIBUTES)
        result = self.get_content('negotiation_status')
        self.assertEqual(1, len(result))
        self.assertEqual(1, result[0]['deals'])
        self.assertEqual(self.RELEVANT_ATTRIBUTES['pi_negotiation_status'], result[0]['name'])
        self.assertEqual(self.DEAL_SIZE, result[0]['hectares'])

    def test_raw_sql(self):
        from decimal import Decimal

        self._generate_negotiation_status_data(123, self.DEAL_SIZE, self.DEAL_SCOPE)
        result = self._execute_sql(self.RAW_SQL)

        self.assertIn(1, result[0])
        self.assertIn('Concluded (Contract signed)', result[0])
        self.assertIn(Decimal(self.DEAL_SIZE), result[0])

    def test_with_domestic(self):
        self._generate_negotiation_status_data(123, 12345, 'transnational', {'pi_negotiation_status': self.RELEVANT_ATTRIBUTES['pi_negotiation_status']})
        self._generate_negotiation_status_data(124,  2345, 'domestic',      {'pi_negotiation_status': self.RELEVANT_ATTRIBUTES['pi_negotiation_status']})
        result = self.get_content('negotiation_status')
        self.assertEqual(1, len(result))
        self.assertEqual(self.EXPECTED_DEAL_COUNT, result[0]['deals'])
        self.assertEqual(self.RELEVANT_ATTRIBUTES['pi_negotiation_status'], result[0]['name'])
        self.assertEqual(self.EXPECTED_SIZE, result[0]['hectares'])

    def _execute_sql(self, sql):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute(sql)
        return cursor.fetchall()


class TestNegotiationStatusTransnational(TestNegotiationStatus):

    POSTFIX = '.json?deal_scope=transnational'
    EXPECTED_DEAL_COUNT = 1
    EXPECTED_SIZE = 12345


class TestNegotiationStatusDomestic(TestNegotiationStatus):

    POSTFIX = '.json?deal_scope=domestic'
    RELEVANT_ATTRIBUTES = {
        'pi_negotiation_status': 'Concluded (Contract signed)'
    }
    EXPECTED_DEAL_COUNT = 1
    EXPECTED_SIZE = 2345

    def test_with_data(self):
        self._generate_negotiation_status_data(124, 2345, 'domestic', self.RELEVANT_ATTRIBUTES)
        result = self.get_content('negotiation_status')
        self.assertEqual(1, len(result))
        self.assertEqual(1, result[0]['deals'])
        self.assertEqual('Concluded (Contract signed)', result[0]['name'])
        self.assertEqual(self.EXPECTED_SIZE, result[0]['hectares'])


class TestNegotiationStatusConcluded(TestNegotiationStatus):

    POSTFIX = '.json?deal_scope=transnational&deal_scope=domestic&negotiation_status=concluded'
    EXPECTED_DEAL_COUNT = 2
    EXPECTED_SIZE = 14690


class TestNegotiationStatusIntended(TestNegotiationStatus):

    POSTFIX = '.json?deal_scope=transnational&deal_scope=domestic&negotiation_status=intended'
    EXPECTED_DEAL_COUNT = 2
    EXPECTED_SIZE = 14690
    RELEVANT_ATTRIBUTES = {
        'pi_negotiation_status': 'intended (expression of interest)'
    }


class TestNegotiationStatusFailed(TestNegotiationStatus):

    POSTFIX = '.json?deal_scope=transnational&deal_scope=domestic&negotiation_status=failed'
    EXPECTED_DEAL_COUNT = 2
    EXPECTED_SIZE = 14690
    RELEVANT_ATTRIBUTES = {
        'pi_negotiation_status': 'failed (negotiations failed)'
    }


class TestNegotiationStatusDataSource(TestNegotiationStatus):

    POSTFIX = '.json?deal_scope=transnational&deal_scope=domestic&data_source_type=1'
    EXPECTED_DEAL_COUNT = 0
    EXPECTED_SIZE = 0
    RELEVANT_ATTRIBUTES = {
        'pi_negotiation_status': 'Concluded (Contract signed)', 'type': 'Media report'
    }

    def test_with_data(self):
        self._generate_negotiation_status_data(123, self.DEAL_SIZE, self.DEAL_SCOPE, self.RELEVANT_ATTRIBUTES)
        result = self.get_content('negotiation_status')
        self.assertEqual(0, len(result))

    def test_with_domestic(self):
        self._generate_negotiation_status_data(123, 12345, 'transnational', {
            'pi_negotiation_status': self.RELEVANT_ATTRIBUTES['pi_negotiation_status'], 'type': 'Media report'
        })
        self._generate_negotiation_status_data(124, 2345, 'domestic', {
            'pi_negotiation_status': self.RELEVANT_ATTRIBUTES['pi_negotiation_status'], 'type': 'Media report'
        })
        result = self.get_content('negotiation_status')
        self.assertEqual(0, len(result))


class TestNegotiationStatusDataSourceNot(TestNegotiationStatus):

    POSTFIX = '.json?deal_scope=transnational&deal_scope=domestic&data_source_type=1'
    EXPECTED_DEAL_COUNT = 2
    EXPECTED_SIZE = 14690
    RELEVANT_ATTRIBUTES = {
        'pi_negotiation_status': 'Concluded (Contract signed)', 'type': 'NOT Media report'
    }

    def test_with_domestic(self):
        self._generate_negotiation_status_data(123, 12345, 'transnational', {
            'pi_negotiation_status': self.RELEVANT_ATTRIBUTES['pi_negotiation_status'], 'type': 'NOT Media report'
        })
        self._generate_negotiation_status_data(124, 2345, 'domestic', {
            'pi_negotiation_status': self.RELEVANT_ATTRIBUTES['pi_negotiation_status'], 'type': 'NOT Media report'
        })
        result = self.get_content('negotiation_status')
        self.assertEqual(1, len(result))
        self.assertEqual(self.EXPECTED_DEAL_COUNT, result[0]['deals'])
        self.assertEqual(self.RELEVANT_ATTRIBUTES['pi_negotiation_status'], result[0]['name'])
        self.assertEqual(self.EXPECTED_SIZE, result[0]['hectares'])
