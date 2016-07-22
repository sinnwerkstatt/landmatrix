import re

from django import forms

from grid.widgets.year_based_widget import YearBasedWidget

class MultiCharField(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        kwargs["fields"] = [forms.CharField(required=False)]
        kwargs["widget"] = MultiTextInput(help_text=kwargs.pop("help_text", ""), attrs={})
        super(MultiCharField, self).__init__(*args, **kwargs)

    def clean(self, value):
        # update fields
        if value:
            self.fields = []
            for i in range(len(value)):
                self.fields.append(forms.CharField(required=False))
        return super(MultiCharField, self).clean(value)

    def compress(self, data_list):
        if data_list:
            data = []
            for i in range(len(data_list)):
                if data_list[i]:
                    yb_data.append(str(data_list[i]))
            return "#".join(data)
        else:
            self.fields = [forms.CharField(required=False)]

class MultiTextInput(YearBasedWidget):
    def get_widgets(self):
        return [
            forms.TextInput(),
        ]