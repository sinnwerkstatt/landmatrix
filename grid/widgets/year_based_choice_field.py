__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from grid.widgets.year_based_select import YearBasedSelect, YearBasedSelectMultiple, YearBasedSelectMultipleNumber
from grid.widgets.year_based_widget import YearBasedWidget
from grid.widgets.nested_multiple_choice_field import NestedMultipleChoiceField
from grid.widgets.nested_checkbox_select_multiple import NestedCheckboxSelectMultiple

from django import forms


class YearBasedChoiceField(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        self.choices = kwargs["choices"]
        kwargs["fields"] = [forms.ChoiceField(choices=kwargs["choices"], required=False), forms.CharField(required=False)]
        kwargs["widget"] = YearBasedSelect(choices=kwargs.pop("choices"), help_text=kwargs.pop("help_text", ""),attrs={})
        super(YearBasedChoiceField, self).__init__(*args, **kwargs)

    def clean(self, value):
        # update fields
        if value:
            self.fields = []
            for i in range(len(value)//3):
                self.fields.extend([
                    forms.ChoiceField(choices=self.choices, required=False),
                    forms.CharField(required=False),
                    forms.BooleanField(required=False)
                ])
        return super(YearBasedChoiceField, self).clean(value)

    def compress(self, data_list):
        if data_list:
            yb_data = []
            for i in range(len(data_list)//3):
                if data_list[i] or data_list[i+1]:
                    yb_data.append("%s:%s:%s" % (str(data_list[i]), str(data_list[i+1]), str(data_list[i+2])))
            return "#".join(yb_data)
        else:
            self.fields = [
                forms.ChoiceField(choices=self.choices, required=False),
                forms.CharField(required=False),
                forms.BooleanField(required=False)
            ]


class YearBasedModelMultipleChoiceField(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        self.queryset = kwargs.pop("queryset")
        kwargs["fields"] = [forms.ModelMultipleChoiceField(queryset=self.queryset, required=False), forms.CharField(required=False)]
        kwargs["widget"] = YearBasedSelectMultiple(choices=kwargs['fields'][0].choices, help_text=kwargs.pop("help_text", ""),attrs={})
        super(YearBasedModelMultipleChoiceField, self).__init__(*args, **kwargs)

    def clean(self, value):
        # update fields
        if value:
            self.fields = []
            for i in range(len(value)//3):
                self.fields.extend([
                    forms.ModelMultipleChoiceField(queryset=self.queryset, required=False),
                    forms.CharField(required=False),
                    forms.BooleanField(required=False)
                ])
        return super(YearBasedModelMultipleChoiceField, self).clean(value)

    def compress(self, data_list):
        if data_list:
            yb_data = []
            for i in range(len(data_list)//3):
                if data_list[i] or data_list[i+1]:
                    yb_data.append("%s:%s" % (str(data_list[i]), str(data_list[i+1]), str(data_list[i+2])))
            return "#".join(yb_data)
        else:
            self.fields = [
                forms.ModelMultipleChoiceField(queryset=self.queryset, required=False),
                forms.CharField(required=False),
                forms.BooleanField(required=False)
            ]


class YearBasedModelMultipleChoiceIntegerField(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        self.queryset = kwargs.pop("queryset")
        kwargs["fields"] = [
            forms.ModelMultipleChoiceField(queryset=self.queryset, required=False),
            forms.IntegerField(required=False),
            forms.CharField(required=False),
            forms.BooleanField(required=False),
        ]
        kwargs["widget"] = YearBasedSelectMultipleNumber(
            choices=kwargs['fields'][0].choices,
            help_text=kwargs.pop("help_text", ""),
            attrs={}
        )
        super(YearBasedModelMultipleChoiceIntegerField, self).__init__(*args, **kwargs)

    def clean(self, value):
        # update fields
        if value:
            self.fields = []
            for i in range(len(value)//4):
                self.fields.extend([
                    forms.ModelMultipleChoiceField(queryset=self.queryset, required=False),
                    forms.IntegerField(required=False),
                    forms.CharField(required=False),
                    forms.BooleanField(required=False),
                ])
        return super(YearBasedModelMultipleChoiceIntegerField, self).clean(value)

    def compress(self, data_list):
        if data_list:
            yb_data = []
            for i in range(len(data_list)//4):
                if data_list[i] or data_list[i+1]:
                    yb_data.append("%s:%s:%s" % (str(data_list[i]), str(data_list[i+1]), str(data_list[i+2])))
            return "#".join(yb_data)
        else:
            self.fields = [
                forms.ModelMultipleChoiceField(queryset=self.queryset, required=False),
                forms.IntegerField(required=False),
                forms.CharField(required=False),
                forms.BooleanField(required=False),
            ]

class YearBasedMultipleChoiceIntegerField(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        self.choices = kwargs.pop("choices")
        kwargs["fields"] = [
            forms.MultipleChoiceField(choices=self.choices, required=False),
            forms.IntegerField(required=False),
            forms.CharField(required=False),
            forms.BooleanField(required=False),
        ]
        kwargs["widget"] = YearBasedSelectMultipleNumber(
            choices=self.choices,
            help_text=kwargs.pop("help_text", ""),
            attrs={}
        )
        super(YearBasedMultipleChoiceIntegerField, self).__init__(*args, **kwargs)

    def clean(self, value):
        # update fields
        if value:
            self.fields = []
            for i in range(len(value)//4):
                self.fields.extend([
                    forms.MultipleChoiceField(choices=self.choices, required=False),
                    forms.IntegerField(required=False),
                    forms.CharField(required=False),
                    forms.BooleanField(required=False),
                ])
        return super(YearBasedMultipleChoiceIntegerField, self).clean(value)

    def compress(self, data_list):
        if data_list:
            yb_data = []
            for i in range(len(data_list)//4):
                if data_list[i] or data_list[i+1]:
                    yb_data.append("%s:%s:%s" % (str(data_list[i]), str(data_list[i+1]), str(data_list[i+2])))
            return "#".join(yb_data)
        else:
            self.fields = [
                forms.MultipleChoiceField(choices=self.choices, required=False),
                forms.IntegerField(required=False),
                forms.CharField(required=False),
                forms.BooleanField(required=False),
            ]