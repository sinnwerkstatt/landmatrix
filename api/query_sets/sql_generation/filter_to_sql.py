
from django.utils.translation import ugettext_lazy as _

from grid.forms.choices import intention_choices, get_choice_parent
from api.query_sets.sql_generation.join_functions import (
    join_attributes, join_expression,
)
from api.query_sets.sql_generation.sql_builder_data import SQLBuilderData
from api.filters import FILTER_OPERATION_MAP


__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class FilterToSQL:

    DEBUG = False
    OPERATION_MAP = FILTER_OPERATION_MAP

    count_offset = 1

    def __init__(self, filters, columns):
        FilterToSQL.count_offset += 10
        self.filters = filters
        self.columns = columns
        if self.DEBUG:
            print('FilterToSQL: filters', self.filters)
            print('FilterToSQL: columns', self.columns)

    def filter_from(self):
        from_activity = self._tables_activity()
        from_investor = self._tables_investor()
        if self.DEBUG:
            print('FilterToSQL:  tables', from_activity, "\n", from_investor)

        return "\n".join([from_activity, from_investor])

    def filter_where(self):
        where_activity = self._where_activity()
        where_investor = self.where_investor()
        if self.DEBUG:
            print('FilterToSQL:   where', where_activity, "\n", where_investor)
        return "\n".join([where_activity, where_investor])

    def _where_activity(self, taggroup=None, last_index=0):
        # TODO: Split this beast up a bit better
        # TODO: lots of sql injection vulnerabilities here
        where = []
        if taggroup:
            where.append('AND (')
        else:
            where.extend(self._where_activity_identifier())
            where.extend(self._where_activity_deal_scope())

        tags = taggroup or self.filters.get("activity", {}).get("tags", {})
        for index, (tag, value) in enumerate(tags.items()):
            i = last_index + index
            # Multiple rules?
            if isinstance(value, dict):
                where.append(self._where_activity(taggroup=value, last_index=i))
                last_index += len(value) - 1
                continue
            # Relation
            relation = ''
            if taggroup:
                relation = index > 0 and 'OR' or ''
            else:
                relation = 'AND'
            # Replace boolean
            if value == 'on':
                value = 'True'
            if not isinstance(value, list):
                value = [value]
            sanitized_values = [v.strip().replace("'", "\\'") for v in value]

            try:
                variable, key, operation = tag.split("__")
            except ValueError:
                variable = tag
                key = 'value'
                operation = None
                operation_sql = None
            else:
                operation_sql = self.OPERATION_MAP[operation][0]

            if variable == 'activity_identifier':
                where.append(
                    "%(relation)s a.activity_identifier %(operation)s" % {
                        'relation': relation,
                        'operation': operation_sql % value[0],
                    }
                )
            # empty as operation or no value given
            elif operation == "is_empty" or not value[0]:
                where.append(
                    "%(relation)s attr_%(count)i.name = '%(variable)s' AND attr_%(count)i.%(key)s IS NULL " % {
                        'relation': relation,
                        'count': i,
                        'variable': variable,
                        'key': key,
                    }
                )
            elif operation in ("in", "not_in"):
                in_values = ",".join(
                    ["'%s'" % value for value in sanitized_values])
                if variable == 'target_region':
                    where.append(
                        "%(relation)s ar%(count)i.name %(op)s " % {
                            'relation': relation,
                            "count": i,
                            "op": operation_sql % in_values,
                        }
                    )
                elif variable in 'deal_country':
                    where.append(
                        "%(relation)s ac%(count)i.%(key)s %(op)s " % {
                            'relation': relation,
                            "count": i,
                            "op": operation_sql % in_values,
                            'key': key,
                        }
                    )
                else:
                    where.append(
                        "%(relation)s attr_%(count)i.name = '%(variable)s' AND "
                        "attr_%(count)i.%(key)s %(op)s " % {
                            'relation': relation,
                            "count": i,
                            "key": key,
                            "op": operation_sql % in_values,
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
                        """%(relation)s attr_d%(count)i.name = 'type'
                           AND attr_d%(count)i.value = data_source_type.value""" % {
                            'relation': relation,
                            "count": i,
                        })
            elif operation == 'is' and variable in ('target_region', 'deal_country'):
                where.append(
                    "%(relation)s ar%(count)i.id %(op)s " % {
                        'relation': relation,
                        "count": i,
                        "op": operation_sql % value[-1].replace("'", "\\'"),
                    }
                )
            else:
                if self.DEBUG:
                    print('_where_activity', index, tag, value)

                for v in value:
                    year = None
                    if "##!##" in v:
                        v, year = v.split("##!##")[0], v.split("##!##")[1]
                    operation_type = not v.isdigit() and 1 or 0
                    operation_sql = self.OPERATION_MAP[operation][operation_type]
                    if variable == "region":
                        where.append(
                            "%(relation)s ar%(count)i.name %(op)s " % {
                                'relation': relation,
                                "count": i,
                                "op": operation_sql % v.replace("'", "\\'")
                            }
                        )
                    else:
                        if operation in ('lt', 'lte', 'gt', 'gte', 'is') and str(v).isnumeric():
                            comparator = "attr_%(count)i.name = '%(variable)s' AND CAST(attr_%(count)i.%(key)s AS DECIMAL)" % {
                                "count": i,
                                'variable': variable,
                                'key': key,
                            }
                        else:
                            comparator = "attr_%(count)i.name = '%(variable)s' AND attr_%(count)i.%(key)s" % {
                                "count": i,
                                'variable': variable,
                                'key': key,
                            }
                        where.append(
                            v and "%(relation)s %(comparator)s %(op)s " % {
                                'relation': relation,
                                'comparator': comparator,
                                "op": operation_sql % v.replace("'", "\\'"),
                            } or ""
                        )
            is_operation_limits = self._where_activity_filter_is_operator(
                variable, operation, value)
            where.extend(is_operation_limits)
        if taggroup:
            where.append(')')
        return '\n'.join(where)

    def _where_activity_identifier(self):
        # TODO: I don't think this is used anymore?
        where = []

        if self.filters.get("activity", {}).get("identifier"):
            for f in self.filters.get("activity").get("identifier"):
                operation = f.get("op")
                value = ",".join(filter(None, [s.strip() for s in f.get("value").split(",")]))
                where.append("AND a.activity_identifier %s " % self.OPERATION_MAP[operation][0] % value)

        return where

    def _where_activity_deal_scope(self):
        where = []
        if self.filters.get("deal_scope") and self.filters.get("deal_scope") != "all":
            where.append("AND a.deal_scope = '%s' " % self.filters.get("deal_scope"))

        return where

    def _where_activity_filter_is_operator(self, variable, operation, value):
        where = []
        # TODO: optimize SQL? This query seems painful, it could be
        # better as an array_agg possibly
        if operation == 'is' and variable not in ('deal_country', 'target_country', 'target_region', 'investor_country', 'investor_region'):
            # 'Is' operations requires that we exclude other values,
            # otherwise it's just the same as contains

            allowed_values = None
            if variable == 'intention':
                # intentions can be nested, for example all biofuels
                # deals are also agriculture (parent of biofuels)
                parent_value = get_choice_parent(value[-1], intention_choices)
                if parent_value:
                    allowed_values = (
                        parent_value,
                        value[-1].replace("'", "\\'"),
                    )

            if not allowed_values:
                allowed_values = (value[-1].replace("'", "\\'"),)

            # Exclude deals with given AND other values
            where.append("""
                AND a.id NOT IN (
                    SELECT fk_activity_id
                    FROM landmatrix_activityattribute
                    WHERE landmatrix_activityattribute.name = '%(variable)s'
                    AND landmatrix_activityattribute.value NOT IN ('%(value)s')
                )
                """ % {
                'variable': variable,
                'value': "', '".join([str(v) for v in allowed_values]),
            })

        return where

    def _tables_activity(self, taggroup=None, last_index=0):
        tables_from = []
        #if self.filters.get("activity", {}).get("tags"):
        tags = taggroup or self.filters.get("activity").get("tags")
        for index, (tag, value) in enumerate(tags.items()):
            i = last_index + index
            # Multiple rules?
            if isinstance(value, dict):
                tables_from.append(self._tables_activity(taggroup=value, last_index=i))
                last_index += len(value) - 1
                continue
            variable_operation = tag.split("__")
            variable = variable_operation[0]

            # join tag tables for each condition
            if variable == 'activity_identifier':
                continue
            elif variable in ('target_region', 'deal_country'):
                tables_from.append(
                    """
                    LEFT JOIN landmatrix_activityattribute AS attr_%(count)i
                    ON (a.id = attr_%(count)i.fk_activity_id AND attr_%(count)i.name = 'target_country')
                    """ % {
                        'count': i,
                    })
                tables_from.append(
                    """
                    LEFT JOIN landmatrix_country AS ac%(count)i
                    ON CAST(attr_%(count)i.value AS NUMERIC) = ac%(count)i.id
                    """ % {
                        'count': i,
                    })
                if variable == 'target_region':
                    tables_from.append(
                        """
                        LEFT JOIN landmatrix_region AS ar%(count)i
                        ON ar%(count)i.id = ac%(count)i.fk_region_id
                        """ % {
                            'count': i,
                        })
            elif variable.isdigit():
                tables_from.append(
                    "LEFT JOIN landmatrix_activityattribute AS attr_%(count)i\n" \
                    " ON (a.id = attr_%(count)i.fk_activity_id AND attr_%(count)i.key_id = '%(key)s')" % {
                        "count": i,
                        "key": variable
                    }
                )
            else:
                tables_from.append(join_attributes("attr_%(count)i" % {"count": i}, variable))
        return '\n'.join(tables_from)

    def where_investor(self):
        where_inv = ''
        tags = self.filters.get("investor", {}).get("tags", {})
        for index, (tag, value) in enumerate(tags.items()):
            i = index + FilterToSQL.count_offset

            if not value:
                continue

            try:
                variable, key, operation = tag.split("__")
            except ValueError:
                variable = tag
                key = 'value'
                operation = 'is'

            if operation == "is_empty" or not value or (value and not value[0]):
                where_inv += " AND opsh_{count}.id IS NULL ".format(count)
            elif operation in ("in", "not_in"):
                value = value[0].split(",")
                in_values = ",".join(["'%s'" % v.strip().replace("'", "\\'") for v in value])
                op_sql = self.OPERATION_MAP[operation][0] % in_values
                if variable == "operational_stakeholder_region":
                    where_inv += "AND opsh_region_{count}.id {op}".format(
                        count=i, op=op_sql)
                elif variable == "operational_stakeholder_country":
                    where_inv += "AND opsh_country_{count}.id {op}".format(
                        count=i, op=op_sql)
                else:
                    where_inv += "AND opsh_{count}.id {op}".format(
                        count=i, op=op_sql)
            else:
                if not isinstance(value, list):
                    value = [value]

                for v in value:
                    operation_type = not v.isdigit() and 1 or 0
                    op_sql = self.OPERATION_MAP[operation][operation_type] % v.replace("'", "\\'")

                    if self.DEBUG:
                        print('FilterToSQL.where_investor:', index, variable, operation, v, operation_type)

                    if variable == 'operational_stakeholder_region':
                        where_inv += "AND opsh_region_{count}.id {op}".format(
                            count=i, op=op_sql)
                    elif variable == 'operational_stakeholder_country':
                        where_inv += "AND opsh_country_{count}.id {op}".format(
                            count=i, op=op_sql)
                    elif variable == 'investor':
                        where_inv += ' AND sh.investor_identifier = {}'.format(v)
                    elif variable == 'operational_stakeholder' and operation != 'contains':
                        where_inv += " AND opsh_%i.id %s" % (i, self.OPERATION_MAP[operation][operation_type] % v.replace("'", "\\'"))
                    else:
                        where_inv += " AND opsh_%i.name %s" % (i, self.OPERATION_MAP[operation][operation_type] % v.replace("'", "\\'"))

        return where_inv

    def _tables_investor(self):
        # TODO: resuse previous joins. This duplicates a lot of SQLBuilderData
        investor_tables = []
        tags = self.filters.get("investor", {}).get("tags", {})

        for index, (tag, value) in enumerate(tags.items()):
            i = index + FilterToSQL.count_offset

            if value:
                variable = tag.split("__")[0]

            investor_tables.extend([
                join_expression(
                    'landmatrix_investoractivityinvolvement',
                    'iai_{count}'.format(count=i), 'a.id', 'fk_activity_id'),
                join_expression(
                    'landmatrix_investor', 'opsh_{count}'.format(count=i),
                    'iai_{count}.fk_investor_id'.format(count=i)),
                join_expression(
                    'landmatrix_investorventureinvolvement',
                    'ivi_{count}'.format(count=i),
                    'opsh_{count}.id'.format(count=i), 'fk_venture_id'),
                join_expression(
                    'landmatrix_investor', 'sh_{count}'.format(count=i),
                    'ivi_{count}.fk_investor_id'.format(count=i)),
                ])

            is_country_or_region = variable in (
                'operational_stakeholder_country',
                'operational_stakeholder_region',
            )

            if is_country_or_region:
                country_join = join_expression(
                    'landmatrix_country',
                    'opsh_country_{count}'.format(count=i),
                    'opsh_{count}.fk_country_id'.format(count=i))
                investor_tables.append(country_join)

            if variable == 'operational_stakeholder_region':
                region_join = join_expression(
                    'landmatrix_region',
                    'opsh_region_{count}'.format(count=i),
                    'opsh_region_{count}.fk_region_id'.format(count=i))
                investor_tables.append(region_join)

        return '\n'.join(investor_tables)
