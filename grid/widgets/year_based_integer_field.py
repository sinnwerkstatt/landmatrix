__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django.utils.translation import ugettext_lazy as _

from grid.widgets.year_based_text_input import YearBasedTextInput

from django import forms


class YearBasedIntegerField(forms.MultiValueField):

    def __init__(self, *args, **kwargs):
        kwargs["fields"] = [
            forms.IntegerField(required=False),
            forms.CharField(required=False),
            forms.BooleanField(required=False)
        ]
        if 'placeholder' in kwargs:
            attrs = {'placeholder': kwargs.pop('placeholder', None)}
        else:
            attrs = {}
        kwargs["widget"] = YearBasedTextInput(help_text=kwargs.pop("help_text", ""), attrs=attrs)
        super(YearBasedIntegerField, self).__init__(*args, **kwargs)

    def clean(self, value):
        # update fields
        if value:
            self.fields = []
            for i in range(len(value)//3):
                self.fields.extend([
                    forms.IntegerField(required=False),
                    forms.CharField(required=False),
                    forms.BooleanField(required=False)
                ])
        return super(YearBasedIntegerField, self).clean(value)

    def compress(self, data_list):
        """  """
        if data_list:
            yb_data = []
            for i in range(len(data_list)//3):
                if data_list[i] or data_list[i+1]:
                    yb_data.append("%s:%s:%s" % (str(data_list[i]), str(data_list[i+1]), str(data_list[i+2])))
            return "#".join(yb_data)
        else:
            self.fields = [forms.IntegerField(required=False), forms.CharField(required=False)]