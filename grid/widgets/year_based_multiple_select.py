__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from grid.widgets.year_based_widget import YearBasedWidget

from django import forms
import re


class YearBasedMultipleSelect(YearBasedWidget):

    def __init__(self, *args, **kwargs):
        self.choices = kwargs.pop("choices")
        # Remove empty option
        self.choices = filter(lambda c: c[0] != 0, self.choices)
        self.help_text = kwargs.pop("help_text", "")
        kwargs["widgets"] = self.get_widgets()
        super(YearBasedMultipleSelect, self).__init__(*args, **kwargs)

    def get_widgets(self):
        return [
            forms.CheckboxSelectMultiple(choices=self.choices, attrs={"class": "year-based"}),
            forms.TextInput(attrs={"class": "year-based-year"})
        ]

    def decompress(self, value):
        if value:
            splitted = re.split("[:\|]", value)
            return len(splitted) == 1 and splitted.append(None) or splitted
        return [None, None]

    def format_output(self, rendered_widgets):
        return u''.join(rendered_widgets)

    def value_from_datadict(self, data, files, name):
        #return [widget.value_from_datadict(data, files, name + '_%s' % i) for i, widget in enumerate(self.widgets)]
        value = [data[k] for k in sorted(filter(lambda o: re.match(r"%s_\d+"%name,o), data))]
        return value
