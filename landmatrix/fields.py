from django import forms

class CommaSeparatedCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    def value_from_datadict(self, *args, **kwargs):
        data_list = super(CommaSeparatedCheckboxSelectMultiple, self).value_from_datadict(*args, **kwargs)
        return ','.join(data_list)