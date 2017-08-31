SELECT
  sub.name AS name,
  sub.deal_id AS deal_id,
  sub.target_country AS target_country,
  sub.operational_stakeholder AS operational_stakeholder,
  sub.parent_stakeholder_country AS parent_stakeholder_country,
  sub.intention AS intention,
  sub.negotiation_status AS negotiation_status,
  sub.implementation_status AS implementation_status,
  NULLIF(ARRAY_TO_STRING(ARRAY_AGG(DISTINCT intended_size.value), ', '), '') AS intended_size,
  NULLIF(ARRAY_TO_STRING(ARRAY_AGG(DISTINCT contract_size.value), ', '), '') AS contract_size
FROM
landmatrix_activity AS a
LEFT JOIN landmatrix_activityattribute         AS intended_size         ON a.id = intended_size.fk_activity_id AND intended_size.name = 'intended_size'
LEFT JOIN landmatrix_activityattribute         AS contract_size         ON a.id = contract_size.fk_activity_id AND contract_size.name = 'contract_size'
LEFT JOIN landmatrix_activityattribute         AS production_size       ON a.id = production_size.fk_activity_id AND production_size.name = 'production_size'

JOIN (
    SELECT DISTINCT
    a.id AS id,
    'all deals' AS name,
    a.activity_identifier AS deal_id,
ARRAY_AGG(DISTINCT deal_country.name) AS target_country,
ARRAY_AGG(DISTINCT operational_stakeholder.name) AS operational_stakeholder,
ARRAY_AGG(DISTINCT CONCAT(parent_stakeholder_country.name, '#!#', parent_stakeholder_country.code_alpha3)) AS parent_stakeholder_country,
ARRAY_AGG(DISTINCT intention.value ORDER BY intention.value) AS intention,
ARRAY_AGG(DISTINCT CONCAT(
                        negotiation_status.value,
                        '#!#',
                        negotiation_status.date,
                        '#!#',
                        negotiation_status.is_current
                )) AS negotiation_status,
CASE WHEN (
                ARRAY_AGG(
                    DISTINCT CONCAT(
                        implementation_status.value,
                        '#!#',
                        implementation_status.date,
                        '#!#',
                        implementation_status.is_current
                    )
                ) = '{#!##!#}') THEN NULL
                ELSE ARRAY_AGG(
                    DISTINCT CONCAT(
                        implementation_status.value,
                        '#!#',
                        implementation_status.date,
                        '#!#',
                        implementation_status.is_current
                    )
                ) END AS implementation_status
    FROM landmatrix_activity AS a
    LEFT JOIN landmatrix_investoractivityinvolvement AS iai                   ON a.id = iai.fk_activity_id
LEFT JOIN landmatrix_investor                  AS operational_stakeholder ON iai.fk_investor_id = operational_stakeholder.id
LEFT JOIN landmatrix_investorventureinvolvement AS ivi                   ON operational_stakeholder.id = ivi.fk_venture_id
LEFT JOIN landmatrix_investor                  AS stakeholder           ON ivi.fk_investor_id = stakeholder.id
LEFT JOIN landmatrix_activityattribute         AS target_country        ON a.id = target_country.fk_activity_id AND target_country.name = 'target_country'
LEFT JOIN landmatrix_country                   AS deal_country          ON CAST(target_country.value AS numeric) = deal_country.id
LEFT JOIN landmatrix_region                    AS deal_region           ON deal_country.fk_region_id = deal_region.id
LEFT JOIN landmatrix_investor                  AS stakeholders          ON ivi.fk_investor_id = stakeholders.id
LEFT JOIN landmatrix_country                   AS parent_stakeholder_country ON parent_stakeholder_country.id = stakeholders.fk_country_id
LEFT JOIN landmatrix_activityattribute         AS intention             ON a.id = intention.fk_activity_id AND intention.name = 'intention'
LEFT JOIN landmatrix_activityattribute         AS negotiation_status    ON a.id = negotiation_status.fk_activity_id AND negotiation_status.name = 'negotiation_status'
LEFT JOIN landmatrix_activityattribute         AS implementation_status ON a.id = implementation_status.fk_activity_id AND implementation_status.name = 'implementation_status'
LEFT JOIN landmatrix_activityattribute         AS intended_size         ON a.id = intended_size.fk_activity_id AND intended_size.name = 'intended_size'
LEFT JOIN landmatrix_activityattribute         AS contract_size         ON a.id = contract_size.fk_activity_id AND contract_size.name = 'contract_size'
LEFT JOIN landmatrix_activityattribute         AS deal_scope            ON a.id = deal_scope.fk_activity_id AND deal_scope.name = 'deal_scope'
    LEFT JOIN landmatrix_activityattribute         AS attr_0                ON a.id = attr_0.fk_activity_id AND attr_0.name = 'nature'

                    LEFT JOIN landmatrix_activityattribute AS attr_2
                    ON (a.id = attr_2.fk_activity_id AND attr_2.name = 'target_country')


                    LEFT JOIN landmatrix_country AS ac2
                    ON CAST(NULLIF(attr_2.value, '0') AS NUMERIC) = ac2.id

LEFT JOIN landmatrix_activityattribute         AS attr_3                ON a.id = attr_3.fk_activity_id AND attr_3.name = 'deal_scope'
LEFT JOIN landmatrix_activityattribute         AS attr_4                ON a.id = attr_4.fk_activity_id AND attr_4.name = 'intention'
LEFT JOIN landmatrix_activityattribute         AS attr_5                ON a.id = attr_5.fk_activity_id AND attr_5.name = 'intention'
LEFT JOIN landmatrix_activityattribute         AS attr_6                ON a.id = attr_6.fk_activity_id AND attr_6.name = 'nature'
LEFT JOIN landmatrix_activityattribute         AS attr_7                ON a.id = attr_7.fk_activity_id AND attr_7.name = 'intention'
LEFT JOIN landmatrix_activityattribute         AS attr_8                ON a.id = attr_8.fk_activity_id AND attr_8.name = 'negotiation_status'
LEFT JOIN landmatrix_activityattribute         AS attr_9                ON a.id = attr_9.fk_activity_id AND attr_9.name = 'implementation_status'
LEFT JOIN landmatrix_activityattribute         AS attr_10               ON a.id = attr_10.fk_activity_id AND attr_10.name = 'negotiation_status'
LEFT JOIN landmatrix_activityattribute         AS attr_11               ON a.id = attr_11.fk_activity_id AND attr_11.name = 'implementation_status'
LEFT JOIN landmatrix_activityattribute         AS attr_12               ON a.id = attr_12.fk_activity_id AND attr_12.name = 'deal_size'

    WHERE a.fk_status_id IN (2, 3)

    AND ((((attr_0.value NOT IN ('Pure contract farming') OR attr_0.value IS NULL))) AND
a.negotiation_status IN ('Oral agreement','Contract signed') AND
ac2.high_income = 'f' AND
a.deal_scope = 'transnational' AND
(((attr_4.value NOT IN ('Mining') OR attr_4.value IS NULL))) AND
(((attr_5.value NOT IN ('Forest logging / management') OR attr_5.value IS NULL)) OR
((attr_6.value NOT IN ('Concession') OR attr_6.value IS NULL))) AND
((attr_7.value NOT IN ('Oil / Gas extraction') OR attr_7.value IS NULL)) AND
((attr_8.date >= '2000-01-01') OR
(attr_9.date >= '2000-01-01')) AND
(a.deal_size >= 200))
    GROUP BY a.id
) AS sub ON (sub.id = a.id)
 GROUP BY a.id , sub.deal_id, sub.target_country, sub.operational_stakeholder, sub.parent_stakeholder_country, sub.intention, sub.negotiation_status, sub.implementation_status, sub.name
ORDER BY deal_id  ASC