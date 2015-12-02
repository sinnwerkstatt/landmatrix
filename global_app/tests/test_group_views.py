from global_app.tests.test_view_base import TestViewBase

from django.test import TestCase

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

# Bit of code monkeying going on here because I couldn't get the test framework to run dynamically created test cases

class TestInvestorRegionGroupView(TestViewBase, TestCase):

    VIEW_URL = '/en/global_app/by-investor-region/none/'
    EXPECTED_VIEW_DATA = [ 'Agriculture' ]
    def setUp(self):
        TestViewBase.setUp(self)


class TestTargetCountryGroupView(TestViewBase, TestCase):

    VIEW_URL = '/en/global_app/by-target-country/none/'
    EXPECTED_VIEW_DATA = [ 'Agriculture' ]
    def setUp(self):
        TestViewBase.setUp(self)


class TestTargetRegionGroupView(TestViewBase, TestCase):

    VIEW_URL = '/en/global_app/by-target-region/none/'
    EXPECTED_VIEW_DATA = [ 'Agriculture' ]
    def setUp(self):
        TestViewBase.setUp(self)


class TestInvestorNameGroupView(TestViewBase, TestCase):

    VIEW_URL = '/en/global_app/by-investor-name/none/'
    EXPECTED_VIEW_DATA = [ 'Agriculture' ]
    def setUp(self):
        TestViewBase.setUp(self)


class TestStakeholderNameGroupView(TestViewBase, TestCase):

    VIEW_URL = '/en/global_app/by-stakeholder-name/none/'
    EXPECTED_VIEW_DATA = [ 'Agriculture' ]
    def setUp(self):
        TestViewBase.setUp(self)


class TestInvestorCountryGroupView(TestViewBase, TestCase):

    VIEW_URL = '/en/global_app/by-investor-country/none/'
    EXPECTED_VIEW_DATA = [ 'Agriculture' ]
    def setUp(self):
        TestViewBase.setUp(self)


class TestStakeholderCountryGroupView(TestViewBase, TestCase):

    VIEW_URL = '/en/global_app/by-stakeholder-country/none/'
    EXPECTED_VIEW_DATA = [ 'Agriculture' ]
    def setUp(self):
        TestViewBase.setUp(self)


class TestStakeholderRegionGroupView(TestViewBase, TestCase):

    VIEW_URL = '/en/global_app/by-stakeholder-region/none/'
    EXPECTED_VIEW_DATA = []
    def setUp(self):
        TestViewBase.setUp(self)


class TestIntentionGroupView(TestViewBase, TestCase):

    VIEW_URL = '/en/global_app/by-intention/none/'
    EXPECTED_VIEW_DATA = [ 'Livestock' ]
    def setUp(self):
        TestViewBase.setUp(self)


class TestCropGroupView(TestViewBase, TestCase):

    VIEW_URL = '/en/global_app/by-crop/none/'
    EXPECTED_VIEW_DATA = [ 'Agriculture' ]
    def setUp(self):
        TestViewBase.setUp(self)


class TestDataSourceTypeView(TestViewBase, TestCase):

    VIEW_URL = '/en/global_app/by-data-source-type/none/'
    EXPECTED_VIEW_DATA = [ 'Agriculture' ]
    def setUp(self):
        TestViewBase.setUp(self)


class TestYearGroupView(TestViewBase, TestCase):

    VIEW_URL = '/en/global_app/by-year/none/'
    EXPECTED_VIEW_DATA = [ 'Agriculture' ]
    def setUp(self):
        TestViewBase.setUp(self)

