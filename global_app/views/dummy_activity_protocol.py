__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django.http import HttpResponse
from django.db import connection
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

import json

from .sql_builder import SQLBuilder

def get_limit_sql(limit):
    if limit: return " LIMIT %s " % limit
    return ''

def get_order_sql(order_by):
    order_by_sql = ''
    if order_by:
        for field in order_by:
            if not order_by_sql:
                order_by_sql = "ORDER BY "
            else:
                order_by_sql += ", "
            natural_sort = ""
            if "+0" in field:
                natural_sort = "+0"
                field = field.split("+0")[0]
            if field[0] == "-":
                field = field[1:]
                order_by_sql += "%s %s DESC" % (field, natural_sort)
            else:
                order_by_sql += "%s %s ASC" % (field, natural_sort)

    return order_by_sql


class DummyActivityProtocol:

    def dispatch(self, request, action):

        if request.POST:
            if settings.DEBUG: print(request.POST['data'])
            self.data = json.loads(request.POST["data"])

        res = {"errors": [], "activities": []}
        filters = self.data["filters"]
        columns = self.data["columns"]

        res["activities"] = self._get_activities_by_filter_and_grouping(filters, columns)

#        return HttpResponse(json.dumps(res,encoding="cp1251"), mimetype="application/json")#FIXME, utf-8 breaks for get-the-detail view
        return HttpResponse(json.dumps(res))

    def _get_activities_by_filter_and_grouping(self, filters, columns):

        filter_sql = self._browse_filters_to_sql(filters)

        builder = SQLBuilder.create(columns, filters)
        sql = builder.get_base_sql() % {
            "from": (builder.get_from_sql()),
            "where": builder.get_where_sql(),
            "limit": get_limit_sql(filters.get("limit")),
            "order_by": get_order_sql(filters.get("order_by")),
            "from_filter_activity": filter_sql["activity"]["from"],
            "where_filter_activity": filter_sql["activity"]["where"],
            "from_filter_investor": filter_sql["investor"]["from"],
            "where_filter_investor": filter_sql["investor"]["where"],
            "group_by": builder.get_group_sql(),
            "inner_group_by": builder.get_inner_group_sql(),
            "name": builder.get_name_sql(),
            "columns": builder.get_columns_sql(),
            "sub_columns": builder.get_sub_columns_sql()
        }

        if (False and settings.DEBUG): print('*'*80, 'SQL: \n', sql)

        cursor = connection.cursor()
        cursor.execute(sql)
        return cursor.fetchall()


    def _browse_filters_to_sql(self, filters):
        sql = {
            "activity": {
                "where": "",
                "from": "",
            },
            "investor": {
                "where": "",
                "from": "",
            }
        }
        if not filters:
            return sql
        tables_from_act, where_act, tables_from_inv, where_inv = "", "", "", ""
        if filters.get("activity", {}).get("identifier"):
            for f in filters.get("activity").get("identifier"):
                operation = f.get("op")
                value = ",".join(filter(None, [s.strip() for s in f.get("value").split(",")]))
                where_act += "AND a.activity_identifier %s " % DummyActivityProtocol.OPERATION_MAP[operation][0] % value
        if filters.get("deal_scope") and filters.get("deal_scope") != "all":
            where_act += " AND deal_scope.attributes->'deal_scope' = '%s' " % filters.get("deal_scope")
        if filters.get("activity", {}).get("tags"):
            tags = filters.get("activity").get("tags")
            for i, (tag, value) in enumerate(tags.items()):
                variable_operation = tag.split("__")
                variable = variable_operation[0]
                # choose operation depending on variable type default 0(int)
                operation = ""
                if len(variable_operation) > 1:
                    operation = variable_operation[1]
                # empty as operation or no value given
                if operation == "is_empty" or not value or (value and not value[0]):
                    where_act += " AND akv%(count)i.value IS NULL " % {
                        "count": i,
                    }
                elif operation in ("in", "not_in"):
                    # value = value[0].split(",")
                    in_values = ",".join(["'%s'" % v.strip().replace("'", "\\'") for v in value])
                    if variable == "region":
                        where_act += " AND ar%(count)i.name %(op)s " % {
                            "count": i,
                            "op": DummyActivityProtocol.OPERATION_MAP[operation][0] % in_values,
                        }
                    else:
                        where_act += " AND akv%(count)i.attributes->'%(variable)s' %(op)s " % {
                            "count": i,
                            "op": DummyActivityProtocol.OPERATION_MAP[operation][0] % in_values,
                            'variable': variable
                        }
                else:
                    for v in value:
                        year = None
                        if "##!##" in v:
                            v,year =  v.split("##!##")[0], v.split("##!##")[1]
                        operation_type = not v.isdigit() and 1 or 0
                        if variable == "region":
                            where_act += " AND ar%(count)i.name %(op)s " % { "count": i, "op": DummyActivityProtocol.OPERATION_MAP[operation][operation_type] % v.replace("'", "\\'")}
                        else:
                            where_act += "  %(value)s  %(year)s " % {
                                "value": v and " AND akv%(count)i.value %(op)s " % { "count": i, "op": DummyActivityProtocol.OPERATION_MAP[operation][operation_type] % v.replace("'", "\\'")}  or "",
                                "year": year and " AND akv%i.year = '%s' " % (i, year) or ""
                            }
                # join tag tables for each condition
                if variable == "region":
                    tables_from_act += "LEFT JOIN landmatrix_activityattributegroup AS akv%(count)i, countries AS ac%(count)i, regions AS ar%(count)i \n" % {"count": i}
                    tables_from_act += " ON (a.id = akv%(count)i.fk_activity_id AND akv%(count)i.attributes ? 'target_country' AND akv%(count)i.value = ac%(count)i.name AND ar%(count)i.id = ac%(count)i.fk_region)"%{"count": i, "key": variable}
                if variable.isdigit():
                    tables_from_act += "LEFT JOIN landmatrix_activityattributegroup AS akv%(count)i\n" % {"count": i}
                    tables_from_act += " ON (a.id = akv%(count)i.fk_activity_id AND akv%(count)i.key_id = '%(key)s')"%{"count": i, "key": variable}
                else:
                    from .sql_builder import join_attributes
                    tables_from_act += join_attributes("akv%(count)i" % {"count": i}, variable)
