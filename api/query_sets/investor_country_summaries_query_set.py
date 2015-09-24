__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from api.query_sets.fake_query_set import FakeQuerySet


class InvestorCountrySummariesQuerySet(FakeQuerySet):

    fields = [
        ('country_id', 'investor_country.id'),
        ('country',    'investor_country.name AS country'),
        ('region',     'investor_region.name'),
        ('lat',        'investor_country.point_lat,'),
        ('lon',        'investor_country.point_lon,'),
        ('deals',      'COUNT(DISTINCT a.activity_identifier)'),
        ('deal_scope', "deal_scope.attributes->'deal_scope'")
    ]

    QUERY = """
SELECT DISTINCT
    investor_country.id,
    investor_country.name AS country,
    investor_region.name,
    investor_country.point_lat,
    investor_country.point_lon,
    COUNT(DISTINCT a.activity_identifier) AS deals,
    deal_scope.attributes->'deal_scope'
FROM landmatrix_activity                       AS a
LEFT JOIN landmatrix_involvement               AS i                ON i.fk_activity_id = a.id
LEFT JOIN landmatrix_stakeholder               AS s                ON i.fk_stakeholder_id = s.id
LEFT JOIN landmatrix_primaryinvestor           AS pi               ON i.fk_primary_investor_id = pi.id
LEFT JOIN landmatrix_stakeholderattributegroup AS skvf1            ON s.id = skvf1.fk_stakeholder_id AND skvf1.attributes ? 'country'
LEFT JOIN landmatrix_country                   AS investor_country ON CAST(skvf1.attributes->'country' AS NUMERIC) = investor_country.id
LEFT JOIN landmatrix_region                    AS investor_region  ON investor_country.fk_region_id = investor_region.id
--  LEFT JOIN landmatrix_activityattributegroup    AS intention        ON a.id = intention.fk_activity_id AND intention.attributes ? 'intention'
--    LEFT JOIN landmatrix_activityattributegroup    AS target_country   ON a.id = target_country.fk_activity_id AND target_country.attributes ? 'target_country'
--    LEFT JOIN landmatrix_country                   AS deal_country     ON CAST(target_country.attributes->'target_country' AS NUMERIC) = deal_country.id
--    LEFT JOIN landmatrix_region                    AS deal_region      ON  deal_country.fk_region_id = deal_region.id
LEFT JOIN landmatrix_activityattributegroup    AS negotiation      ON a.id = negotiation.fk_activity_id AND negotiation.attributes ? 'pi_negotiation_status'
--    LEFT JOIN landmatrix_activityattributegroup    AS implementation   ON a.id = implementation.fk_activity_id AND implementation.attributes ? 'pi_implementation_status'
LEFT JOIN landmatrix_activityattributegroup    AS bf               ON a.id = bf.fk_activity_id AND bf.attributes ? 'pi_deal'
LEFT JOIN landmatrix_activityattributegroup    AS deal_scope       ON a.id = deal_scope.fk_activity_id AND deal_scope.attributes ? 'deal_scope'
WHERE
    a.version = (
        SELECT MAX(version) FROM landmatrix_activity AS amax
        WHERE amax.activity_identifier = a.activity_identifier AND amax.fk_status_id IN (2, 3, 4)
    )
    AND a.fk_status_id IN (2, 3)
    AND bf.attributes->'pi_deal' = 'True'
    AND pi.version = (
        SELECT MAX(version) FROM landmatrix_primaryinvestor AS amax
        WHERE amax.primary_investor_identifier = pi.primary_investor_identifier AND amax.fk_status_id IN (2, 3, 4)
    )
    AND pi.fk_status_id IN (2, 3)
    %s
GROUP BY investor_country.id, investor_region.name, deal_scope.attributes->'deal_scope'
"""

