__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from global_app.widgets.number_input import NumberInput
from global_app.widgets.year_based_widget import YearBasedWidget

import re


class YearBasedTextInput(YearBasedWidget):

    def __init__(self, *args, **kwargs):
        self.help_text = kwargs.pop("help_text", "")
        kwargs["widgets"] = self.get_widgets()
        super(YearBasedTextInput, self).__init__(*args, **kwargs)

    def get_widgets(self):
        return [
            NumberInput(attrs={"class": "year-based"}),
            NumberInput(attrs={"class": "year-based-year"})
        ]

    def decompress(self, value):
        if value:
            sorted_values = sorted(value.split("|"), key=lambda v: v.split(":")[1] and int(v.split(":")[1]) or 0)
            splitted = []
            for s in sorted_values:
                splitted.extend(s.split(":"))
            return len(splitted) == 1 and splitted.append(None) or splitted
        return [None, None]

    def format_output(self, rendered_widgets):
        return u''.join(rendered_widgets)

    def value_from_datadict(self, data, files, name):
        value = [data[k] for k in sorted(filter(lambda o: re.match(r"%s_\d+"%name,o), data))]

        # update widgets
        self.widgets = []
        for i in range(len(value)//2):
            self.widgets.extend([NumberInput(attrs={"class": "year-based"}), NumberInput(attrs={"class": "year-based-year"})])
        return value
