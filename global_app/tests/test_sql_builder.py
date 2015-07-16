__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django.test import TestCase
from landmatrix.models import Activity

from global_app.views.sql_builder import join_expression

class TestSQLBuilder(TestCase):

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

from .deals_test_data import DealsTestData
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


