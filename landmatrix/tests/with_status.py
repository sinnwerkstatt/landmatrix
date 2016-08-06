__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django.test import TestCase
from landmatrix.models.status import Status

class WithStatus(TestCase):
    def setUp(self):
        self.status = Status.objects.get(id=1)
