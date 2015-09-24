__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from api.query_sets.fake_query_set import FakeQuerySet
from global_app.forms.add_deal_general_form import AddDealGeneralForm


class IntentionQuerySet(FakeQuerySet):

    fields = [
        ('intention', 'sub.intention'),
        ('deal_count',         'COUNT(DISTINCT a.activity_identifier)'),
        ('deal_size',          "ROUND(SUM(CAST(REPLACE(size.attributes->'pi_deal_size', ',', '.') AS NUMERIC)))")
    ]

    QUERY = """
SELECT
    sub.intention                                                       AS intention,
    COUNT(DISTINCT a.activity_identifier)                                           AS deal_count,
    ROUND(SUM(CAST(REPLACE(size.attributes->'pi_deal_size', ',', '.') AS NUMERIC))) AS deal_size
FROM landmatrix_activity                    AS a
LEFT JOIN landmatrix_activityattributegroup AS size             ON a.id = size.fk_activity_id AND size.attributes ? 'pi_deal_size',
(
    SELECT DISTINCT
        a.id AS id,
        CASE
            WHEN COUNT(DISTINCT intention.attributes->'intention') > 1 THEN 'Multiple intention'
            ELSE intention.attributes->'intention'
        END AS intention
    FROM landmatrix_activity                       AS a
    LEFT JOIN landmatrix_involvement               AS i                ON i.fk_activity_id = a.id
--    LEFT JOIN landmatrix_stakeholder               AS s                ON i.fk_stakeholder_id = s.id
    LEFT JOIN landmatrix_primaryinvestor           AS pi               ON i.fk_primary_investor_id = pi.id
--    LEFT JOIN landmatrix_stakeholderattributegroup AS skvf1            ON s.id = skvf1.fk_stakeholder_id AND skvf1.attributes ? 'country'
--    LEFT JOIN landmatrix_country                   AS investor_country ON CAST(skvf1.attributes->'country' AS NUMERIC) = investor_country.id
--    LEFT JOIN landmatrix_region                    AS investor_region  ON investor_country.fk_region_id = investor_region.id
    LEFT JOIN landmatrix_activityattributegroup    AS intention        ON a.id = intention.fk_activity_id AND intention.attributes ? 'intention'
--    LEFT JOIN landmatrix_activityattributegroup    AS target_country   ON a.id = target_country.fk_activity_id AND target_country.attributes ? 'target_country'
--    LEFT JOIN landmatrix_country                   AS deal_country     ON CAST(target_country.attributes->'target_country' AS NUMERIC) = deal_country.id
--    LEFT JOIN landmatrix_region                    AS deal_region      ON  deal_country.fk_region_id = deal_region.id
    LEFT JOIN landmatrix_activityattributegroup    AS negotiation      ON a.id = negotiation.fk_activity_id AND negotiation.attributes ? 'pi_negotiation_status'
    LEFT JOIN landmatrix_activityattributegroup    AS implementation   ON a.id = implementation.fk_activity_id AND implementation.attributes ? 'pi_implementation_status'
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
    GROUP BY a.id, intention.attributes->'intention'
)                                           AS sub
WHERE sub.id = a.id
GROUP BY sub.intention ORDER BY sub.intention
"""

    def set_intention(self, intention):
        self.intention = intention

    INTENTIONS = list(filter(lambda k: "Mining" not in k, [str(i[1]) for i in AddDealGeneralForm().fields["intention"].choices]))
    INTENTIONS_AGRICULTURE = [str(i[1]) for i in AddDealGeneralForm().fields["intention"].choices[0][2]]

    def all(self):
        parent_intention = self.intention
        filter_intentions = parent_intention.lower() == "agriculture" and self.INTENTIONS_AGRICULTURE[:] or self.INTENTIONS[:]
        filter_intentions.append("Multiple intention")

        intention_filter_sql = "\nAND (intention.attributes->'intention' IN ('%s')\nOR intention.attributes->'intention' = '')" % "', '".join(filter_intentions)
        self._filter_sql += intention_filter_sql

        found = FakeQuerySet.all(self)

        intentions = {}

        for i in found:
             name = i['intention'] or ""
             name = (name == "Agriunspecified" and "Non-specified") or (name == "Other (please specify)" and "Other") or name
             intentions[name] = {
                 "name": name,
                 "deals": i['deal_count'],
                 "hectares": i['deal_size'],
             }
        output = []
        for i in filter_intentions:
            i = (i == "Agriunspecified" and "Non-specified") or (i == "Other (please specify)" and "Other") or i
            output.append(intentions.get(i, {"name": i, "deals": 0, "hectares": 0}))
        output.append(intentions.get("", {"name": "", "deals": 0, "hectares": 0}))
        return output