#from landmatrix.models.stakeholder_attribute_group import StakeholderAttributeGroup

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django.utils.translation import ugettext_lazy as _

from api.query_sets.sql_generation.join_functions import join_attributes


class FilterToSQL:

    def __init__(self, filters, columns):
        self.filters = filters
        self.columns = columns

    def filter_from(self):
        return self._tables_activity() + "\n" + self._tables_investor()

    def filter_where(self):
        return self._where_activity() + "\n" + self.where_investor()

    # operation => (numeric operand, character operand, description )
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

    def _where_activity(self):
        where_act = ''
        if self.filters.get("activity", {}).get("identifier"):
            for f in self.filters.get("activity").get("identifier"):
                operation = f.get("op")
                value = ",".join(filter(None, [s.strip() for s in f.get("value").split(",")]))
                where_act += "AND a.activity_identifier %s " % self.OPERATION_MAP[operation][0] % value
        if self.filters.get("deal_scope") and self.filters.get("deal_scope") != "all":
            where_act += " AND pi.deal_scope = '%s' " % self.filters.get("deal_scope")

        if self.filters.get("activity", {}).get("tags"):
            tags = self.filters.get("activity").get("tags")
            for i, (tag, value) in enumerate(tags.items()):
                variable_operation = tag.split("__")
                variable = variable_operation[0]
                # choose operation depending on variable type default 0(int)
                operation = ""
                if len(variable_operation) > 1:
                    operation = variable_operation[1]
                # empty as operation or no value given
                if operation == "is_empty" or not value or (value and not value[0]):
                    where_act += " AND akv%(count)i.attributes->'%(variable)s' IS NULL " % {
                        "count": i, 'variable': variable
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
                            where_act += " AND ar%(count)i.name %(op)s " % {
                                "count": i,
                                "op": self.OPERATION_MAP[operation][operation_type] % v.replace("'", "\\'")
                            }
                        else:
                            # TODO: that goes for 'is' too of the field is numeric. need better condition.
                            if operation in ['lt', 'lte', 'gt', 'gte']:
                                comparator = "CAST(akv%(count)i.attributes->'%(variable)s' AS NUMERIC)" % {
                                    "count": i, 'variable': variable
                                }
                            else:
                                comparator = "akv%(count)i.attributes->'%(variable)s'" % {
                                    "count": i, 'variable': variable
                                }
                            where_act += "  %(value)s  %(year)s " % {
                                "value": v and " AND %(comparator)s %(op)s " % {
                                    'comparator': comparator,
                                    "op": self.OPERATION_MAP[operation][operation_type] % v.replace("'", "\\'"),
                                } or "",
                                "year": year and " AND akv%i.year = '%s' " % (i, year) or ""
                            }
        return where_act

    def where_investor(self):
        where_inv = ''
        if self.filters.get("investor", {}).get("tags"):
            tags = self.filters.get("investor").get("tags")
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
        return where_inv

    def _tables_activity(self):
        tables_from_act = ''
        if self.filters.get("activity", {}).get("tags"):
            tags = self.filters.get("activity").get("tags")
            for i, (tag, value) in enumerate(tags.items()):
                variable_operation = tag.split("__")
                variable = variable_operation[0]
                # join tag tables for each condition
                if variable == "region":
                    tables_from_act += "LEFT JOIN landmatrix_activityattributegroup AS akv%(count)i, countries AS ac%(count)i, regions AS ar%(count)i \n" % {"count": i}
                    tables_from_act += " ON (a.id = akv%(count)i.fk_activity_id AND akv%(count)i.attributes ? 'target_country' AND akv%(count)i.value = ac%(count)i.name AND ar%(count)i.id = ac%(count)i.fk_region)"%{"count": i, "key": variable}
                if variable.isdigit():
                    tables_from_act += "LEFT JOIN landmatrix_activityattributegroup AS akv%(count)i\n" % {"count": i}
                    tables_from_act += " ON (a.id = akv%(count)i.fk_activity_id AND akv%(count)i.key_id = '%(key)s')"%{"count": i, "key": variable}
                else:
                    tables_from_act += join_attributes("akv%(count)i" % {"count": i}, variable)
#                    tables_from_act += "LEFT JOIN landmatrix_activityattributegroup AS akv%(count)i\n" % {"count": i}
#                    tables_from_act += " ON (a.id = akv%(count)i.fk_activity_id AND akv%(count)i.attributes ? '%(key)s')"%{"count": i, "key": variable}
        return tables_from_act

    def _tables_investor(self):
        tables_from_inv = ''
        if self.filters.get("investor", {}).get("tags"):
            tags = self.filters.get("investor").get("tags")
            for i, (tag, value) in enumerate(tags.items()):
                if not value:
                    continue
                variable_operation = tag.split("__")
                variable = variable_operation[0]
                # join tag tables for each condition
                if variable == "region":
                    # tables_from_inv += "LEFT JOIN (sh_key_value_lookup skv%(count)i, countries skvc%(count)i, regions skvr%(count)i) \n" % {"count": i}
                    # tables_from_inv += " ON (skv%(count)i.stakeholder_identifier = s.stakeholder_identifier AND skv%(count)i.key = 'country' AND skv%(count)i.value = skvc%(count)i.name AND skvr%(count)i.id = skvc%(count)i.fk_region)"%{"count": i, "key": variable}
                    tables_from_inv += "LEFT JOIN countries skvc%(count)i, regions skvr%(count)i \n" % {"count": i}
                    tables_from_inv += " ON stakeholder.fk_country_id = skvc%(count)i.id AND skvr%(count)i.id = skvc%(count)i.fk_region)"%{"count": i, "key": variable}

        return tables_from_inv

