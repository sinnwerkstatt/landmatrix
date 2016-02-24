__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


#
# make script run in django context.
#
import sys

import os.path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))


proj_path = os.path.join(os.path.dirname(__file__), "../..")
# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "landmatrix.settings")
sys.path.append(proj_path)

# This is so my local_settings.py gets loaded.
os.chdir(proj_path)

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

#
# actual script follows.
#

from django.db import connection
from api.query_sets.sql_generation.sql_builder import SQLBuilder

def get_excluded_deals():
    if not get_excluded_deals.deals:
        query = """SELECT DISTINCT a.activity_identifier AS deal_id
    FROM landmatrix_activity AS a
        LEFT JOIN landmatrix_activityattributegroup    AS pi_deal               ON a.id = pi_deal.fk_activity_id AND pi_deal.attributes ? 'pi_deal'
        LEFT JOIN landmatrix_activityattributegroup    AS intention             ON a.id = intention.fk_activity_id AND intention.attributes ? 'intention'
    WHERE a.version = (
        SELECT max(version)
        FROM landmatrix_activity amax, landmatrix_status st
        WHERE amax.fk_status_id = st.id
            AND amax.activity_identifier = a.activity_identifier
            AND st.name IN ('active', 'overwritten', 'deleted')
        )
        AND a.fk_status_id IN (2, 3)
        AND pi_deal.attributes->'pi_deal' = 'True'
        AND intention.attributes->'intention' = 'Mining'
    GROUP BY deal_id"""
        excluded_deals = execute(query)
        get_excluded_deals.deals = [item for sublist in excluded_deals for item in sublist]
    return get_excluded_deals.deals

get_excluded_deals.deals = []

def x(query):
    from django.db import connection
    print(len(query))
    print(query[:10])
    print('*'*80)
    print(connection.queries[-1]['sql'])
    print()

