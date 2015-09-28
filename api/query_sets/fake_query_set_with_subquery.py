from api.query_sets.fake_query_set import FakeQuerySet

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class FakeQuerySetWithSubquery(FakeQuerySet):

    _group_by = []

    def sql_query(self):
        if self._group_by:
            self._filter_sql += "\nGROUP BY " + ', '.join(self._group_by)
        return self.QUERY % (self.columns(), self.subquery_columns(), self.additional_joins(), self.additional_wheres(), self._filter_sql)

    def subquery_columns(self):
        return ",\n        ".join([definition+" AS "+alias for alias, definition in self._subquery_fields])


class FakeQuerySetFlat(FakeQuerySet):

    QUERY = """
SELECT DISTINCT
    %s
FROM landmatrix_activity                       AS a
LEFT JOIN landmatrix_involvement               AS i                ON i.fk_activity_id = a.id
LEFT JOIN landmatrix_primaryinvestor           AS pi               ON i.fk_primary_investor_id = pi.id
LEFT JOIN landmatrix_activityattributegroup    AS bf               ON a.id = bf.fk_activity_id AND bf.attributes ? 'pi_deal'
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
    %s
    %s
"""

    _group_by = []

    def sql_query(self):
        if self._group_by:
            self._filter_sql += "\nGROUP BY " + ', '.join(self._group_by)
        return self.QUERY % (self.columns(), self.additional_joins(), self.additional_wheres(), self._filter_sql)
