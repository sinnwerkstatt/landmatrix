from django.test.client import Client

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class WithClientMixin:

    def setUp(self):
        self.client = Client()
