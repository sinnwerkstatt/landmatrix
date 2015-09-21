__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from .api_test_functions import ApiTestFunctions
from api.tests.deals_test_data import DealsTestData


class TestNegotiationStatus(ApiTestFunctions, DealsTestData):

    PREFIX = '/en/api/'
    POSTFIX = '.json?deal_scope=transnational&deal_scope=domestic'
    RELEVANT_ATTRIBUTES = {
        'pi_deal_size': '12345', 'deal_scope': 'transnational', 'pi_negotiation_status': 'Concluded (Contract signed)'
    }

    RAW_SQL = """SELECT
    sub.negotiation_status                AS negotiation_status,
    COUNT(DISTINCT a.activity_identifier) AS deal_count,
    ROUND(SUM(CAST(REPLACE(size.attributes->'pi_deal_size', ',', '.') AS NUMERIC))) AS deal_size
FROM landmatrix_activity AS a
LEFT JOIN landmatrix_activityattributegroup        AS size             ON a.id = size.fk_activity_id AND size.attributes ? 'pi_deal_size',
(
    SELECT DISTINCT
        a.id,
        negotiation.attributes->'pi_negotiation_status' AS negotiation_status
--        implementation.attributes->'pi_implementation_status' AS implementation_status
    FROM landmatrix_activity AS a
    JOIN      landmatrix_status                                        ON (landmatrix_status.id = a.fk_status_id)
    LEFT JOIN landmatrix_involvement               AS i                ON i.fk_activity_id = a.id
    LEFT JOIN landmatrix_stakeholder               AS s                ON i.fk_stakeholder_id = s.id
    LEFT JOIN landmatrix_primaryinvestor           AS pi               ON i.fk_primary_investor_id = pi.id
    LEFT JOIN landmatrix_status                    AS pi_st            ON pi.fk_status_id = pi_st.id
    LEFT JOIN landmatrix_stakeholderattributegroup AS skvf1            ON s.id = skvf1.fk_stakeholder_id AND skvf1.attributes ? 'country'
    LEFT JOIN landmatrix_country                   AS investor_country ON CAST(skvf1.attributes->'country' AS NUMERIC) = investor_country.id
    LEFT JOIN landmatrix_region                    AS investor_region  ON investor_country.fk_region_id = investor_region.id
    LEFT JOIN landmatrix_activityattributegroup    AS intention        ON a.id = intention.fk_activity_id AND intention.attributes ? 'intention'
    LEFT JOIN landmatrix_activityattributegroup    AS target_country   ON a.id = target_country.fk_activity_id AND target_country.attributes ? 'target_country'
    LEFT JOIN landmatrix_country                   AS deal_country     ON CAST(target_country.attributes->'target_country' AS NUMERIC) = deal_country.id
    LEFT JOIN landmatrix_region                    AS deal_region      ON  deal_country.fk_region_id = deal_region.id
    LEFT JOIN landmatrix_activityattributegroup    AS negotiation      ON a.id = negotiation.fk_activity_id AND negotiation.attributes ? 'pi_negotiation_status'
    LEFT JOIN landmatrix_activityattributegroup    AS implementation   ON a.id = implementation.fk_activity_id AND implementation.attributes ? 'pi_implementation_status'
    LEFT JOIN landmatrix_activityattributegroup    AS bf               ON a.id = bf.fk_activity_id AND bf.attributes ? 'pi_deal'
    LEFT JOIN landmatrix_activityattributegroup    AS size             ON a.id = size.fk_activity_id AND size.attributes ? 'pi_deal_size'
    LEFT JOIN landmatrix_activityattributegroup    AS deal_scope       ON a.id = deal_scope.fk_activity_id AND deal_scope.attributes ? 'deal_scope'
    WHERE
        a.version = (
            SELECT MAX(version) FROM landmatrix_activity AS amax
            WHERE amax.activity_identifier = a.activity_identifier AND amax.fk_status_id IN (2, 3, 4)
        ) AND a.fk_status_id IN (2, 3) AND bf.attributes->'pi_deal' = 'True' AND pi.version = (
            SELECT MAX(version) FROM landmatrix_primaryinvestor AS amax
            WHERE amax.primary_investor_identifier = pi.primary_investor_identifier AND amax.fk_status_id IN (2, 3, 4)
        )
        AND pi_st.name IN ('active', 'overwritten')
--        AND deal_scope.attributes->'deal_scope' = 'transnational'
--        AND deal_scope.attributes->'deal_scope' = 'domestic'
) AS sub
WHERE sub.id = a.id
GROUP BY sub.negotiation_status ORDER BY sub.negotiation_status"""

    EXPECTED_DEAL_COUNT = 2
    EXPECTED_SIZE = 14690

    def test_empty(self):
        self.assertListEqual([], self.get_content('negotiation_status'))

    def test_with_data(self):
        self._generate_negotiation_status_data(123, self.RELEVANT_ATTRIBUTES)
        result = self.get_content('negotiation_status')
        self.assertEqual(1, len(result))
        self.assertEqual(1, result[0]['deals'])
        self.assertEqual(self.RELEVANT_ATTRIBUTES['pi_negotiation_status'], result[0]['name'])
        self.assertEqual(12345, result[0]['hectares'])

    def test_raw_sql(self):
        from decimal import Decimal

        self._generate_negotiation_status_data(123, {'pi_deal_size': '12345', 'deal_scope': 'transnational'})
        result = self._execute_sql(self.RAW_SQL)

        self.assertIn(1, result[0])
        self.assertIn('Concluded (Contract signed)', result[0])
        self.assertIn(Decimal(12345), result[0])

    def test_with_domestic(self):
        self._generate_negotiation_status_data(123, {'pi_deal_size': '12345', 'deal_scope': 'transnational', 'pi_negotiation_status': self.RELEVANT_ATTRIBUTES['pi_negotiation_status']})
        self._generate_negotiation_status_data(124, {'pi_deal_size': '2345', 'deal_scope': 'domestic', 'pi_negotiation_status': self.RELEVANT_ATTRIBUTES['pi_negotiation_status']})
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
        'pi_deal_size': '2345', 'deal_scope': 'domestic', 'pi_negotiation_status': 'Concluded (Contract signed)'
    }
    EXPECTED_DEAL_COUNT = 1
    EXPECTED_SIZE = 2345

    def test_with_data(self):
        self._generate_negotiation_status_data(124, self.RELEVANT_ATTRIBUTES)
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
        'pi_deal_size': '12345', 'deal_scope': 'transnational', 'pi_negotiation_status': 'intended (expression of interest)'
    }


