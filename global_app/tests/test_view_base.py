__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from .deals_test_data import DealsTestData


class TestViewBase(DealsTestData):

    def setUp(self):
        self.create_data()
        self.content = self.get_url_following_redirects(self.VIEW_URL).content.decode('utf-8')

    # disabled because no django-cms pages configured, but redirects are applied
    def _test_anything_loads(self):
        response = self.get_url_following_redirects('/')
        print(response.content.decode('utf-8'))
        self.assertEqual(200, response.status_code)

    def test_view_loads(self):
        response = self.get_url_following_redirects(self.VIEW_URL)
        self.assertEqual(200, response.status_code)

    def get_url_following_redirects(self, url):
        response = self.client.get(url)
        while response.status_code in range(300, 308):
            response = self.client.get(response.url)
        return response

