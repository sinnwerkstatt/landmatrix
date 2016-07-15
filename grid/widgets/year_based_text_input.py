__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

import re
from django import forms
from django.utils.translation import ugettext_lazy as _

from grid.widgets.year_based_widget import YearBasedWidget

class YearBasedTextInput(YearBasedWidget):
    widget = forms.NumberInput(attrs={"class": "year-based", "placeholder": _('Size')})

    def decompress(self, value):
        if value:
            values = value.split("#")

            sorted_values = sorted(values, key=lambda v: v.split(":")[1] if ':' in v else '0')
            splitted = []
            for s in sorted_values:
                splitted.extend(s.split(":"))
            return len(splitted) == 1 and splitted.append(None) or splitted
        return [None, None]