__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

import re
from django import forms

from grid.widgets.year_based_widget import YearBasedWidget

class YearBasedMultipleSelect(YearBasedWidget):
    def __init__(self, *args, **kwargs):
        self.choices = kwargs.pop("choices")
        # Remove empty option
        self.choices = filter(lambda c: c[0] != 0, self.choices)
        self.widget = forms.CheckboxSelectMultiple(choices=self.choices, attrs={"class": "year-based"})
        super(YearBasedMultipleSelect, self).__init__(*args, **kwargs)
