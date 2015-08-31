from api.tests.deals_test_data import DealsTestData

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from landmatrix.models import *

from .api_test_functions import ApiTestFunctions


class TestNegotiationStatus(ApiTestFunctions, DealsTestData):

    PREFIX = '/en/api/'
    POSTFIX = '.json'

    def test_empty(self):
        self.assertListEqual([], self.get_content('negotiation_status'))

    def test_with_data(self):
        self._generate_data()
        result = self.get_content('negotiation_status')
        self.assertEqual(1, len(result))
        self.assertEqual(1, result[0]['deal_count'])
        self.assertEqual('Concluded (Contract signed)', result[0]['negotiation_status'])
        self.assertEqual(12345, result[0]['deal_size'])

    def test_raw_sql(self):
        from decimal import Decimal

        self._generate_data()
        result = self._execute_sql("""
SELECT
    sub.negotiation_status                AS negotiation_status,
    COUNT(DISTINCT a.activity_identifier) AS deal_count,
    ROUND(SUM(CAST(REPLACE(size.attributes->'pi_deal_size', ',', '.') AS NUMERIC))) AS deal_size
FROM landmatrix_activity AS a
LEFT JOIN landmatrix_activityattributegroup        AS size             ON a.id = size.fk_activity_id AND size.attributes ? 'pi_deal_size',
(
    SELECT DISTINCT
        a.id,
        negotiation.attributes->'pi_negotiation_status' AS negotiation_status,
        implementation.attributes->'pi_implementation_status' AS implementation_status
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
        AND deal_scope.attributes->'deal_scope' = 'transnational'

) AS sub
WHERE sub.id = a.id
GROUP BY sub.negotiation_status ORDER BY sub.negotiation_status
        """)

        self.assertIn(1, result[0])
        self.assertIn('Concluded (Contract signed)', result[0])
        self.assertIn(Decimal(12345), result[0])

    def _generate_data(self, preset_id=123):
        activity = Activity(activity_identifier=preset_id, fk_status_id=2, version=1)
        activity.save()
        p_i = PrimaryInvestor(id=preset_id, primary_investor_identifier=preset_id, fk_status_id=2, version=1)
        p_i.save()
        stakeholder = Stakeholder(id=preset_id, stakeholder_identifier=preset_id, fk_status_id=2, version=1)
        stakeholder.save()
        involvement = Involvement(fk_activity=activity, fk_primary_investor=p_i, fk_stakeholder=stakeholder)
        involvement.save()
        region = Region(id=123)
        region.save()
        country = Country(id=123, fk_region=region)
        country.save()
        ac_attributes = ActivityAttributeGroup(
            fk_activity=activity, fk_language_id=1, attributes={
                'intention': 'boring test stuff', 'target_country': '123',
                'pi_negotiation_status': 'Concluded (Contract signed)',
                'pi_implementation_status': 'blah', 'pi_deal': 'True', 'pi_deal_size': '12345',
                'deal_scope': 'transnational'
            }
        )
        ac_attributes.save()
        sh_attributes = StakeholderAttributeGroup(
            fk_stakeholder=stakeholder, fk_language_id=1, attributes={'country': '123'}
        )
        sh_attributes.save()

    def _execute_sql(self, sql):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute(sql)
        return cursor.fetchall()