def humungous_sql():
    return """
SELECT
    sub.deal_id AS deal_id,
    sub.target_country AS target_country,
    sub.primary_investor AS primary_investor,
    sub.investor_name AS investor_name,
    sub.investor_country AS investor_country,
    sub.intention AS intention,
    sub.negotiation_status AS negotiation_status,
    sub.implementation_status AS implementation_status,
    NULLIF(ARRAY_TO_STRING(ARRAY_AGG(DISTINCT intended_size.attributes->'intended_size'), ', '), '') AS intended_size,
    NULLIF(ARRAY_TO_STRING(ARRAY_AGG(DISTINCT contract_size.attributes->'contract_size'), ', '), '') AS contract_size
FROM
landmatrix_activity AS a
LEFT JOIN landmatrix_activityattributegroup    AS size                  ON a.id = size.fk_activity_id AND size.attributes ? 'pi_deal_size'
LEFT JOIN landmatrix_activityattributegroup    AS intended_size         ON a.id = intended_size.fk_activity_id AND intended_size.attributes ? 'intended_size'
LEFT JOIN landmatrix_activityattributegroup    AS contract_size         ON a.id = contract_size.fk_activity_id AND contract_size.attributes ? 'contract_size'
LEFT JOIN landmatrix_activityattributegroup    AS production_size       ON a.id = production_size.fk_activity_id AND production_size.attributes ? 'production_size'
JOIN (
    SELECT DISTINCT
        a.id AS id,
        a.activity_identifier AS deal_id,
        ARRAY_TO_STRING(ARRAY_AGG(DISTINCT deal_country.name), '##!##') AS target_country,
        ARRAY_TO_STRING(ARRAY_AGG(DISTINCT p.name), '##!##') AS primary_investor,
        ARRAY_TO_STRING(ARRAY_AGG(DISTINCT CONCAT(investor_name.attributes->'investor_name', '#!#', s.stakeholder_identifier)), '##!##') AS investor_name,
        ARRAY_TO_STRING(ARRAY_AGG(DISTINCT CONCAT(investor_country.name, '#!#', investor_country.code_alpha3)), '##!##') AS investor_country,
        ARRAY_TO_STRING(ARRAY_AGG(DISTINCT intention.attributes->'intention' ORDER BY intention.attributes->'intention'), '##!##') AS intention,
        ARRAY_TO_STRING(ARRAY_AGG(
            DISTINCT CONCAT(
                negotiation_status.attributes->'negotiation_status',        '#!#',
                EXTRACT(YEAR FROM negotiation_status.date)
            )), '##!##'
        ) AS negotiation_status,
        CASE WHEN (
            ARRAY_TO_STRING(ARRAY_AGG(
                DISTINCT CONCAT(
                    implementation_status.attributes->'implementation_status',  '#!#',
                    EXTRACT(YEAR FROM implementation_status.date)
                )), '##!##'
            ) = '#!#') THEN NULL
            ELSE ARRAY_TO_STRING(ARRAY_AGG(
                DISTINCT CONCAT(
                    implementation_status.attributes->'implementation_status',  '#!#',
                    EXTRACT(YEAR FROM implementation_status.date)
                )), '##!##'
        ) END AS implementation_status
    FROM
    landmatrix_activity AS a
    JOIN landmatrix_status ON (landmatrix_status.id = a.fk_status_id)
    LEFT JOIN landmatrix_involvement               AS i                     ON a.id = i.fk_activity_id
    LEFT JOIN landmatrix_stakeholder               AS s                     ON i.fk_stakeholder_id = s.id
    LEFT JOIN landmatrix_activityattributegroup    AS deal_id               ON a.id = deal_id.fk_activity_id AND deal_id.attributes ? 'deal_id'
    LEFT JOIN landmatrix_activityattributegroup    AS target_country        ON a.id = target_country.fk_activity_id AND target_country.attributes ? 'target_country'
    LEFT JOIN landmatrix_country                   AS deal_country          ON CAST(target_country.attributes->'target_country' AS numeric) = deal_country.id
    LEFT JOIN landmatrix_region                    AS deal_region           ON deal_country.fk_region_id = deal_region.id
    LEFT JOIN landmatrix_primaryinvestor           AS p                     ON i.fk_primary_investor_id = p.id
    LEFT JOIN landmatrix_primaryinvestor           AS pi                    ON i.fk_primary_investor_id = pi.id
    LEFT JOIN landmatrix_status                    AS pi_st                 ON pi.fk_status_id = pi_st.id
    LEFT JOIN landmatrix_stakeholderattributegroup AS investor_name         ON s.id = investor_name.fk_stakeholder_id AND investor_name.attributes ? 'investor_name'
    LEFT JOIN landmatrix_stakeholderattributegroup AS skvl1                 ON s.id = skvl1.fk_stakeholder_id AND skvl1.attributes ? 'country'
    LEFT JOIN landmatrix_country                   AS investor_country      ON investor_country.id = CAST(skvl1.attributes->'country' AS numeric)
    LEFT JOIN landmatrix_region                    AS investor_region       ON investor_country.fk_region_id = investor_region.id
    LEFT JOIN landmatrix_activityattributegroup    AS intention             ON a.id = intention.fk_activity_id AND intention.attributes ? 'intention'
    LEFT JOIN landmatrix_activityattributegroup    AS negotiation_status    ON a.id = negotiation_status.fk_activity_id AND negotiation_status.attributes ? 'negotiation_status'
    LEFT JOIN landmatrix_activityattributegroup    AS implementation_status ON a.id = implementation_status.fk_activity_id AND implementation_status.attributes ? 'implementation_status'
    LEFT JOIN landmatrix_activityattributegroup    AS pi_deal               ON a.id = pi_deal.fk_activity_id AND pi_deal.attributes ? 'pi_deal'
    LEFT JOIN landmatrix_activityattributegroup    AS deal_scope            ON a.id = deal_scope.fk_activity_id AND deal_scope.attributes ? 'deal_scope'
    WHERE
        a.version = (
            SELECT max(version)
            FROM landmatrix_activity amax, landmatrix_status st
            WHERE amax.fk_status_id = st.id
                AND amax.activity_identifier = a.activity_identifier
                AND st.name IN ('active', 'overwritten', 'deleted')
        )
        AND landmatrix_status.name IN ('active', 'overwritten')
        AND pi_deal.attributes->'pi_deal' = 'True'
        AND (NOT DEFINED(intention.attributes, 'intention') OR intention.attributes->'intention' != 'Mining')
    GROUP BY a.id
) AS sub ON (sub.id = a.id)
GROUP BY a.id , sub.deal_id, sub.target_country, sub.primary_investor, sub.investor_name, sub.investor_country, sub.intention, sub.negotiation_status, sub.implementation_status
ORDER BY sub.deal_id
;
"""

