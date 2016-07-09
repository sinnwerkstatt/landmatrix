__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

import re
from django import forms
from django.utils.translation import ugettext_lazy as _

from grid.widgets.year_based_widget import YearBasedWidget

class YearBasedSelect(YearBasedWidget):

    def __init__(self, *args, **kwargs):
        self.choices = kwargs.pop("choices")
        self.widget = forms.Select(choices=self.choices, attrs={"class": "year-based"})
        super(YearBasedSelect, self).__init__(*args, **kwargs)


class YearBasedSelectMultiple(YearBasedWidget):

    def __init__(self, *args, **kwargs):
        self.choices = kwargs.pop("choices")
        self.widget = forms.SelectMultiple(choices=self.choices, attrs={"class": "year-based"})
        super(YearBasedSelectMultiple, self).__init__(*args, **kwargs)


class YearBasedSelectMultipleNumber(YearBasedWidget):

    def __init__(self, *args, **kwargs):
        self.choices = kwargs.pop("choices")
        super(YearBasedSelectMultipleNumber, self).__init__(*args, **kwargs)

    def get_widgets(self):
        return [
        	forms.SelectMultiple(choices=self.choices, attrs={"class": "year-based"}),
        	forms.NumberInput(attrs={"class": "year-based", "placeholder": _("Size")}),
            forms.TextInput(attrs={"class": "year-based-year"})
        ]