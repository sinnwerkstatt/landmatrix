
from django.test import TestCase

from global_app.forms.base_form import BaseForm

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class TestForms(TestCase):

    def test_base_form_instantiates(self):
        form = BaseForm()