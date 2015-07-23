__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from .deals_test_data import DealsTestData

def extract_tag(string, open_tag, close_tag):
    start = string.find('>', string.find(open_tag))
    if start < 0: return ''
    end = string.find(close_tag, start)
    return string[start+1:end]


class TestViewBase(DealsTestData):

    """Sadly, every class derived from TestViewBase needs to explicitly call TestViewBase.setUp()"""
    def setUp(self):
        self.create_data()
        self.content = self._get_url_following_redirects(self.VIEW_URL).content.decode('utf-8')

    # disabled because no django-cms pages configured, but redirects are applied
    def _test_anything_loads(self):
        response = self._get_url_following_redirects('/')
        print(response.content.decode('utf-8'))
        self.assertEqual(200, response.status_code)

    def test_view_loads(self):
        response = self._get_url_following_redirects(self.VIEW_URL)
        self.assertEqual(200, response.status_code)

    def test_view_contains_data(self):
        tbody = extract_tag(self.content, '<tbody>', '</tbody>')
        self.assertNotEqual(tbody, '', self.__class__.__name__ + ' does not find any data.')

    def test_view_data_ok(self):
        tbody = extract_tag(self.content, '<tbody>', '</tbody>')
        print(list(map(self._extract_info_from_cell, self._extract_cells(tbody))))

    def _get_url_following_redirects(self, url):
        response = self.client.get(url)
        while response.status_code in range(300, 308):
            response = self.client.get(response.url)
        return response

    def _extract_cells(self, tbody, found=list()):
        start = tbody.find('<td')
        if start < 0: return found
        realstart = tbody.find('>', start)
        end = tbody.find('</td>', realstart)
        return self._extract_cells(tbody[end+1:], found + [tbody[realstart+1:end].strip()])

    def _extract_info_from_cell(self, cell):
        if '<a href="' in cell: return self._extract_info_from_a(cell)
        return cell

    def _extract_info_from_a(self, cell):
        return extract_tag(cell, '<a href="', '</a>')