class TestNegotiationStatusFailed(TestNegotiationStatus):

    POSTFIX = '.json?deal_scope=transnational&deal_scope=domestic&negotiation_status=failed'
    EXPECTED_DEAL_COUNT = 2
    EXPECTED_SIZE = 14690
    RELEVANT_ATTRIBUTES = {
        'pi_deal_size': '12345', 'deal_scope': 'transnational', 'pi_negotiation_status': 'failed (negotiations failed)'
    }


class TestNegotiationStatusDataSource(TestNegotiationStatus):

    POSTFIX = '.json?deal_scope=transnational&deal_scope=domestic&data_source_type=1'
    EXPECTED_DEAL_COUNT = 0
    EXPECTED_SIZE = 0
    RELEVANT_ATTRIBUTES = {
        'pi_deal_size': '12345', 'deal_scope': 'transnational', 'pi_negotiation_status': 'Concluded (Contract signed)', 'type': 'Media report'
    }

    def test_with_data(self):
        self._generate_negotiation_status_data(123, self.RELEVANT_ATTRIBUTES)
        result = self.get_content('negotiation_status')
        self.assertEqual(0, len(result))

    def test_with_domestic(self):
        self._generate_negotiation_status_data(123, {
            'pi_deal_size': '12345', 'deal_scope': 'transnational',
            'pi_negotiation_status': self.RELEVANT_ATTRIBUTES['pi_negotiation_status'], 'type': 'Media report'
        })
        self._generate_negotiation_status_data(124, {
            'pi_deal_size': '2345', 'deal_scope': 'domestic',
            'pi_negotiation_status': self.RELEVANT_ATTRIBUTES['pi_negotiation_status'], 'type': 'Media report'
        })
        result = self.get_content('negotiation_status')
        self.assertEqual(0, len(result))


class TestNegotiationStatusDataSourceNot(TestNegotiationStatus):

    POSTFIX = '.json?deal_scope=transnational&deal_scope=domestic&data_source_type=1'
    EXPECTED_DEAL_COUNT = 2
    EXPECTED_SIZE = 14690
    RELEVANT_ATTRIBUTES = {
        'pi_deal_size': '12345', 'deal_scope': 'transnational', 'pi_negotiation_status': 'Concluded (Contract signed)', 'type': 'NOT Media report'
    }

    def test_with_domestic(self):
        self._generate_negotiation_status_data(123, {
            'pi_deal_size': '12345', 'deal_scope': 'transnational',
            'pi_negotiation_status': self.RELEVANT_ATTRIBUTES['pi_negotiation_status'], 'type': 'NOT Media report'
        })
        self._generate_negotiation_status_data(124, {
            'pi_deal_size': '2345', 'deal_scope': 'domestic',
            'pi_negotiation_status': self.RELEVANT_ATTRIBUTES['pi_negotiation_status'], 'type': 'NOT Media report'
        })
        result = self.get_content('negotiation_status')
        self.assertEqual(1, len(result))
        self.assertEqual(self.EXPECTED_DEAL_COUNT, result[0]['deals'])
        self.assertEqual(self.RELEVANT_ATTRIBUTES['pi_negotiation_status'], result[0]['name'])
        self.assertEqual(self.EXPECTED_SIZE, result[0]['hectares'])
