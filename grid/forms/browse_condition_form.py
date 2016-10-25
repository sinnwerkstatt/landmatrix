from django import forms
from django.forms.formsets import formset_factory
from django.utils.translation import ugettext_lazy as _

from landmatrix.models.browse_condition import BrowseCondition
from api.filters import FILTER_OPERATION_MAP, FILTER_VAR_ACT, FILTER_VAR_INV
from grid.forms.base_model_form import BaseModelForm
from grid.widgets import BrowseTextInput
from grid.views.browse_filter_conditions import get_field_by_key, a_keys


__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class BrowseConditionForm(BaseModelForm):

    variable = forms.ChoiceField(
        required=False, label=_("Variable"), initial="", choices=())
    operator = forms.ChoiceField(
        required=False, label=_("Operator"), initial="", choices=(),
        widget=forms.Select(attrs={"class": "operator"}))
    value = forms.CharField(
        required=False, label=_("Value"), initial="", widget=BrowseTextInput())

    # TODO: no idea whats going on here, but it can be simplified I think
    def __init__(self, variables_activity=None, variables_investor=None, *args, **kwargs):
        super(BrowseConditionForm, self).__init__(*args, **kwargs)

        if variables_activity is None:
            variables_activity = FILTER_VAR_ACT
        if variables_investor is None:
            variables_investor = FILTER_VAR_INV

        self._set_a_fields(variables_activity)
        self._set_sh_fields(variables_investor)

        self.fields["variable"].choices = self._variables()
        self.fields["operator"].choices = _operators()

    def _set_a_fields(self, variables_activity):
        if variables_activity:
            self.a_fields = [
                (str(key), get_field_by_key(str(key))) for key in a_keys().values() if key in variables_activity
            ]  # FIXME language
        else:
            self.a_fields = [(str(key), get_field_by_key(str(key))) for key in a_keys()]

    def _set_sh_fields(self, variables_investor):
        if variables_investor:
            self.sh_fields = [
                (str(key), get_field_by_key(str(key))) for key in a_keys().values() if key in variables_investor
            ]
        else:
            self.sh_fields = [(str(key), get_field_by_key(str(key))) for key in a_keys().values() if not key == 'name']

    def _variables(self):
        variables = [("", "-----"),
                     ("-1", "ID"),
                     ("-2", "Deal scope"),
                     ("fully_updated", "Fully updated"),
                     ("fully_updated_by", "Fully updated by"),
                     ("last_modification", "Last modification"),
                     ("inv_-2", "Primary investor")]
        variables.extend([(f[0], str(f[1].label)) for f in self.a_fields if f[1]])
        variables.extend([(f[0], "Investor %s" % str(f[1].label)) for f in self.sh_fields if f[1]])
        variables = sorted(variables, key=lambda x: x[1])
        return variables

    class Meta:
        model = BrowseCondition
        exclude = ('rule',)


def _operators():
    operators = [("", "-----")]
    operators.extend([(op, op_name[2]) for op, op_name in FILTER_OPERATION_MAP.items()])
    return operators


ConditionFormset = formset_factory(BrowseConditionForm, extra=0)
