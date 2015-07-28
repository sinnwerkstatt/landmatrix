
from django.http.request import HttpRequest
from global_app.views.table_group_view import TableGroupView

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from global_app.tests.deals_test_data import DealsTestData

from django.test import TestCase

class TestViewVariables(TestCase, DealsTestData):

    def setUp(self):
        self._call_dispatch('all.csv')

    def test_download_set(self):
        self.assertTrue(self.download_view.is_download)

    def test_group_value_set_correctly(self):
        self.assertFalse(self.download_view.group_value.endswith('.csv'))
        self.assertFalse(self.download_view.group.endswith('.csv'))

    def test_no_download(self):
        self._call_dispatch('all')
        self.assertFalse(self.download_view.is_download)

    def test_columns(self):
        self.assertEqual(self.download_view.DOWNLOAD_COLUMNS, self.download_view.columns)

    def test_columns_2(self):
        self._call_dispatch('all')
        self.assertEqual(self.download_view.group_columns_list, self.download_view.columns)

    def test_columns_3(self):
        self._call_dispatch('by-crop')
        self.assertNotEqual(self.download_view.group_columns_list, self.download_view.columns)
        self.assertNotEqual(self.download_view.DOWNLOAD_COLUMNS, self.download_view.columns)
        self.assertIn('crop', self.download_view.columns)

    def test_filters(self):
        print('filters:', self.download_view.filters)
        self._call_dispatch('crop')
        print('filters:', self.download_view.filters)
        self.skipTest('not yet implemented')


    def _call_dispatch(self, group, **kwargs):
        from django.db.utils import InternalError
        self.download_view = TableGroupView()
        try:
            self.download_view.dispatch(self._request(), group=group, **kwargs)
        except InternalError:
            pass


    def _request(self):
        class User:
            is_authenticated = lambda x: False

        from django.test.client import RequestFactory
        rf = RequestFactory()

        request = rf.get('')
        request.current_page = 0
        request.user = User()
        request.session = {}
        return request