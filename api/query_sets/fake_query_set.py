from api.query_sets.sql_generation.filter_to_sql import FilterToSQL
from grid.views.browse_filter_conditions import BrowseFilterConditions
from grid.views.view_aux_functions import create_condition_formset, apply_filters_from_session
from landmatrix.models.browse_condition import BrowseCondition
from landmatrix.models.activity_attribute_group import ActivityAttribute

from django.db.models.query import QuerySet
from django.db import connection


__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class FakeModel(dict):
    pk = None


class FakeQuerySet(QuerySet):

    DEBUG = False

    _filter_sql = ''

    FIELDS = []
    ADDITIONAL_JOINS = []
    ADDITIONAL_WHERES = []
    GROUP_BY = []
    ORDER_BY = []
    LIMIT = None

    def __init__(self, request):
        self._all_results = []

        self._additional_joins = self.ADDITIONAL_JOINS
        self._additional_wheres = self.ADDITIONAL_WHERES
        self._set_filter_sql(self._get_filter(request))
        self._fields = self.FIELDS
        self._group_by = self.GROUP_BY
        self._order_by = self.ORDER_BY
        self._limit = self.LIMIT
        super().__init__()

    def all(self):
        self._fetch_all()
        return self._all_results

    def sql_query(self):
        return self.QUERY % self._filter_sql
#        return self.QUERY % (self.columns(), self.additional_joins(), self.additional_wheres(), self._filter_sql)

    def columns(self):
        # print(self.FIELDS)
        return ",\n    ".join([definition+" AS "+alias for alias, definition in self._fields])

    def additional_joins(self):
        no_dups = self._uniquify_join_expressions(self._additional_joins)
        # print('additional joins:', no_dups)
        return "\n".join(no_dups)

    def _uniquify_join_expressions(self, joins):
        no_dups = []
        [no_dups.append(i) for i in reversed(joins) if not self._contains_join(no_dups, i)]
        return reversed(no_dups)

    def _contains_join(self, joins, join):
        for checked_join in joins:
            if self._joins_equal(join, checked_join):
                return True
        return False

    def _join_components(self, join):
        import re
        m = re.match('LEFT JOIN (?P<table>\w+)\s+AS\s+(?P<alias>\w+)\s+ON\s+(?P<condition>.+)', join)
        if not m:
            return None, None, None
        return m.group('table'), m.group('alias'), m.group('condition')

    def _joins_equal(self, join_1, join_2):

        table_1, alias_1, condition_1 = self._join_components(join_1)
        table_2, alias_2, condition_2 = self._join_components(join_2)
        if table_1 is None or table_2 is None:
            return False
        if table_1 != table_2:
            return False
        if not 'attr_' in alias_1 or not 'attr_' in alias_2:
            return False
        return condition_1 == condition_2.replace(alias_2, alias_1)


    def additional_wheres(self):
        return 'AND ' + "\n    AND ".join(self._additional_wheres) if self._additional_wheres else ''

    def group_by(self):
        return "\nGROUP BY " + ', '.join(self._group_by) if self._group_by else ''

    def order_by(self):
        return "\nORDER BY " + ', '.join(self._order_by) if self._order_by else ''

    def limit(self):
        return 'LIMIT ' + str(self._limit) if self._limit else ''

    def _set_filter_sql(self, filter):
        self._filter_sql = filter

    def _fetch_all(self):
        if not self._all_results:
            for result in self._execute_query():
                try:
                    as_dict = {self._fields[i][0]: result[i] for i in range(len(self._fields))}
                except KeyError:
                    raise RuntimeError('You probably haven\'t defined the correct fields for your FakeQuerySet.')
                as_model = FakeModel(as_dict)
                self._all_results.append(as_model)

    def _execute_query(self):
        import time
        start_time = time.time()

        if self.DEBUG:
            print('*'*80, 'SQL: \n', self.sql_query())

        cursor = connection.cursor()
        cursor.execute(self.sql_query())
        all_results = list(cursor.fetchall())

        if self.DEBUG:
            print('*'*20, 'execution time:', time.time() - start_time)
            print('*'*20, 'Results:', all_results)

        return all_results

    BASE_FILTER_MAP = {
        "concluded": ("concluded (oral agreement)", "concluded (contract signed)"),
        "intended": ("intended (expression of interest)", "intended (under negotiation)" ),
        "failed": ("failed (contract canceled)", "failed (negotiations failed)"),
    }

    def _set_filters(self, GET):
        self.rules = BrowseCondition.objects.filter(rule__rule_type="generic")
        ConditionFormset = create_condition_formset()
        # if self._filter_set():
        # set given filters
        formset_data = GET.copy()
        formset_data.update({"conditions_empty-TOTAL_FORMS": 1, "conditions_empty-INITIAL_FORMS": 0, "form-MAX_NUM_FORMS": 1000})
        self.current_formset_conditions = ConditionFormset(formset_data, prefix="conditions_empty")
        # else:
        #     if self.group == "database":
        #         self.current_formset_conditions = None
        #     else:
        #         self.current_formset_conditions = ConditionFormset(self._get_filter_dict(), prefix="conditions_empty")

        # self.filters = BrowseFilterConditions(self.current_formset_conditions, [self.order_by()], 0).parse()
        self.filters = BrowseFilterConditions(self.current_formset_conditions, [], 0).parse()

        # self.filters["group_by"] = self.group_by()
        # self.filters["group_value"] = self.group_value
        self.filters["starts_with"] = GET.get("starts_with", None)

    def _get_filter(self, request):
        get_data = request.GET

        negotiation_status = get_data.getlist("negotiation_status", [])
        deal_scope = get_data.getlist("deal_scope", [])
        data_source_type = get_data.get("data_source_type")
        filter_sql = ""
        if negotiation_status:
            stati = []
            for n in negotiation_status:
                stati.extend(self.BASE_FILTER_MAP.get(n))
            filter_sql += " AND LOWER(a.negotiation_status) IN ('%s') " % "', '".join(stati)
        if len(deal_scope) == 1:
            filter_sql += " AND a.deal_scope = '%s' " % deal_scope[0]
        if data_source_type:
            filter_sql += """ AND NOT (
            SELECT ARRAY_AGG(value)
            FROM %s AS activity_attrs
            WHERE a.id = activity_attrs.fk_activity_id AND activity_attrs.name = 'type'
        ) = ARRAY['Media report']""" % ActivityAttribute._meta.db_table

        self._set_filters(get_data)
        # self._add_order_by_columns()

        apply_filters_from_session(request, self.filters)

        self.filter_to_sql = FilterToSQL(self.filters, self.columns)
        additional_sql = self.filter_to_sql.filter_where()
        filter_sql += additional_sql
        additional_joins = self.filter_to_sql.filter_from()
        if additional_joins:
            self._additional_joins.append(additional_joins)

        return filter_sql
