__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from global_app.widgets.year_based_select import YearBasedSelect

from django import forms


class YearBasedChoiceField(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        self.choices = kwargs["choices"]
        kwargs["fields"] = [forms.ChoiceField(choices=kwargs["choices"], required=False), forms.CharField(required=False)]
        kwargs["widget"] = YearBasedSelect(choices=kwargs.pop("choices"),help_text=kwargs.pop("help_text", ""))
        super(YearBasedChoiceField, self).__init__(*args, **kwargs)

    def clean(self, value):
        # update fields
        if value:
            self.fields = []
            for i in range(len(value)/2):
                self.fields.extend([forms.ChoiceField(choices=self.choices, required=False), forms.CharField(required=False)])
        return super(YearBasedChoiceField, self).clean(value)

    def compress(self, data_list):
        if data_list:
            yb_data = []
            for i in range(len(data_list)/2):
                if data_list[i] or data_list[i+1]:
                    yb_data.append("%s:%s" % (str(data_list[i]), str(data_list[i+1])))
            return "|".join(yb_data)
        else:
            self.fields = [forms.ChoiceField(choices=self.choices, required=False), forms.CharField(required=False)]

    # def prepare_value(self, value):
    #     raise IOError, "ok"
