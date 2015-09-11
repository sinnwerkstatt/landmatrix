__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from api.query_sets.fake_query_set import FakeQuerySet
from global_app.forms.add_deal_general_form import AddDealGeneralForm


class TransnationalDealsQuerySet(FakeQuerySet):

    fields = [
        ('intention', 'sub.intention'),
        ('deal_count',         'COUNT(DISTINCT a.activity_identifier)'),
        ('deal_size',          "ROUND(SUM(CAST(REPLACE(size.attributes->'pi_deal_size', ',', '.') AS NUMERIC)))")
    ]

    QUERY = """
SELECT DISTINCT
    CONCAT(deal_region.id, '.', deal_country.name, '#!#', deal_country.id) AS target_country,
    ARRAY_AGG(DISTINCT CONCAT(investor_region.id, '.', investor_country.name,  '#!#', investor_country.id)) AS investor_country
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
    AND investor_country.id <> deal_country.id
GROUP BY target_country
"""

    def set_regions(self, regions):
        self.regions = regions

    def all(self):
        region_sql = ""
        if self.regions:
            region_sql = "AND deal_region.id in (%s) " % ", ".join(self.regions)
        self._filter_sql += region_sql

        found = FakeQuerySet.all(self)

        return found
