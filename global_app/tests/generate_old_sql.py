from landmatrix.models.stakeholder_attribute_group import StakeholderAttributeGroup

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django.utils.translation import ugettext_lazy as _

""" browse_filters_to_sql() from landmatrix V1 is preserved here to test generated
    SQL against the old SQL
"""
class GenerateOldSQL:

    def _browse_filters_to_sql(self, filters):
        sql = {
            "activity": {
                "where": "",
                "from": "",
            },
            "stakeholder": {
                "where": "",
                "from": "",
            }
        }
        if not filters:
            return sql
        tables_from_act, where_act, tables_from_inv, where_inv = "", "", "", ""
        if filters.get("activity", {}).get("identifier"):
#            print(filters.get("activity").get("identifier"))
            for f in filters.get("activity").get("identifier"):
#                print('f:',f)
                operation = f.get("op")
                value = ",".join(filter(None, [s.strip() for s in f.get("value").split(",")]))
                where_act += "AND a.activity_identifier %s " % self.OPERATION_MAP[operation][0] % value
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
                            "op": self.OPERATION_MAP[operation][0] % in_values,
                        }
                    else:
                        where_act += " AND akv%(count)i.attributes->'%(variable)s' %(op)s " % {
                            "count": i,
                            "op": self.OPERATION_MAP[operation][0] % in_values,
                            'variable': variable
                        }
                else:
                    for v in value:
                        year = None
                        if "##!##" in v:
                            v,year =  v.split("##!##")[0], v.split("##!##")[1]
                        operation_type = not v.isdigit() and 1 or 0
                        if variable == "region":
                            where_act += " AND ar%(count)i.name %(op)s " % { "count": i, "op": self.OPERATION_MAP[operation][operation_type] % v.replace("'", "\\'")}
                        else:
                            where_act += "  %(value)s  %(year)s " % {
                                "value": v and " AND akv%(count)i.value %(op)s " % { "count": i, "op": self.OPERATION_MAP[operation][operation_type] % v.replace("'", "\\'")}  or "",
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
                    from api.query_sets.sql_generation.join_functions import join_attributes
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
                            "op": self.OPERATION_MAP[operation][0] % in_values
                        }
                    else:
                        where_inv += " AND skv%(count)i.value %(op)s" % {
                            "count": i,
                            "op": self.OPERATION_MAP[operation][0] % in_values
                        }
                else:
                    for v in value:
                        operation_type = not v.isdigit() and 1 or 0
                        if variable == "region":
                            where_inv += " AND skvr%i.name %s" % (i, self.OPERATION_MAP[operation][operation_type] % v.replace("'", "\\'"))
                        else:
                            where_inv += " AND skv%i.value %s" % (i, self.OPERATION_MAP[operation][operation_type] % v.replace("'", "\\'"))
                        #query_params.append(v)
                # join tag tables for each condition
                if variable == "region":
                    tables_from_inv += "LEFT JOIN (sh_key_value_lookup skv%(count)i, countries skvc%(count)i, regions skvr%(count)i) \n" % {"count": i}
                    tables_from_inv += " ON (skv%(count)i.stakeholder_identifier = s.stakeholder_identifier AND skv%(count)i.key = 'country' AND skv%(count)i.value = skvc%(count)i.name AND skvr%(count)i.id = skvc%(count)i.fk_region)"%{"count": i, "key": variable}
                else:
                    tables_from_inv += "LEFT JOIN " + StakeholderAttributeGroup._meta.db_table + " AS skv%(count)i\n" % {"count": i}
                    tables_from_inv += " ON (skv%(count)i.fk_stakeholder_id = s.id AND skv%(count)i.attributes ? '%(key)s')\n" % {"count": i, "key": variable}
            sql["stakeholder"]["from"] = tables_from_inv
            sql["stakeholder"]["where"] = where_inv
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
