from api.query_sets.fake_query_set import FakeQuerySet

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class FakeQuerySetWithSubquery(FakeQuerySet):

    ADDITIONAL_SUBQUERY_OPTIONS = ''

    QUERY = """
SELECT DISTINCT
--  columns:
    %s
FROM landmatrix_activity                    AS a
LEFT JOIN landmatrix_publicinterfacecache   AS pi               ON a.id = pi.fk_activity_id AND pi.is_deal,
(
    SELECT DISTINCT
        a.id
--  subquery columns:
        %s
    FROM landmatrix_activity                       AS a
    LEFT JOIN landmatrix_publicinterfacecache   AS pi               ON a.id = pi.fk_activity_id AND pi.is_deal
    LEFT JOIN landmatrix_involvement               AS i                ON i.fk_activity_id = a.id
--#    LEFT JOIN landmatrix_primaryinvestor           AS pi               ON i.fk_primary_investor_id = pi.id
--  additional joins:
    %s
    WHERE
        a.version = (
            SELECT MAX(version) FROM landmatrix_activity AS amax
            WHERE amax.activity_identifier = a.activity_identifier AND amax.fk_status_id IN (2, 3, 4)
        )
        AND a.fk_status_id IN (2, 3)
--#        AND pi.version = (
--#            SELECT MAX(version) FROM landmatrix_primaryinvestor AS amax
--#            WHERE amax.primary_investor_identifier = pi.primary_investor_identifier AND amax.fk_status_id IN (2, 3, 4)
--#        )
--#        AND pi.fk_status_id IN (2, 3)
--  additional where conditions:
        %s
--  filter sql:
        %s
-- additional subquery options:
    %s
)                                           AS sub
WHERE sub.id = a.id
--  group by:
%s
--  order by:
%s
"""

    def __init__(self, get_data):
        super().__init__(get_data)
        self._additional_subquery_options = self.ADDITIONAL_SUBQUERY_OPTIONS

    def sql_query(self):
        return (self.QUERY + '\n%s') % (
            self.columns(),
            self.subquery_columns(),
            self.additional_joins(),
            self.additional_wheres(),
            self._filter_sql,
            self._additional_subquery_options,
            self.group_by(),
            self.order_by(),
            self.limit()
        )

    def subquery_columns(self):
        return ",\n        " + ",\n        ".join([definition+" AS "+alias for alias, definition in self.SUBQUERY_FIELDS]) if self.SUBQUERY_FIELDS else ''


class FakeQuerySetFlat(FakeQuerySet):

    QUERY = """
SELECT DISTINCT
--  columns:
    %s
FROM landmatrix_activity                       AS a
LEFT JOIN landmatrix_publicinterfacecache      AS pi               ON a.id = pi.fk_activity_id AND pi.is_deal
LEFT JOIN landmatrix_investoractivityinvolvement AS iai            ON iai.fk_activity_id = a.id
LEFT JOIN landmatrix_investor                  AS operational_stakeholder ON iai.fk_investor_id = operational_stakeholder.id
--  additional joins:
%s
WHERE
    a.version = (
        SELECT MAX(version) FROM landmatrix_activity AS amax
        WHERE amax.activity_identifier = a.activity_identifier AND amax.fk_status_id IN (2, 3, 4)
    )
    AND a.fk_status_id IN (2, 3)
--  additional where conditions:
    %s
--  filter sql:
    %s
--  group by:
%s
--  limit:
%s
"""

    def sql_query(self):
        return self.QUERY % (self.columns(), self.additional_joins(), self.additional_wheres(), self._filter_sql, self.group_by(), self.limit())