def inner_sql():
    return """
SELECT DISTINCT
    a.activity_identifier AS deal_id,
    ARRAY_TO_STRING(ARRAY_AGG(DISTINCT deal_country.name), '##!##') AS target_country,
    ARRAY_TO_STRING(ARRAY_AGG(DISTINCT p.name), '##!##') AS primary_investor,
    ARRAY_TO_STRING(ARRAY_AGG(DISTINCT CONCAT(investor_name.attributes->'investor_name', '#!#', s.stakeholder_identifier)), '##!##') AS investor_name,
    ARRAY_TO_STRING(ARRAY_AGG(DISTINCT CONCAT(investor_country.name, '#!#', investor_country.code_alpha3)), '##!##') AS investor_country,
    ARRAY_TO_STRING(ARRAY_AGG(DISTINCT intention.attributes->'intention' ORDER BY intention.attributes->'intention'), '##!##') AS intention,
    ARRAY_TO_STRING(ARRAY_AGG(
        DISTINCT CONCAT(
            negotiation_status.attributes->'negotiation_status',        '#!#',
            EXTRACT(YEAR FROM negotiation_status.date)
        )), '##!##'
    ) AS negotiation_status,
    CASE WHEN (
        ARRAY_TO_STRING(ARRAY_AGG(
            DISTINCT CONCAT(
                implementation_status.attributes->'implementation_status',  '#!#',
                EXTRACT(YEAR FROM implementation_status.date)
            )), '##!##'
        ) = '#!#') THEN NULL
        ELSE ARRAY_TO_STRING(ARRAY_AGG(
            DISTINCT CONCAT(
                implementation_status.attributes->'implementation_status',  '#!#',
                EXTRACT(YEAR FROM implementation_status.date)
            )), '##!##'
    ) END AS implementation_status
FROM
landmatrix_activity AS a
JOIN landmatrix_status ON (landmatrix_status.id = a.fk_status_id)
LEFT JOIN landmatrix_involvement               AS i                     ON a.id = i.fk_activity_id
LEFT JOIN landmatrix_stakeholder               AS s                     ON i.fk_stakeholder_id = s.id
LEFT JOIN landmatrix_activityattributegroup    AS deal_id               ON a.id = deal_id.fk_activity_id AND deal_id.attributes ? 'deal_id'
LEFT JOIN landmatrix_activityattributegroup    AS target_country        ON a.id = target_country.fk_activity_id AND target_country.attributes ? 'target_country'
LEFT JOIN landmatrix_country                   AS deal_country          ON CAST(target_country.attributes->'target_country' AS numeric) = deal_country.id
LEFT JOIN landmatrix_region                    AS deal_region           ON deal_country.fk_region_id = deal_region.id
LEFT JOIN landmatrix_primaryinvestor           AS p                     ON i.fk_primary_investor_id = p.id
LEFT JOIN landmatrix_primaryinvestor           AS pi                    ON i.fk_primary_investor_id = pi.id
LEFT JOIN landmatrix_status                    AS pi_st                 ON pi.fk_status_id = pi_st.id
LEFT JOIN landmatrix_stakeholderattributegroup AS investor_name         ON s.id = investor_name.fk_stakeholder_id AND investor_name.attributes ? 'investor_name'
LEFT JOIN landmatrix_stakeholderattributegroup AS skvl1                 ON s.id = skvl1.fk_stakeholder_id AND skvl1.attributes ? 'country'
LEFT JOIN landmatrix_country                   AS investor_country      ON investor_country.id = CAST(skvl1.attributes->'country' AS numeric)
LEFT JOIN landmatrix_region                    AS investor_region       ON investor_country.fk_region_id = investor_region.id
LEFT JOIN landmatrix_activityattributegroup    AS intention             ON a.id = intention.fk_activity_id AND intention.attributes ? 'intention'
LEFT JOIN landmatrix_activityattributegroup    AS negotiation_status    ON a.id = negotiation_status.fk_activity_id AND negotiation_status.attributes ? 'negotiation_status'
LEFT JOIN landmatrix_activityattributegroup    AS implementation_status ON a.id = implementation_status.fk_activity_id AND implementation_status.attributes ? 'implementation_status'
LEFT JOIN landmatrix_activityattributegroup    AS pi_deal               ON a.id = pi_deal.fk_activity_id AND pi_deal.attributes ? 'pi_deal'
LEFT JOIN landmatrix_activityattributegroup    AS deal_scope            ON a.id = deal_scope.fk_activity_id AND deal_scope.attributes ? 'deal_scope'
WHERE
    a.version = (
        SELECT max(version)
        FROM landmatrix_activity amax, landmatrix_status st
        WHERE amax.fk_status_id = st.id
            AND amax.activity_identifier = a.activity_identifier
            AND st.name IN ('active', 'overwritten', 'deleted')
    )
    AND a.fk_status_id IN (2, 3)
    AND pi_deal.attributes->'pi_deal' = 'True'
--    AND (NOT DEFINED(intention.attributes, 'intention') OR intention.attributes->'intention' != 'Mining')
  AND NOT a.activity_identifier IN(%s)
GROUP BY deal_id
ORDER BY deal_id
""" % ', '.join(map(str, get_excluded_deals()))

