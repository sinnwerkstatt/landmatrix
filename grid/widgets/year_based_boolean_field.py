__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from grid.widgets.year_based_checkbox_input import YearBasedCheckboxInput

from django import forms


class YearBasedBooleanField(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        kwargs["fields"] = [forms.BooleanField(required=False), forms.CharField(required=False)]
        kwargs["widget"] = YearBasedCheckboxInput(help_text=kwargs.pop("help_text", ""))
        super(YearBasedBooleanField, self).__init__(*args, **kwargs)

    def clean(self, value):
        # update fields
        if value:
            self.fields = []
            for i in range(len(value)/3):
                self.fields.extend([
                    forms.BooleanField(required=False),
                    forms.CharField(required=False),
                    forms.BooleanField(required=False)
                ])
        return super(YearBasedBooleanField, self).clean(value)

    def compress(self, data_list):
        if data_list:
            yb_data = []
            for i in range(len(data_list)/3):
                if data_list[i] or data_list[i+1]:
                    yb_data.append("%s:%s" % (str(data_list[i]), str(data_list[i+1]), str(data_list[i+2])))
            return "#".join(yb_data)
        else:
            self.fields = [
                forms.IntegerField(required=False),
                forms.CharField(required=False),
                forms.BooleanField(required=False)
            ]
