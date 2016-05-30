from django.utils.translation import ugettext_lazy as _

from grid.forms.choices import intention_choices, get_choice_parent
from api.query_sets.sql_generation.join_functions import join_attributes

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class FilterToSQL:

    DEBUG = False

    # operation => (numeric operand, character operand, description )
    OPERATION_MAP = {
        "is":       ("= %s", "= '%s'", _("is")),
        "in":       ("IN (%s)", "IN (%s)", _("is one of")),
        "not_in":   ("NOT IN (%s)", "NOT IN (%s)", _("isn't any of")),
        "gte":      (">= %s", ">= %s", _("is >=")),
        "gt":       ("> %s", "> '%s'", _("is >")),
        "lte":      ("<= %s", "<= '%s'", _("is <=")),
        "lt":       ("< %s", "< '%s'", _("is <")),
        "contains": ("LIKE '%%%%%%%%%s%%%%%%%%'", "LIKE '%%%%%%%%%s%%%%%%%%'", _("contains")),
        "is_empty": ("IS NULL", "IS NULL", _("is empty")),
    }

    count_offset = 1

    def __init__(self, filters, columns):
        FilterToSQL.count_offset += 10
        self.filters = filters
        self.columns = columns
        if self.DEBUG:
            print('FilterToSQL: filters', self.filters)
            print('FilterToSQL: columns', self.columns)

    def filter_from(self):
        if self.DEBUG: print('FilterToSQL:  tables', self._tables_activity() + "\n" + self._tables_investor())
        return self._tables_activity() + "\n" + self._tables_investor()

    def filter_where(self):
        if self.DEBUG: print('FilterToSQL:   where', self._where_activity() + "\n" + self.where_investor())
        return self._where_activity() + "\n" + self.where_investor()

    def _where_activity(self):
        where = []
        if self.filters.get("activity", {}).get("identifier"):
            for f in self.filters.get("activity").get("identifier"):
                operation = f.get("op")
                value = ",".join(filter(None, [s.strip() for s in f.get("value").split(",")]))
                where.append("AND a.activity_identifier %s " % self.OPERATION_MAP[operation][0] % value)
        if self.filters.get("deal_scope") and self.filters.get("deal_scope") != "all":
            where.append("AND pi.deal_scope = '%s' " % self.filters.get("deal_scope"))

        if self.filters.get("activity", {}).get("tags"):
            tags = self.filters.get("activity").get("tags")
            for index, (tag, value) in enumerate(tags.items()):

                i = index+FilterToSQL.count_offset

                variable_operation = tag.split("__")
                variable = variable_operation[0]
                # choose operation depending on variable type default 0(int)
                operation = ""
                if len(variable_operation) > 1:
                    operation = variable_operation[1]
                # empty as operation or no value given
                if operation == "is_empty" or not value or (value and not value[0]):
                    where.append(
                        "AND attr_%(count)i.attributes->'%(variable)s' IS NULL " % {"count": i, 'variable': variable}
                    )
                elif operation in ("in", "not_in"):
                    # value = value[0].split(",")
                    in_values = ",".join(["'%s'" % v.strip().replace("'", "\\'") for v in value])
                    if variable == "region":
                        where.append(
                            "AND ar%(count)i.name %(op)s " % {
                                "count": i,
                                "op": self.OPERATION_MAP[operation][0] % in_values,
                            }
                        )
                    else:
                        where.append(
                            "AND SPLIT_PART(attr_%(count)i.attributes->'%(variable)s', '#', 1) %(op)s " % {
                                "count": i,
                                "op": self.OPERATION_MAP[operation][0] % in_values,
                                'variable': variable
                            }
                        )

                    # Special hack for weird results in data source filtering
                    if variable == 'type' and 'data_source_type' in self.columns:
                        # This is results in a pretty broken query, but it's a
                        # way to get the exclude media reports filter working
                        # without major surgery. Works by lining up the
                        # columns that we're joining twice :(
                        where.append(
                            """AND attr_%(count)i.attributes->'type'
                             = data_source_type.attributes->'type'""" % {
                                "count": i,
                            })
                else:

                    if self.DEBUG: print('_where_activity', index, tag, value)

                    if not isinstance(value, list):
                        value = [value]
                    for v in value:
                        year = None
                        if "##!##" in v:
                            v,year =  v.split("##!##")[0], v.split("##!##")[1]
                        operation_type = not v.isdigit() and 1 or 0
                        if variable == "region":
                            where.append(
                                "AND ar%(count)i.name %(op)s " % {
                                    "count": i,
                                    "op": self.OPERATION_MAP[operation][operation_type] % v.replace("'", "\\'")
                                }
                            )
                        else:
                            if operation in ['lt', 'lte', 'gt', 'gte'] or operation == 'is' and str(v).isnumeric():
                                comparator = "CAST(SPLIT_PART(attr_%(count)i.attributes->'%(variable)s', '#', 1) AS NUMERIC)" % {
                                    "count": i, 'variable': variable
                                }
                            else:
                                comparator = "SPLIT_PART(attr_%(count)i.attributes->'%(variable)s', '#', 1)" % {
                                    "count": i, 'variable': variable
                                }
                            where.append(
                                v and "AND %(comparator)s %(op)s " % {
                                        'comparator': comparator,
                                        "op": self.OPERATION_MAP[operation][operation_type] % v.replace("'", "\\'"),
                                    } or ""
                            )
                # TODO: move this somewhere else, this function is too complicated
                # TODO: optimize SQL? This query seems painful, it could be
                # better as an array_agg possibly
                if operation == 'is':
                    # 'Is' operations requires that we exclude other values,
                    # otherwise it's just the same as contains

                    allowed_values = None
                    if variable == 'intention':
                        # intentions can be nested, for example all biofuels
                        # deals are also agriculture (parent of biofuels)
                        parent_value = get_choice_parent(v, intention_choices)
                        if parent_value:
                            allowed_values = (
                                parent_value,
                                v.replace("'", "\\'"),
                            )

                    if not allowed_values:
                        allowed_values = (v.replace("'", "\\'"),)

                    where.append("""
                        AND a.id NOT IN (
                            SELECT fk_activity_id
                            FROM landmatrix_activityattributegroup 
                            WHERE landmatrix_activityattributegroup.attributes ? '%(variable)s'
                            AND SPLIT_PART(landmatrix_activityattributegroup.attributes->'%(variable)s', '#', 1) NOT IN ('%(value)s')
                        )
                        """ % {
                        'variable': variable,
                        'value': "', '".join([str(v) for v in allowed_values]),
                    })

        return '\n'.join(where)

    def where_investor(self):
        where_inv = ''
        if self.filters.get("investor", {}).get("tags"):
            tags = self.filters.get("investor").get("tags")
            for index, (tag, value) in enumerate(tags.items()):
                i = index+FilterToSQL.count_offset
                if not value:
                    continue
                variable_operation = tag.split("__")
                variable = variable_operation[0]
                # if self.DEBUG: print('FilterToSQL.where_investor:', index, tag, value, variable_operation)

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
                    if not isinstance(value, list):
                        value = [value]
                    for v in value:

                        operation_type = not v.isdigit() and 1 or 0

                        if self.DEBUG: print('FilterToSQL.where_investor:', index, variable, operation, v, operation_type)

                        if variable == "region":
                            where_inv += " AND skvr%i.name %s" % (i, self.OPERATION_MAP[operation][operation_type] % v.replace("'", "\\'"))
                        elif 'country' in variable:
                            where_inv += ' AND stakeholder.fk_country_id = {}'.format(v)
                        elif 'investor' == variable:
                            where_inv += ' AND stakeholder.investor_identifier = {}'.format(v)
                        else:
                            where_inv += " AND skv%i.value %s" % (i, self.OPERATION_MAP[operation][operation_type] % v.replace("'", "\\'"))
        return where_inv

    def _tables_activity(self):
        tables_from = []
        if self.filters.get("activity", {}).get("tags"):
            tags = self.filters.get("activity").get("tags")
            for index, (tag, value) in enumerate(tags.items()):
                i = index+FilterToSQL.count_offset
                variable_operation = tag.split("__")
                variable = variable_operation[0]

                # join tag tables for each condition
                if variable == "region":
                    tables_from.append(
                        "LEFT JOIN landmatrix_activityattributegroup AS attr_%(count)i, countries AS ac%(count)i, regions AS ar%(count)i \n" % {"count": i} +\
                        " ON (a.id = attr_%(count)i.fk_activity_id AND attr_%(count)i.attributes ? 'target_country' AND attr_%(count)i.value = ac%(count)i.name AND ar%(count)i.id = ac%(count)i.fk_region)"%{"count": i, "key": variable}
                    )
                elif variable.isdigit():
                    tables_from.append(
                        "LEFT JOIN landmatrix_activityattributegroup AS attr_%(count)i\n" % {"count": i} +\
                        " ON (a.id = attr_%(count)i.fk_activity_id AND attr_%(count)i.key_id = '%(key)s')"%{"count": i, "key": variable}
                    )
                else:
                    tables_from.append(join_attributes("attr_%(count)i" % {"count": i}, variable))
        return '\n'.join(tables_from)

    def _tables_investor(self):
        tables_from_inv = ''
        if self.filters.get("investor", {}).get("tags"):
            tags = self.filters.get("investor").get("tags")
            for index, (tag, value) in enumerate(tags.items()):
                if self.DEBUG: print('FilterToSQL._tables_investor:', index, tag, value)
                i = index+FilterToSQL.count_offset
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
                elif 'country' in variable:
                    pass

        if self.DEBUG: print('FilterToSQL._tables_investor tables:', tables_from_inv)
        return tables_from_inv

