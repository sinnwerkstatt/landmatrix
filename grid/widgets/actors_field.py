__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

import re

from grid.widgets.year_based_text_input import YearBasedTextInput
from grid.widgets.year_based_widget import YearBasedWidget

from django import forms

class ActorsField(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        self.choices = kwargs["choices"]
        kwargs["fields"] = [forms.CharField(required=False), forms.ChoiceField(choices=kwargs["choices"], required=False)]
        kwargs["widget"] = TextChoiceInput(choices=kwargs.pop("choices"), help_text=kwargs.pop("help_text", ""), attrs={})
        super(ActorsField, self).__init__(*args, **kwargs)

    def clean(self, value):
        # update fields
        if value:
            self.fields = []
            for i in range(len(value)//2):
                self.fields.extend([forms.CharField(required=False), forms.ChoiceField(choices=self.choices, required=False)])
        return super(ActorsField, self).clean(value)

    def compress(self, data_list):
        if data_list:
            yb_data = []
            for i in range(len(data_list)//2):
                if data_list[i] or data_list[i+1]:
                    yb_data.append("%s:%s" % (str(data_list[i]), str(data_list[i+1])))
            return "#".join(yb_data)
        else:
            self.fields = [forms.CharField(required=False), forms.ChoiceField(choices=self.choices, required=False)]

class TextChoiceInput(YearBasedWidget):
    def __init__(self, *args, **kwargs):
        self.choices = kwargs.pop("choices")
        super(TextChoiceInput, self).__init__(*args, **kwargs)

    def get_widgets(self):
        return [
            forms.TextInput(),
            forms.Select(choices=self.choices)
        ]