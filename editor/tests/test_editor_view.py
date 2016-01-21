from django.test import TestCase
from django.test.client import Client
from django.conf import settings

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class TestEditorView(TestCase):

    def setUp(self):
        self.client = Client()

    def test_user_not_logged_in(self):
        url, response = self._get_url_following_redirects('/editor')
        self.assertEqual(200, response.status_code)
        self.assertIn(settings.LOGIN_URL, url)

    def _get_url_following_redirects(self, url):
        response = self.client.get(url)
        while response.status_code in range(300, 308):
            url = response.url
            response = self.client.get(url)
        return url, response