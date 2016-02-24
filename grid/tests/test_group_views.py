from grid.tests.test_view_base import TestViewBase

from django.test import TestCase

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

# Bit of code monkeying going on here because I couldn't get the test framework to run dynamically created test cases


class TestTargetCountryGroupView(TestViewBase, TestCase):

    VIEW_URL = '/en/grid/by-target-country/none/'
    EXPECTED_VIEW_DATA = [ 'Agriculture' ]
    def setUp(self):
        TestViewBase.setUp(self)


class TestTargetRegionGroupView(TestViewBase, TestCase):

    VIEW_URL = '/en/grid/by-target-region/none/'
    EXPECTED_VIEW_DATA = [ 'Agriculture' ]
    def setUp(self):
        TestViewBase.setUp(self)


class TestStakeholderNameGroupView(TestViewBase, TestCase):

    VIEW_URL = '/en/grid/by-stakeholder-name/none/'
    EXPECTED_VIEW_DATA = [ 'Agriculture' ]
    def setUp(self):
        TestViewBase.setUp(self)


class TestStakeholderCountryGroupView(TestViewBase, TestCase):

    VIEW_URL = '/en/grid/by-stakeholder-country/none/'
    EXPECTED_VIEW_DATA = [ 'Agriculture' ]
    def setUp(self):
        TestViewBase.setUp(self)


class TestStakeholderRegionGroupView(TestViewBase, TestCase):

    VIEW_URL = '/en/grid/by-stakeholder-region/none/'
    EXPECTED_VIEW_DATA = []
    def setUp(self):
        TestViewBase.setUp(self)


class TestIntentionGroupView(TestViewBase, TestCase):

    VIEW_URL = '/en/grid/by-intention/none/'
    EXPECTED_VIEW_DATA = [ 'Livestock' ]
    def setUp(self):
        TestViewBase.setUp(self)


class TestCropGroupView(TestViewBase, TestCase):

    VIEW_URL = '/en/grid/by-crop/none/'
    EXPECTED_VIEW_DATA = [ 'Agriculture' ]
    def setUp(self):
        TestViewBase.setUp(self)


class TestDataSourceTypeView(TestViewBase, TestCase):

    VIEW_URL = '/en/grid/by-data-source-type/none/'
    EXPECTED_VIEW_DATA = [ 'Agriculture' ]
    def setUp(self):
        TestViewBase.setUp(self)


class TestYearGroupView(TestViewBase, TestCase):

    VIEW_URL = '/en/grid/by-year/none/'
    EXPECTED_VIEW_DATA = [ 'Agriculture' ]
    def setUp(self):
        TestViewBase.setUp(self)

