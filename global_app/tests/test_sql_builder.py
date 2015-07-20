__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django.test import TestCase
from django.utils.translation import ugettext_lazy as _

from landmatrix.models import Activity
from .deals_test_data import DealsTestData

from global_app.views.sql_builder import join_expression, SQLBuilder

class TestSQLBuilder(TestCase, DealsTestData):

    def test_join_expression(self):
        join = join_expression(Activity, 'a', 'local.fk_activity_id', 'id')
        self.assertTrue('LEFT JOIN landmatrix_activity' in join)
        self.assertTrue('AS a' in join)
        self.assertTrue('ON local.fk_activity_id = a.id' in join)

    def test_compare_to_v1_data(self):
        import os
        from subprocess import call
        dir = os.path.dirname(os.path.realpath(__file__))
        num_errors = call(['python', dir+'/compare_sql_results.py'])
        self.assertEqual(0, num_errors)

    def test_order_by(self):
        self._check_order_by('id', 'id  ASC')
        self._check_order_by('-id', 'id  DESC')
        self._check_order_by('id+0', 'id +0 ASC')
        self._check_order_by('-id+0', 'id +0 DESC')

    def test_limit(self):
        post = self.MINIMAL_POST
        post['filters']['limit'] = 10
        builder = SQLBuilder.create(post['columns'], post['filters'])
        self.assertIn('LIMIT 10', builder.get_limit_sql())

    def test_filters(self):
        from global_app.views.dummy_activity_protocol import DummyActivityProtocol
        post = self.MINIMAL_POST
        to_test = [
            { "activity": {"tags": {"pi_negotiation_status__in": ["Concluded (Oral Agreement)", "Concluded (Contract signed)"]}} },
            { "investor": {"tags": {"24055__is": ["0"]}} },
        ]

        for test in to_test:
            post['filters'] = test
            builder = SQLBuilder.create(post['columns'], post['filters'])
            self.assertIn(self._browse_filters_to_sql(post['filters'])['activity']['from'], builder.filter_from())
            self.assertIn(self._browse_filters_to_sql(post['filters'])['investor']['from'], builder.filter_from())
            self.assertIn(self._browse_filters_to_sql(post['filters'])['activity']['where'], builder.filter_where())
            self.assertIn(self._browse_filters_to_sql(post['filters'])['investor']['where'], builder.filter_where())

    def _check_order_by(self, column, expected):
        post = self.MINIMAL_POST
        post['filters']['order_by'] = [column]
        builder = SQLBuilder.create(post['columns'], post['filters'])
        self.assertIn('ORDER BY', builder.get_order_sql())
        self.assertIn(expected, builder.get_order_sql())

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
                    from global_app.views.sql_builder import join_attributes
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


class TestORMGeneratedQueries(TestCase, DealsTestData):

    def test_simple_join(self):
        for i in range(1,7):
            self.create_activity_with_status(i, act_id=i%3+1, version=i/3+1)
        objects = Activity.objects.all()
        self.assertEqual(6, len(objects))
        objects = Activity.objects.filter(fk_status__name__in=['active', 'overwritten'])
        self.assertEqual(2, len(objects))

    def test_join_attributes(self):
        for i in range(1,7):
            self.create_activity_with_status(i, act_id=i%3+1, version=i/3+1)
            self.add_attributes_to_activity(Activity.objects.last(), { 'intention': 'blah' })
        objects = Activity.objects.filter(fk_status__name__in=['active', 'overwritten']). \
            filter(activityattributegroup__attributes__contains=['intention'])
        self.assertEqual(2, len(objects))

    def test_join_multiple_attributes(self):
        self.create_activity_with_status(2)
        self.add_attributes_to_activity(Activity.objects.last(), { 'intention': 'blah' })
        self.add_attributes_to_activity(Activity.objects.last(), { 'intention': 'blub' })
        objects = Activity.objects.filter(fk_status__name__in=['active', 'overwritten']). \
            filter(activityattributegroup__attributes__contains=['intention'])
        self.assertEqual(2, len(objects))
        objects = Activity.objects.filter(fk_status__name__in=['active', 'overwritten']). \
            filter(activityattributegroup__attributes__contains=['intention']).distinct()
        self.assertEqual(1, len(objects))

    def test_get_multiple_attributes(self):
        self.create_activity_with_status(2)
        self.add_attributes_to_activity(Activity.objects.last(), { 'intention': 'blah' })
        self.add_attributes_to_activity(Activity.objects.last(), { 'intention': 'blub' })
        object = Activity.objects.filter(fk_status__name__in=['active', 'overwritten']). \
            filter(activityattributegroup__attributes__contains=['intention']).distinct().last()
        intentions = list(map(lambda r: r['attributes']['intention'], object.activityattributegroup_set.all().values('attributes')))
        self.assertIn('blah', intentions)
        self.assertIn('blub', intentions)

    def test_group_by(self):
        from django.db.models import Count
        self.create_activity_with_status(2, act_id=1, version=1)
        self.create_activity_with_status(2, act_id=1, version=2)
        self.create_activity_with_status(2, act_id=2, version=1)
        self.create_activity_with_status(2, act_id=2, version=2)
        id_1 = Activity.objects.values('activity_identifier', 'version').annotate(Count('activity_identifier'))
        self.assertEqual(4, len(id_1))
        id_2 = Activity.objects.values('version').annotate(Count('version'))
        self.assertEqual(2, len(id_2))
        for result in id_2:
            self.assertEqual(2, result['version__count'])


