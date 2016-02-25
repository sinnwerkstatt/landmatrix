from grid.tests.test_view_base import TestViewBase

from django.test import TestCase

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

# Bit of code monkeying going on here because I couldn't get the test framework to run dynamically created test cases


class TestTargetCountryGroupView(TestViewBase, TestCase):

    VIEW_URL = '/global/grid/by-target-country/'
    EXPECTED_VIEW_DATA = [ 'Agriculture' ]
    def setUp(self):
        TestViewBase.setUp(self)


class TestTargetRegionGroupView(TestViewBase, TestCase):

    VIEW_URL = '/global/grid/by-target-region/'
    EXPECTED_VIEW_DATA = [ 'Agriculture' ]
    def setUp(self):
        TestViewBase.setUp(self)


class TestStakeholderNameGroupView(TestViewBase, TestCase):

    VIEW_URL = '/global/grid/by-stakeholder-name/'
    EXPECTED_VIEW_DATA = [ 'Agriculture' ]
    def setUp(self):
        TestViewBase.setUp(self)


class TestStakeholderCountryGroupView(TestViewBase, TestCase):

    VIEW_URL = '/global/grid/by-stakeholder-country/'
    EXPECTED_VIEW_DATA = [ 'Agriculture' ]
    def setUp(self):
        TestViewBase.setUp(self)


class TestStakeholderRegionGroupView(TestViewBase, TestCase):

    VIEW_URL = '/global/grid/by-stakeholder-region/'
    EXPECTED_VIEW_DATA = []
    def setUp(self):
        TestViewBase.setUp(self)


class TestIntentionGroupView(TestViewBase, TestCase):

    VIEW_URL = '/global/grid/by-intention/'
    EXPECTED_VIEW_DATA = [ 'Livestock' ]
    def setUp(self):
        TestViewBase.setUp(self)


class TestCropGroupView(TestViewBase, TestCase):

    VIEW_URL = '/global/grid/by-crop/'
    EXPECTED_VIEW_DATA = [ 'Agriculture' ]
    def setUp(self):
        TestViewBase.setUp(self)


class TestDataSourceTypeView(TestViewBase, TestCase):

    VIEW_URL = '/global/grid/by-data-source-type/'
    EXPECTED_VIEW_DATA = [ 'Agriculture' ]
    def setUp(self):
        TestViewBase.setUp(self)


class TestYearGroupView(TestViewBase, TestCase):

    VIEW_URL = '/global/grid/by-year/'
    EXPECTED_VIEW_DATA = [ 'Agriculture' ]
    def setUp(self):
        TestViewBase.setUp(self)

