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

if True:

    class TestGroupView(TestViewBase, TestCase):

        # we use global_app as defined in landmatrix.url here because django-cms pages are not configured in test db
        VIEW_URL = '/en/global_app/crop/by-target-country/'

        "Sadly, every class derived from TestViewBase needs to explicitly call TestViewBase.setUp()"
        def setUp(self):
            TestViewBase.setUp(self)

