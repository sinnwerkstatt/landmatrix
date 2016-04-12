
from django.http.request import HttpRequest
from django.http import QueryDict

from grid.views.export_view import ExportView, AllDealsExportView
from grid.views.table_group_view import TableGroupView

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from grid.tests.deals_test_data import DealsTestData

from django.test import TestCase

class TestViewVariables(TestCase, DealsTestData):

    def setUp(self):
        self._call_dispatch('all.csv')

    def test_csv_download_mimetype(self):
        self.create_data()
        response = AllDealsExportView.as_view()(self._request(), format='csv')
        self.assertTrue(response.has_header('Content-Type'))
        self.assertEqual('text/csv', response['Content-Type'])

    def test_csv_download_database(self):
        values = self._get_csv_data('database')

        self.assertEqual(values['target_country'], self.country.name)
        self.assertEqual(values['intention'], self.INTENTION)

        for key in AllDealsExportView.DOWNLOAD_COLUMNS:
            self.assertIn(key, values.keys())

    def test_csv_download_all(self):
        values = self._get_csv_data('all')

        for key in AllDealsExportView.DOWNLOAD_COLUMNS:
            self.assertIn(key, values.keys())

        self.assertEqual(values['target_country'], self.country.name)
        self.assertEqual(values['intention'], self.INTENTION)

    def test_csv_download_intention(self):
        values = self._get_csv_data('intention')

        for key in self.view.columns:
            self.assertIn(key, values.keys())

        # print(values)

        # self.assertEqual(int(values['deal_count']), 1)
        self.assertEqual(values['intention'], self.INTENTION)

    def test_csv_download_target_country(self):
        values = self._get_csv_data('target-country')

        for key in self.view.columns:
            self.assertIn(key, values.keys())

        # self.assertEqual(int(values['deal_count']), 1)
        self.assertEqual(values['target_country'], self.country.name)
        # self.assertEqual(values['target_region'], self.region.name)
        self.assertEqual(values['intention'], self.INTENTION)

    def test_xml_download_mimetype(self):
        self.create_data()
        response = AllDealsExportView.as_view()(self._request(), format='xml')
        self.assertTrue(response.has_header('Content-Type'))
        self.assertEqual('text/xml', response['Content-Type'])

    def test_xml_download_contains_keys(self):
        xml = self._get_xml_data('all')
        self.skipTest('Investigate which columns should be shown')
        for key in AllDealsExportView.DOWNLOAD_COLUMNS:
            self.assertIn(key, xml)

    def test_xml_download_is_valid(self):
        from xml.etree import ElementTree

        xml = self._get_xml_data('all')
        try:
            ElementTree.fromstring(xml)
        except ElementTree.ParseError:
            self.fail('Invalid XML:' + xml)

    def test_xls_download_mimetype(self):
        self.create_data()
        response = AllDealsExportView.as_view()(self._request(), format='xls')
        self.assertTrue(response.has_header('Content-Type'))
        self.assertEqual('application/ms-excel', response['Content-Type'])

    def _get_xml_data(self, group):
        self.create_data()
        response = AllDealsExportView.as_view()(self._request(), format='xml')
        # response.render()
        return response.content.decode('utf-8')
        return response.content.decode('utf-8')

    def _get_csv_data(self, group):
        self.create_data()
        self.view = AllDealsExportView()
        response = self.view.dispatch(self._request(), format='csv', group=group + '.csv')
        result = response.content.decode()
        fields = [
            list(map(lambda s: s.strip(), line.split(';')))
            for line in result.strip().split('\n')
            ]
        self.assertEqual(2, len(fields))
        values = dict(zip(fields[0], fields[1]))
        values = {key: eval(value).decode('utf-8') for key, value in values.items()}
        return values

    def _call_dispatch_with_GET(self, get_string, group=None, debug=False):
        self.view = AllDealsExportView()
        self.view.debug_query = debug
        request = self._request()
        request.GET = QueryDict(get_string)
        self.view.dispatch(request, format=group, group=group if group else 'all')

    def _call_dispatch(self, group, **kwargs):
        from django.db.utils import InternalError
        self.view = AllDealsExportView()
        try:
            response = self.view.dispatch(self._request(), group=group, format=group.split('.')[1], **kwargs)
            return response.content
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