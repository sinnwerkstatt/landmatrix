__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from landmatrix.models.activity_attribute_group import ActivityAttributeGroup

from django.db.models.query import QuerySet
from django.db import connection


class FakeModel(dict):
    pk = None


class FakeQuerySet(QuerySet):

    DEBUG = False

    _filter_sql = ''

    def __init__(self, get_data):
        self._all_results = []
        self._set_filter_sql(self._get_filter(get_data))
        super().__init__()

    def all(self):
        self._fetch_all()
        return self._all_results

    def sql_query(self):
        return self.QUERY % self._filter_sql

#    def sql_query(self):
#        return self.QUERY % (self.columns(), self.additional_joins(), self.additional_wheres(), self._filter_sql)

    _additional_joins = []
    _additional_wheres = []
    _group_by = []

    def columns(self):
        return ",\n    ".join([definition+" AS "+alias for alias, definition in self.fields])

    def additional_joins(self):
        return "\n".join(self._additional_joins)

    def additional_wheres(self):
        return 'AND ' + "\n    AND ".join(self._additional_wheres) if self._additional_wheres else ''

    def group_by(self):
        return "\nGROUP BY " + ', '.join(self._group_by) if self._group_by else ''

    def _set_filter_sql(self, filter):
        self._filter_sql = filter

    def _fetch_all(self):
        if not self._all_results:
            for result in self._execute_query():
                try:
                    as_dict = {self.fields[i][0]: result[i] for i in range(len(self.fields))}
                except KeyError:
                    raise RuntimeError('You probably haven\'t defined the correct fields for your FakeQuerySet.')
                as_model = FakeModel(as_dict)
                self._all_results.append(as_model)

    def _execute_query(self):
        if self.DEBUG:
            print('Query:', self.sql_query())
        cursor = connection.cursor()
        cursor.execute(self.sql_query())
        all_results = list(cursor.fetchall())
        if self.DEBUG:
            print('Results:', all_results)
        return all_results

    BASE_FILTER_MAP = {
        "concluded": ("concluded (oral agreement)", "concluded (contract signed)"),
        "intended": ("intended (expression of interest)", "intended (under negotiation)" ),
        "failed": ("failed (contract canceled)", "failed (negotiations failed)"),
    }

    def _get_filter(self, get_data):
        negotiation_status = get_data.getlist("negotiation_status", [])
        deal_scope = get_data.getlist("deal_scope", [])
        data_source_type = get_data.get("data_source_type")
        filter_sql = ""
        if len(deal_scope) == 0:
            # when no negotiation stati or deal scope given no deals should be shown at the public interface
            return " AND 1 <> 1 "
        if negotiation_status:
            stati = []
            for n in negotiation_status:
                stati.extend(self.BASE_FILTER_MAP.get(n))
            filter_sql += " AND LOWER(negotiation.attributes->'pi_negotiation_status') IN ('%s') " % "', '".join(stati)
        if len(deal_scope) == 1:
            filter_sql += " AND deal_scope.attributes->'deal_scope' = '%s' " % deal_scope[0]
        if data_source_type:
            filter_sql += """ AND NOT (
            SELECT ARRAY_AGG(data_source_type.attributes->'type')
            FROM %s AS data_source_type
            WHERE a.id = data_source_type.fk_activity_id AND data_source_type.attributes ? 'type'
        ) = ARRAY['Media report']""" % ActivityAttributeGroup._meta.db_table

        return filter_sql


