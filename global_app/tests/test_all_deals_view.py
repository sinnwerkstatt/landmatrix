__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from global_app.tests.test_view_base import TestViewBase

from django.conf import settings
from django.test import TestCase


class TestAllDealsView(TestViewBase, TestCase):

    # we use global_app as defined in landmatrix.url here because django-cms pages are not configured in test db
    VIEW_URL = '/en/global_app/all'

    "Sadly, every class derived from TestViewBase needs to explicitly call TestViewBase.setUp()"
    def setUp(self):
        TestViewBase.setUp(self)

    def test_view_contains_investor_name(self):
        if True or settings.DEBUG: print(self.content, file=open('/tmp/testresult.html', 'w'))
        self.assertIn(self.PI_NAME, self.content)

    def test_view_contains_country(self):
        from landmatrix.models import Country
        try:
            from html import unescape
            self.assertIn(Country.objects.last().name, unescape(self.content))
        except ImportError:
            self.skipTest('html.unescape needs Python >= 3.4')


# Bit of code monkeying going on here because I couldn't get the test framework to run dynamically created test cases

class TestInvestorRegionGroupView(TestViewBase, TestCase):

    VIEW_URL = '/en/global_app/by-investor-region/none/'
    def setUp(self): TestViewBase.setUp(self)

if True:

    class TestTargetCountryGroupView(TestViewBase, TestCase):

        VIEW_URL = '/en/global_app/by-target-country/none/'
        def setUp(self): TestViewBase.setUp(self)


    class TestTargetRegionGroupView(TestViewBase, TestCase):

        VIEW_URL = '/en/global_app/by-target-region/none/'
        def setUp(self): TestViewBase.setUp(self)


    class TestInvestorNameGroupView(TestViewBase, TestCase):

        VIEW_URL = '/en/global_app/by-investor-name/none/'
        def setUp(self): TestViewBase.setUp(self)


    class TestInvestorCountryGroupView(TestViewBase, TestCase):

        VIEW_URL = '/en/global_app/by-investor-country/none/'
        def setUp(self): TestViewBase.setUp(self)


    class TestIntentionGroupView(TestViewBase, TestCase):

        VIEW_URL = '/en/global_app/by-intention/none/'
        def setUp(self): TestViewBase.setUp(self)


    class TestCropGroupView(TestViewBase, TestCase):

        VIEW_URL = '/en/global_app/by-crop/none/'
        def setUp(self): TestViewBase.setUp(self)


    class TestDataSourceTypeView(TestViewBase, TestCase):

        VIEW_URL = '/en/global_app/by-data-source-type/none/'
        def setUp(self): TestViewBase.setUp(self)

if False:
    class TestYearGroupView(TestViewBase, TestCase):

        VIEW_URL = '/en/global_app/by-year/none/'
        def setUp(self): TestViewBase.setUp(self)