def outer_sql(activity_identifiers):
    return """
SELECT
    NULLIF(ARRAY_TO_STRING(ARRAY_AGG(DISTINCT intended_size.attributes->'intended_size'), ', '), '') AS intended_size,
    NULLIF(ARRAY_TO_STRING(ARRAY_AGG(DISTINCT contract_size.attributes->'contract_size'), ', '), '') AS contract_size
FROM
landmatrix_activity AS a
LEFT JOIN landmatrix_activityattributegroup    AS size                  ON a.id = size.fk_activity_id AND size.attributes ? 'pi_deal_size'
LEFT JOIN landmatrix_activityattributegroup    AS intended_size         ON a.id = intended_size.fk_activity_id AND intended_size.attributes ? 'intended_size'
LEFT JOIN landmatrix_activityattributegroup    AS contract_size         ON a.id = contract_size.fk_activity_id AND contract_size.attributes ? 'contract_size'
LEFT JOIN landmatrix_activityattributegroup    AS production_size       ON a.id = production_size.fk_activity_id AND production_size.attributes ? 'production_size'
WHERE a.activity_identifier IN (%s)
AND a.version = (
    SELECT max(version)
    FROM landmatrix_activity amax, landmatrix_status st
    WHERE amax.fk_status_id = st.id
        AND amax.activity_identifier = a.activity_identifier
        AND st.name IN ('active', 'overwritten', 'deleted')
)
GROUP BY a.activity_identifier
ORDER BY a.activity_identifier
""" % ', '.join(activity_identifiers)

def activity_identifiers(inner_query_result):
    return list(map(lambda r: str(r[0]), inner_query_result))

def merge(inner, outer):
    from itertools import chain
    return [tuple(chain(inner[i], outer[i])) for i in range(0, len(inner))]

def test_split_humungous_query_in_two():
    humungous_results = execute(humungous_sql())
    inner_results = execute(inner_sql())
    outer_results = execute(outer_sql(activity_identifiers(inner_results)))

    merged = merge(inner_results, outer_results)
    for i in range(0, len(humungous_results)):
        if humungous_results[i] != merged[i]:
            print(i)
            print(humungous_results[i])
            print(merged[i])

def test_split_inner_query():

    print(get_excluded_deals())

    target_country_query = select(
        "ARRAY_AGG(DISTINCT target_country.attributes->'target_country') AS target_country",
        "landmatrix_activityattributegroup    AS target_country        ON a.id = target_country.fk_activity_id AND target_country.attributes ? 'target_country'"
    )
    primary_investor_query = select(
        "ARRAY_AGG(DISTINCT p.name) AS primary_investor",
        [
            "landmatrix_involvement               AS i                     ON a.id = i.fk_activity_id",
            "landmatrix_primaryinvestor           AS p                     ON i.fk_primary_investor_id = p.id",
        ]
    )
    investor_name_query = select(
        "ARRAY_AGG(DISTINCT CONCAT(investor_name.attributes->'investor_name', '#!#', s.stakeholder_identifier)) AS investor_name",
        [
            "landmatrix_involvement               AS i                     ON a.id = i.fk_activity_id",
            "landmatrix_stakeholder               AS s                     ON i.fk_stakeholder_id = s.id",
            "landmatrix_stakeholderattributegroup AS investor_name         ON s.id = investor_name.fk_stakeholder_id AND investor_name.attributes ? 'investor_name'",
        ]
    )
    investor_country_query = select(
        "ARRAY_AGG(DISTINCT skvl1.attributes->'country') AS investor_country",
        [
            "landmatrix_involvement               AS i                     ON a.id = i.fk_activity_id",
            "landmatrix_stakeholder               AS s                     ON i.fk_stakeholder_id = s.id",
            "landmatrix_stakeholderattributegroup AS skvl1                 ON s.id = skvl1.fk_stakeholder_id AND skvl1.attributes ? 'country'"
        ]
    )
    intention_query = select(
        "ARRAY_AGG(DISTINCT intention.attributes->'intention' ORDER BY intention.attributes->'intention') AS intention",
        "landmatrix_activityattributegroup    AS intention             ON a.id = intention.fk_activity_id AND intention.attributes ? 'intention'"
    )
    negotiation_query = select(
        """ARRAY_AGG(DISTINCT CONCAT(
            negotiation_status.attributes->'negotiation_status',        '#!#',
            EXTRACT(YEAR FROM negotiation_status.date)
        )) AS negotiation_status""",
        "landmatrix_activityattributegroup    AS negotiation_status    ON a.id = negotiation_status.fk_activity_id AND negotiation_status.attributes ? 'negotiation_status'"
    )
    implementation_query = select(
        """CASE WHEN (
        ARRAY_TO_STRING(ARRAY_AGG(
            DISTINCT CONCAT(
                implementation_status.attributes->'implementation_status',  '#!#',
                EXTRACT(YEAR FROM implementation_status.date)
            )), '##!##'
        ) = '#!#') THEN NULL
        ELSE ARRAY_TO_STRING(ARRAY_AGG(
            DISTINCT CONCAT(
                implementation_status.attributes->'implementation_status',  '#!#',
                EXTRACT(YEAR FROM implementation_status.date)
            )), '##!##'
    ) END AS implementation_status""",
        "landmatrix_activityattributegroup    AS implementation_status ON a.id = implementation_status.fk_activity_id AND implementation_status.attributes ? 'implementation_status'"
    )
    print(intention_query)

    from time import time
    start_time = time()

    tc_results = execute(target_country_query)
    pi_results = execute(primary_investor_query)
    in_results = execute(investor_name_query)
    ic_results = execute(investor_country_query)
    i_results =  execute(intention_query)
    ns_results = execute(negotiation_query)
    is_results = execute(implementation_query)

    print(time() - start_time)

    # inner_results = execute(inner_sql())
    # for i in range(0, len(inner_results)):
    #     if not inner_results[i][1] == tc_results[i][1]:
    #         print(i)
    #         print(inner_results[i])
    #         print(tc_results[i])

