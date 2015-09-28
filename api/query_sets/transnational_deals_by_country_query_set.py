from api.query_sets.fake_query_set_with_subquery import FakeQuerySetWithSubquery

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class TransnationalDealsQuerySet(FakeQuerySetWithSubquery):

    fields = [
        ('region_id', 'sub.region_id'),
        ('region',    'sub.region'),
        ('deals',     'COUNT(DISTINCT a.activity_identifier)'),
        ('hectares',  "ROUND(SUM(CAST(REPLACE(size.attributes->'pi_deal_size', ',', '.') AS NUMERIC)))")
    ]

    QUERY = """
SELECT DISTINCT
--  columns:
    %s
FROM landmatrix_activity                    AS a
LEFT JOIN landmatrix_activityattributegroup AS size             ON a.id = size.fk_activity_id AND size.attributes ? 'pi_deal_size',
(
    SELECT DISTINCT
        a.id,
--  subquery columns:
        %s
    FROM landmatrix_activity                       AS a
    LEFT JOIN landmatrix_involvement               AS i                ON i.fk_activity_id = a.id
    LEFT JOIN landmatrix_primaryinvestor           AS pi               ON i.fk_primary_investor_id = pi.id
    LEFT JOIN landmatrix_activityattributegroup    AS bf               ON a.id = bf.fk_activity_id AND bf.attributes ? 'pi_deal'
--  additional joins:
    %s
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
        AND investor_country.id <> deal_country.id
--  additional where conditions:
        %s
--  filter sql:
        %s

)                                           AS sub
WHERE sub.id = a.id
GROUP BY sub.region_id, sub.region
"""

    def __init__(self, get_data):
        super().__init__(get_data)
        self.country = get_data.get("country", "")

    def all(self):
        if self.country:
            self._additional_wheres.append("%s.id = %s " % (self.country, self.COUNTRY_FIELD))
        return super().all()



class TransnationalDealsByTargetCountryQuerySet(TransnationalDealsQuerySet):

    _subquery_fields = [
        ('region_id', "deal_region.id"),
        ('region',    "deal_region.name")
    ]
    COUNTRY_FIELD = 'investor_country'
    _additional_joins = [
        "LEFT JOIN landmatrix_stakeholder               AS s                ON i.fk_stakeholder_id = s.id",
        "LEFT JOIN landmatrix_stakeholderattributegroup AS skvf1            ON s.id = skvf1.fk_stakeholder_id AND skvf1.attributes ? 'country'",
        "LEFT JOIN landmatrix_country                   AS investor_country ON CAST(skvf1.attributes->'country' AS NUMERIC) = investor_country.id",
        "LEFT JOIN landmatrix_activityattributegroup    AS target_country   ON a.id = target_country.fk_activity_id AND target_country.attributes ? 'target_country'",
        "LEFT JOIN landmatrix_country                   AS deal_country     ON CAST(target_country.attributes->'target_country' AS NUMERIC) = deal_country.id",
        "LEFT JOIN landmatrix_region                    AS deal_region      ON  deal_country.fk_region_id = deal_region.id",
        "LEFT JOIN landmatrix_activityattributegroup    AS negotiation      ON a.id = negotiation.fk_activity_id AND negotiation.attributes ? 'pi_negotiation_status'"
        "LEFT JOIN landmatrix_activityattributegroup    AS deal_scope       ON a.id = deal_scope.fk_activity_id AND deal_scope.attributes ? 'deal_scope'"
    ]
    _additional_wheres = ["deal_region.name IS NOT NULL"]


class TransnationalDealsByInvestorCountryQuerySet(TransnationalDealsQuerySet):

    _subquery_fields = [
        ('region_id', "investor_region.id"),
        ('region',    "investor_region.name")
    ]

    COUNTRY_FIELD = 'deal_country'

    _additional_joins = [
        "LEFT JOIN landmatrix_stakeholder               AS s                ON i.fk_stakeholder_id = s.id",
        "LEFT JOIN landmatrix_stakeholderattributegroup AS skvf1            ON s.id = skvf1.fk_stakeholder_id AND skvf1.attributes ? 'country'",
        "LEFT JOIN landmatrix_country                   AS investor_country ON CAST(skvf1.attributes->'country' AS NUMERIC) = investor_country.id",
        "LEFT JOIN landmatrix_region                    AS investor_region  ON investor_country.fk_region_id = investor_region.id",
        "LEFT JOIN landmatrix_activityattributegroup    AS target_country   ON a.id = target_country.fk_activity_id AND target_country.attributes ? 'target_country'",
        "LEFT JOIN landmatrix_country                   AS deal_country     ON CAST(target_country.attributes->'target_country' AS NUMERIC) = deal_country.id",
        "LEFT JOIN landmatrix_activityattributegroup    AS negotiation      ON a.id = negotiation.fk_activity_id AND negotiation.attributes ? 'pi_negotiation_status'"
        "LEFT JOIN landmatrix_activityattributegroup    AS deal_scope       ON a.id = deal_scope.fk_activity_id AND deal_scope.attributes ? 'deal_scope'"
    ]
    _additional_wheres = ["investor_country.name IS NOT NULL"]
