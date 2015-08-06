__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django.utils import timezone
from landmatrix.views import AjaxView
from landmatrix.tests.with_status import WithStatus

class TestAjaxView(WithStatus):

    def test_first(self):
        response = self._get_url_following_redirects('/ajax/widget/values?key_id=-2&value=20&name=conditions_empty-1-value&operation=is')
        print(response.status_code)
        print(response.content.decode('utf-8'))


    def _get_url_following_redirects(self, url):
        response = self.client.get(url)
        while response.status_code in range(300, 308):
            response = self.client.get(response.url)
        return response
