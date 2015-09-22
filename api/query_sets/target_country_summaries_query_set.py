__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from api.query_sets.fake_query_set import FakeQuerySet


class TargetCountrySummariesQuerySet(FakeQuerySet):

    fields = [
        ('country_id', 'sub.country_id'),
        ('country', 'sub.country'),
        ('region', 'sub.name'),
        ('lat', 'cast(sub.point_lat as char)'),
        ('lon', 'cast(sub.point_lon as char)'),
        ('deals',         'COUNT(DISTINCT a.activity_identifier)'),
        ('hectares',          "ROUND(SUM(CAST(REPLACE(size.attributes->'pi_deal_size', ',', '.') AS NUMERIC)))"),
        ('intentions', 'GROUP_CONCAT(sub.intention)')
    ]

    QUERY = """
SELECT
                sub.country_id,
                sub.country AS country,
                sub.name as region,
                cast(sub.point_lat as char),
                cast(sub.point_lon as char),
    COUNT(DISTINCT a.activity_identifier)                                           AS deal_count,
    ROUND(SUM(CAST(REPLACE(size.attributes->'pi_deal_size', ',', '.') AS NUMERIC))) AS deal_size,
                ARRAY_AGG(sub.intention)                                            AS intentions
FROM landmatrix_activity                    AS a
LEFT JOIN landmatrix_activityattributegroup AS size             ON a.id = size.fk_activity_id AND size.attributes ? 'pi_deal_size',
(
    SELECT DISTINCT
                a.id,
                deal_country.id as country_id,
                deal_country.name AS country,
                deal_region.name,
                cast(deal_country.point_lat as char) as point_lat,
                cast(deal_country.point_lon as char) as point_lon,
                STRING_AGG(DISTINCT intention.attributes->'intention', ',') AS intention
    FROM landmatrix_activity                       AS a
    JOIN      landmatrix_status                                        ON landmatrix_status.id = a.fk_status_id
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
        )
        AND a.fk_status_id IN (2, 3)
        AND bf.attributes->'pi_deal' = 'True'
        AND pi.version = (
            SELECT MAX(version) FROM landmatrix_primaryinvestor AS amax
            WHERE amax.primary_investor_identifier = pi.primary_investor_identifier AND amax.fk_status_id IN (2, 3, 4)
        )
        AND pi_st.name IN ('active', 'overwritten')
        %s
    GROUP BY a.id, deal_country.id, deal_region.name
)                                           AS sub
WHERE sub.id = a.id
            GROUP BY sub.country, sub.country_id, sub.name, sub.point_lat, sub.point_lon
"""

    def set_country_region(self, country_code, region):
        self.country_code = country_code
        self.region = region

    def all(self):
        if self.region:
            self._filter_sql += "AND deal_region.id = %s " % self.region
        if self.country_code:
            self._filter_sql += "AND deal_country.code_alpha3 = '%s' " % self.country_code

        return FakeQuerySet.all(self)
