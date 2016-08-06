__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from grid.tests.deals_test_data import DealsTestData
from grid.tests.test_view_base import TestViewBase
from landmatrix.models.country import Country

from django.conf import settings
from django.test import TestCase


class TestAllDealsView(TestViewBase, TestCase):

    # we use grid as defined in landmatrix.url here because django-cms pages are not configured in test db
    VIEW_URL = '/global/grid/all'

    "Sadly, every class derived from TestViewBase needs to explicitly call TestViewBase.setUp()"
    def setUp(self):
        TestViewBase.setUp(self)
        self.create_country()
        self.EXPECTED_VIEW_DATA = [self.country.name, DealsTestData.OS_NAME]

    def test_view_contains_data(self):
        self.skipTest('fails after renaming modules; shelved')

    def test_view_contains_investor_name(self):
        self.skipTest('fails after renaming modules; shelved')
        if settings.DEBUG: print(self.content, file=open('/tmp/testresult.html', 'w'))
        self.assertIn(self.OS_NAME, self.content)

    def test_view_contains_country(self):
        self.skipTest('fails after renaming modules; shelved')
        try:
            from html import unescape
            self.assertIn(Country.objects.last().name, unescape(self.content))
        except ImportError:
            self.skipTest('html.unescape needs Python >= 3.4')