def select(fields, tables, where=list()):
    return """
SELECT %s
FROM %s
WHERE %s
GROUP BY deal_id
ORDER BY deal_id
""" % (
        select_fields(fields),
        select_tables(tables),
        select_where(where)
    )

def select_fields(fields):
    if isinstance(fields, str): fields = [fields]
    return ',\n    '.join([base_fields()] + fields)

def select_tables(join_tables):
    if isinstance(join_tables, str): join_tables = [join_tables]
    return '\n    LEFT JOIN '.join([base_tables()] + join_tables)

def select_where(where=[]):
    if isinstance(where, str): where = [where]
    return ' AND '.join([base_where()] + where)

def base_fields(): return 'DISTINCT a.activity_identifier AS deal_id'
def base_tables():
    return """landmatrix_activity AS a
    LEFT JOIN landmatrix_activityattributegroup    AS pi_deal               ON a.id = pi_deal.fk_activity_id AND pi_deal.attributes ? 'pi_deal'"""
def base_where():
    return """a.version = (
    SELECT max(version)
    FROM landmatrix_activity amax, landmatrix_status st
    WHERE amax.fk_status_id = st.id
        AND amax.activity_identifier = a.activity_identifier
        AND st.name IN ('active', 'overwritten', 'deleted')
    )
    AND a.fk_status_id IN (2, 3)
    AND pi_deal.attributes->'pi_deal' = 'True'
    AND NOT a.activity_identifier IN (%s)""" % ', '.join(map(str, get_excluded_deals()))

def execute(sql):
    from time import time
    start_time = time()
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    print(time() - start_time)
    return result

#test_split_humungous_query_in_two()

#test_split_inner_query()

from api.query_sets.sql_generation import RecordReader


null = None
GROUP_VIEW_PARAMETERS = {
    "columns": ["deal_id", "target_country", "primary_investor", "investor_name", "investor_country", "intention", "negotiation_status", "implementation_status", "intended_size", "contract_size"],
    "filters": {
        "deal_scope": "transnational", "order_by": ["deal_id"], "group_by": "all", "limit": "", "group_value": "",
        "activity": {"tags": {"pi_negotiation_status__in": ["Concluded (Oral Agreement)", "Concluded (Contract signed)"]}},
        "investor": {"tags": {}},
        "starts_with": null
    }
}


from time import time
start_time = time()
reader = RecordReader(GROUP_VIEW_PARAMETERS['filters'], GROUP_VIEW_PARAMETERS['columns'])
split_results = reader.get_all(assemble=reader._make_padded_record_from_column_data)
print(time() - start_time)

humungous_query = SQLBuilder.create(GROUP_VIEW_PARAMETERS['filters'], GROUP_VIEW_PARAMETERS['columns']).get_sql()
humungous_results = execute(humungous_query)

print('split:', len(split_results), 'humungous:', len(humungous_results))

extra_found_records = set(split_results)-set(humungous_results)
print('\n  '.join(map(str, extra_found_records)))
print()

not_found_records = set(humungous_results)-set(split_results)
print('\n  '.join(map(str, not_found_records)))

#print(humungous_query)
print('*'*80)
#print(reader.get_column_sql(reader.columns[0]))
exit()
