
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

    def test_filters_group(self):
        self.assertEqual('all', self.download_view.filters['group_by'])
        self.assertEqual('all', self.download_view.group)
        self._call_dispatch('crop')
        self.assertEqual('crop', self.download_view.filters['group_by'])
        self.assertEqual('crop', self.download_view.group)

    def test_order_by(self):
        self.skipTest('not yet implemented')

    def test_filters_with_filter_set(self):
        self.skipTest('not yet implemented')

    def test_filters_with_filter_unset_and_group_database(self):
        self.skipTest('not yet implemented')

    def test_filters_with_filter_unset(self):
        self.skipTest('not yet implemented')

    def test_load_more(self):
        self.skipTest('not yet implemented')

    def test_download(self):
        import json
        self.create_data()

        view = TableGroupView()
        view.debug_query = True
        self.skipTest('csv export not yet functional')
        result = view.dispatch(self._request(), group='database.csv').content.decode()
        try:
            print(json.loads(result))
        except ValueError:
            print(result[:1000], '...')
            self.fail('result is not json')

    def _call_dispatch(self, group, **kwargs):
        from django.db.utils import InternalError
        self.download_view = TableGroupView()
        try:
            return self.download_view.dispatch(self._request(), group=group, **kwargs).content
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