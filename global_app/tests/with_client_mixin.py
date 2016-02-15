from django.test.client import Client

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class WithClientMixin:

    def setUp(self):
        self.client = Client()

    def _get_url_following_redirects(self, url):
        response = self.client.get(url)
        while response.status_code in range(300, 308):
            response = self.client.get(response.url)
        return response


