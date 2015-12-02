__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from global_app.tests.deals_test_data import DealsTestData
from global_app.tests.test_view_base import TestViewBase
from landmatrix.models import Country

from django.conf import settings
from django.test import TestCase


class TestAllDealsView(TestViewBase, TestCase):

    # we use global_app as defined in landmatrix.url here because django-cms pages are not configured in test db
    VIEW_URL = '/en/global_app/all'

    "Sadly, every class derived from TestViewBase needs to explicitly call TestViewBase.setUp()"
    def setUp(self):
        TestViewBase.setUp(self)
        self.create_country()
        self.EXPECTED_VIEW_DATA = [ self.country.name, DealsTestData.PI_NAME ]

    def test_view_contains_investor_name(self):
        if settings.DEBUG: print(self.content, file=open('/tmp/testresult.html', 'w'))
        self.assertIn(self.PI_NAME, self.content)

    def test_view_contains_country(self):
        try:
            from html import unescape
            self.assertIn(Country.objects.last().name, unescape(self.content))
        except ImportError:
            self.skipTest('html.unescape needs Python >= 3.4')


