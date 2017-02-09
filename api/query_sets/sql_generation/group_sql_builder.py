
from api.query_sets.sql_generation.sql_builder import SQLBuilder

class GroupSQLBuilder(SQLBuilder):

    def get_where_sql(self):
        where = []

#        if 'intention' in self.columns:
#            where.append("AND intention.value IS NOT NULL")

        if self.filters.get("starts_with", None):
            starts_with = self.filters.get("starts_with", "").lower()
            if self.group == "investor_country":
                where.append("AND investor_country.slug like '%s%%%%' " % starts_with)
            elif self.group == "target_country":
                where.append("AND deal_country.slug like '%s%%%%' " % starts_with)
            else:
                where.append("AND trim(lower(%s.value)) like '%s%%%%' " % (self.group, starts_with))

        return '\n'.join(where)


    def get_group_sql(self):
        group_by = [self.group if self.group else 'dummy', self.get_name_sql()]
        for c in self.columns:
            if not c in group_by:
                if not self.is_aggregate_column(c):
                    group_by.append(c)
        return "GROUP BY %s" % ', '.join((group_by[0],))

    def get_inner_group_sql(self):
        # query deals grouped by a key
        return ", %s" % self.group

    def column_sql(self, c):
        if c == self.group:
            # use single values for column which gets grouped by
            return self.SQL_COLUMN_MAP[c][1]
        try:
            return self.SQL_COLUMN_MAP[c][0]
        except TypeError:
            raise KeyError(c)

    def get_base_sql(self):
        return u"""SELECT DISTINCT
              %(name)s as name,
              %(columns)s
FROM landmatrix_activity                    AS a
%(from)s
LEFT JOIN landmatrix_activityattribute      AS deal_scope ON a.id = deal_scope.fk_activity_id AND deal_scope.name = 'deal_scope'
%(from_filter)s
WHERE """ + "\nAND ".join(filter(None, [
#            self.max_version_condition(),
            self.status_active_condition(), self.is_public_condition()#, self.not_mining_condition()
        ])) + """
%(where)s
%(where_filter)s
%(group_by)s
%(order_by)s
%(limit)s"""
