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
