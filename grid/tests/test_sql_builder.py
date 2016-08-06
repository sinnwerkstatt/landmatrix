__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django.test import TestCase

from landmatrix.models.activity import Activity
from .deals_test_data import DealsTestData
from .generate_old_sql import GenerateOldSQL
from api.query_sets.sql_generation.join_functions import join_expression
from api.query_sets.sql_generation.sql_builder import SQLBuilder


class TestSQLBuilder(TestCase, DealsTestData, GenerateOldSQL):

    def test_join_expression(self):
        join = join_expression(Activity, 'a', 'local.fk_activity_id', 'id')
        self.assertTrue('LEFT JOIN landmatrix_activity' in join)
        self.assertTrue('AS a' in join)
        self.assertTrue('ON local.fk_activity_id = a.id' in join)

    def test_order_by(self):
        self._check_order_by('id', 'id  ASC')
        self._check_order_by('-id', 'id  DESC')
        self._check_order_by('id+0', 'id +0 ASC')
        self._check_order_by('-id+0', 'id +0 DESC')

    def test_limit(self):
        post = self.MINIMAL_POST
        post['filters']['limit'] = 10
        builder = SQLBuilder.create(post['filters'], post['columns'])
        self.assertIn('LIMIT 10', builder.get_limit_sql())

    def test_filters(self):

        self.skipTest('https://support.sinnwerkstatt.com/issues/158')

        post = self.MINIMAL_POST
        to_test = [
            { "activity": {"tags": {"pi_negotiation_status__in": ["Concluded (Oral Agreement)", "Concluded (Contract signed)"]}} },
            { "investor": {"tags": {"24055__is": ["0"]}} },
        ]

        for test in to_test:
            post['filters'] = test
            builder = SQLBuilder.create(post['filters'], post['columns'])
            self.assertIn(self._browse_filters_to_sql(post['filters'])['activity']['from'], builder.filter_from())
            print('\nTEST', test, ':')
            print('   should:', self._browse_filters_to_sql(post['filters'])['stakeholder']['from'])
            print('       is:', builder.filter_from())
            print('   should:', self._browse_filters_to_sql(post['filters'])['stakeholder']['where'])
            print('       is:', builder.filter_where())
            self.assertIn(self._browse_filters_to_sql(post['filters'])['stakeholder']['from'], builder.filter_from())
            self.assertIn(self._browse_filters_to_sql(post['filters'])['activity']['where'], builder.filter_where())
            self.assertIn(self._browse_filters_to_sql(post['filters'])['stakeholder']['where'], builder.filter_where())

    def _check_order_by(self, column, expected):
        post = self.MINIMAL_POST
        post['filters']['order_by'] = [column]
        builder = SQLBuilder.create(post['filters'], post['columns'])
        self.assertIn('ORDER BY', builder.get_order_sql())
        self.assertIn(expected, builder.get_order_sql())


class TestORMGeneratedQueries(TestCase, DealsTestData):

    def test_simple_join(self):
        for i in range(1,7):
            self.create_activity_with_status(
                    i, act_id=i%3+1,
#                    version=i/3+1
            )
        objects = Activity.objects.all()
        self.assertEqual(6, len(objects))
        objects = Activity.objects.filter(fk_status__name__in=['active', 'overwritten'])
        self.assertEqual(2, len(objects))

    def test_join_attributes(self):
        for i in range(1,7):
            self.create_activity_with_status(
                    i, act_id=i%3+1,
#                    version=i/3+1
            )
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

    def test_get_multiple_attributes_if_this_fails_with_string_indices_must_be_integers_theres_a_problem_with_the_django_hstore_app(self):
        self.create_activity_with_status(2)
        self.add_attributes_to_activity(Activity.objects.last(), { 'intention': 'blah' })
        self.add_attributes_to_activity(Activity.objects.last(), { 'intention': 'blub' })
        object = Activity.objects.filter(fk_status__name__in=['active', 'overwritten']). \
            filter(activityattributegroup__attributes__contains=['intention']).distinct().last()
        attributes_list = object.activityattributegroup_set.all().values('attributes')
        if not isinstance(attributes_list[0]['attributes'], dict):
            self.skipTest('django_hstore app is not included properly')
        intentions = list(map(lambda r: r['attributes']['intention'], attributes_list))
        self.assertIn('blah', intentions)
        self.assertIn('blub', intentions)

    def DISABLED_test_group_by(self):
        from django.db.models import Count
        self.create_activity_with_status(
                2, act_id=1, version=1
        )
        self.create_activity_with_status(
                2, act_id=1, version=2
        )
        self.create_activity_with_status(
                2, act_id=2, version=1
        )
        self.create_activity_with_status(
                2, act_id=2, version=2
        )
        id_1 = Activity.objects.values(
                'activity_identifier',
#                'version'
        ).annotate(Count('activity_identifier'))
        self.assertEqual(4, len(id_1))
        # id_2 = Activity.objects.values('version').annotate(Count('version'))
        # self.assertEqual(2, len(id_2))
        # for result in id_2:
        #     self.assertEqual(2, result['version__count'])


