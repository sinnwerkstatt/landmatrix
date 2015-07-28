
from django.http.request import HttpRequest
from global_app.views.table_group_view import TableGroupView

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from global_app.tests.deals_test_data import DealsTestData

from django.test import TestCase

class TestViewDownload(TestCase, DealsTestData):

    VIEW_URL = '/en/global_app/all.csv'

    def test_download_set(self):
        from django.db.utils import InternalError
        download_view = TableGroupView()
        request = HttpRequest()
        try:
            download_view.dispatch(request, group='all.csv')
        except InternalError:
            pass

        self.assertTrue(download_view.is_download)

    def _get_url_following_redirects(self, url):
        response = self.client.get(url)
        while response.status_code in range(300, 308):
            response = self.client.get(response.url)
        return response
