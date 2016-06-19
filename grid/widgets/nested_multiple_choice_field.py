__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from grid.widgets.nested_checkbox_select_multiple import NestedCheckboxSelectMultiple

from django import forms
from django.utils.encoding import smart_text


class NestedMultipleChoiceField(forms.MultipleChoiceField):

    widget = NestedCheckboxSelectMultiple

    def valid_value(self, value):
        "Check to see if the provided value is a valid choice"
        return value in self._valid_keys()

    def _valid_keys(self):
        values = []
        for k, v, sub_choices in self.choices:
            values.append(k)
            if isinstance(sub_choices, (list, tuple)):
                for k2, v2 in sub_choices:
                    values.append(k2)
        return values

    def get_value(self, key):
        for k, v, c in self.choices:
            if isinstance(v, (list, tuple)):
                # This is an optgroup, so look inside the group for options
                for k2, v2 in v:
                    if key == smart_text(k2):
                        return v2
            else:
                if key == smart_text(k):
                    return v
                elif c:
                    for k2, v2 in c:
                        if k == smart_text(k2):
                            return v2

