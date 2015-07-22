__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from global_app.tests.test_view_base import TestViewBase
from django.test import TestCase

class TestAllDealsView(TestViewBase, TestCase):

    # we use global_app as defined in landmatrix.url here because django-cms pages are not configured in test db
    VIEW_URL = '/en/global_app/all'

    "Sadly, every class derived from TestViewBase needs to explicitly call TestViewBase.setUp()"
    def setUp(self):
        TestViewBase.setUp(self)


if False:

    class TestGroupView(TestViewBase, TestCase):

        # we use global_app as defined in landmatrix.url here because django-cms pages are not configured in test db
        VIEW_URL = '/en/global_app/group/by-target-country/'

        "Sadly, every class derived from TestViewBase needs to explicitly call TestViewBase.setUp()"
        def setUp(self):
            TestViewBase.setUp(self)

