from api.query_sets.fake_query_set import FakeQuerySet



class FakeQuerySetWithSubquery(FakeQuerySet):

    ADDITIONAL_SUBQUERY_OPTIONS = ''

    QUERY = """
SELECT DISTINCT
--  columns:
    %s
FROM landmatrix_activity                    AS a,
(
    SELECT DISTINCT
        a.id
--  subquery columns:
        %s
    FROM landmatrix_activity                       AS a
--  additional joins:
    %s
    WHERE
        %s
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
        self._additional_subquery_options = self.ADDITIONAL_SUBQUERY_OPTIONS
        super().__init__(get_data)

    def sql_query(self):
        return (self.QUERY + '\n%s') % (
            self.columns(),
            self.subquery_columns(),
            self.additional_joins(),
            "\nAND ".join(filter(None, [
                self.status_active_condition(),
                self.is_public_condition()
            ])),
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
    %s
--  additional joins:
%s
WHERE
    %s
--  additional where conditions:
    %s
--  filter sql:
    %s
--  group by:
%s
--  limit:
%s
"""
    APPLY_GLOBAL_FILTERS = True

    def sql_query(self):
        filter_sql = self._filter_sql if self.APPLY_GLOBAL_FILTERS else ''
        return self.QUERY % (
            self.columns(),
            self.get_from(),
            self.additional_joins(),
            "\nAND ".join(filter(None, [
                self.status_active_condition(),
                self.is_public_condition()
            ])),
            self.additional_wheres(),
            filter_sql,
            self.group_by(),
            self.limit()
        )
