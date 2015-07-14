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

#    def test_