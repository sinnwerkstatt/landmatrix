__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from grid.widgets.number_input import NumberInput

from django import forms


class YearBasedCheckboxInput(forms.MultiWidget):
    def __init__(self, *args, **kwargs):
        self.help_text = kwargs.pop("help_text", "")
        kwargs["widgets"] = self.get_widgets()
        super(YearBasedCheckboxInput, self).__init__(*args, **kwargs)

    def get_widgets(self):
        return [
            forms.CheckboxInput(attrs={"class": "year-based"}),
            NumberInput(attrs={"class": "year-based-year"})
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
        # update widgets
        self.widgets = []
        for i in range(len(value)/2):
            self.widgets.extend([forms.CheckboxInput(attrs={"class": "year-based"}), NumberInput(attrs={"class": "year-based-year"})])
        return value
