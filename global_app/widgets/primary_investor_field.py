__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from global_app.widgets.primary_investor_select import PrimaryInvestorSelect

from django import forms


class PrimaryInvestorField(forms.ChoiceField):
    widget = PrimaryInvestorSelect
    # TODO: fix
    #queryset = PrimaryInvestor.objects._get_all_active_primary_investors_choices
    queryset = lambda x: []

    def __init__(self, *args, **kwargs):
        kwargs["choices"] = self.get_choices()
        super(PrimaryInvestorField, self).__init__(*args, **kwargs)

    def validate(self, value):
        pass
        #super(ChoiceField, self).validate(value)
        #if value and not self.valid_value(value):
        #    raise ValidationError(self.error_messages['invalid_choice'] % {'value': value})

    def get_choices(self):
        #PrimaryInvestor.objects.update()
        return self.queryset()