#                    tables_from_act += "LEFT JOIN landmatrix_activityattributegroup AS akv%(count)i\n" % {"count": i}
#                    tables_from_act += " ON (a.id = akv%(count)i.fk_activity_id AND akv%(count)i.attributes ? '%(key)s')"%{"count": i, "key": variable}
        sql["activity"]["from"] = tables_from_act
        sql["activity"]["where"] = where_act
        if filters.get("investor", {}).get("tags"):
            tags = filters.get("investor").get("tags")
            for i, (tag, value) in enumerate(tags.items()):
                if not value:
                    continue
                variable_operation = tag.split("__")
                variable = variable_operation[0]
                # choose operation depending on variable type default 0(int)
                operation = ""
                if len(variable_operation) > 1:
                    operation = variable_operation[1]
                if operation == "is_empty" or not value or (value and not value[0]):
                    where_inv += " AND skv%(count)i.value IS NULL " % {
                        "count": i,
                    }
                elif operation in ("in", "not_in"):
                    value = value[0].split(",")
                    in_values = ",".join(["'%s'" % v.strip().replace("'", "\\'") for v in value])
                    if variable == "region":
                        where_inv += " AND skvr%(count)i.name %(op)s" % {
                            "count": i,
                            "op": DummyActivityProtocol.OPERATION_MAP[operation][0] % in_values
                        }
                    else:
                        where_inv += " AND skv%(count)i.value %(op)s" % {
                            "count": i,
                            "op": DummyActivityProtocol.OPERATION_MAP[operation][0] % in_values
                        }
                else:
                    for v in value:
                        operation_type = not v.isdigit() and 1 or 0
                        if variable == "region":
                            where_inv += " AND skvr%i.name %s" % (i, DummyActivityProtocol.OPERATION_MAP[operation][operation_type] % v.replace("'", "\\'"))
                        else:
                            where_inv += " AND skv%i.value %s" % (i, DummyActivityProtocol.OPERATION_MAP[operation][operation_type] % v.replace("'", "\\'"))
                        #query_params.append(v)
                # join tag tables for each condition
                if variable == "region":
                    tables_from_inv += "LEFT JOIN (sh_key_value_lookup skv%(count)i, countries skvc%(count)i, regions skvr%(count)i) \n" % {"count": i}
                    tables_from_inv += " ON (skv%(count)i.stakeholder_identifier = s.stakeholder_identifier AND skv%(count)i.key = 'country' AND skv%(count)i.value = skvc%(count)i.name AND skvr%(count)i.id = skvc%(count)i.fk_region)"%{"count": i, "key": variable}
                else:
                    tables_from_inv += "LEFT JOIN (sh_key_value_lookup skv%(count)i)\n" % {"count": i}
                    tables_from_inv += " ON (skv%(count)i.stakeholder_identifier = s.stakeholder_identifier AND skv%(count)i.key_id = '%(key)s')\n" % {"count": i, "key": variable}
            sql["investor"]["from"] = tables_from_inv
            sql["investor"]["where"] = where_inv
        return sql


    ## operation => (numeric operand, character operand, description )
    OPERATION_MAP = {
        "is" :      ("= %s", "= '%s'", _("is")),
        "in":       ("IN (%s)", "IN (%s)", _("is one of")),
        "not_in":   ("NOT IN (%s)", "NOT IN (%s)", _("isn't any of")),
        "gte":      (">= %s", ">= %s", _("is >=")),
        "gt":       ("> %s", "> '%s'", _("is >")),
        "lte":      ("<= %s", "<= '%s'", _("is <=")),
        "lt":       ("< %s", "< '%s'", _("is <")),
        "contains": ("LIKE '%%%%%%%%%s%%%%%%%%'", "LIKE '%%%%%%%%%s%%%%%%%%'", _("contains")),
        "is_empty": ("IS NULL", "IS NULL", _("is empty")),
    }


