__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from api.query_sets.fake_query_set import FakeQuerySet


class DealsQuerySet(FakeQuerySet):

    fields = [
        ('point_lat', "location.attributes->'point_lat'"),
        ('point_lon', "location.attributes->'point_lon'"),
        ('intention', "intention.attributes->'intention'")
    ]

    QUERY = """
SELECT
    location.attributes->'point_lat'  AS point_lat,
    location.attributes->'point_lon'  AS point_lon,
    intention.attributes->'intention' AS intention
FROM landmatrix_activity                    AS a
    LEFT JOIN landmatrix_activityattributegroup    AS location         ON a.id = location.fk_activity_id AND location.attributes ? 'point_lat' AND location.attributes ? 'point_lon'
    LEFT JOIN landmatrix_activityattributegroup    AS intention        ON a.id = intention.fk_activity_id AND intention.attributes ? 'intention'
    LEFT JOIN landmatrix_activityattributegroup    AS bf               ON a.id = bf.fk_activity_id AND bf.attributes ? 'pi_deal'
    LEFT JOIN landmatrix_involvement               AS i                ON i.fk_activity_id = a.id
    LEFT JOIN landmatrix_primaryinvestor           AS pi               ON i.fk_primary_investor_id = pi.id
-- if filtering by investor country/region
--    LEFT JOIN landmatrix_stakeholder               AS s                ON i.fk_stakeholder_id = s.id
--    LEFT JOIN landmatrix_stakeholderattributegroup AS skvf1            ON s.id = skvf1.fk_stakeholder_id AND skvf1.attributes ? 'country'
--    LEFT JOIN landmatrix_country                   AS investor_country ON CAST(skvf1.attributes->'country' AS NUMERIC) = investor_country.id
--    LEFT JOIN landmatrix_region                    AS investor_region  ON investor_country.fk_region_id = investor_region.id
-- if filtering by target country/region
--    LEFT JOIN landmatrix_activityattributegroup    AS target_country   ON a.id = target_country.fk_activity_id AND target_country.attributes ? 'target_country'
--    LEFT JOIN landmatrix_country                   AS deal_country     ON CAST(target_country.attributes->'target_country' AS NUMERIC) = deal_country.id
--    LEFT JOIN landmatrix_region                    AS deal_region      ON  deal_country.fk_region_id = deal_region.id
-- if filtering by negotiation status
--    LEFT JOIN landmatrix_activityattributegroup    AS negotiation      ON a.id = negotiation.fk_activity_id AND negotiation.attributes ? 'pi_negotiation_status'
-- if filtering by implementation status
--    LEFT JOIN landmatrix_activityattributegroup    AS implementation   ON a.id = implementation.fk_activity_id AND implementation.attributes ? 'pi_implementation_status'
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
"""


