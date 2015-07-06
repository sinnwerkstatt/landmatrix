__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django.test import TestCase
from landmatrix.models import Activity

from global_app.views.sql_builder import join_expression
class TestSQLBuilder(TestCase):

    def test_join_expression(self):
        self.assertTrue(
            'LEFT JOIN landmatrix_activity AS a ON local.fk_activity_id = a.id' in
            join_expression(Activity, 'a', 'local.fk_activity_id', 'id')
        )
        self.assertTrue(join_expression(Activity, 'a', 'local.fk_activity_id', 'id').endswith(' '))
