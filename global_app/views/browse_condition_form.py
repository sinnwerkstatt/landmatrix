__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django import forms
from django.utils.translation import ugettext_lazy as _

from landmatrix.models import BrowseCondition
from global_app.views.sql_generation.filter_to_sql import FilterToSQL
from global_app.views.base_model_form import BaseModelForm
from global_app.views.browse_text_input import BrowseTextInput
from global_app.views.browse_filter_conditions import BrowseFilterConditions, get_field_by_key, a_keys

class BrowseConditionForm(BaseModelForm):
    variable = forms.ChoiceField(required=False, label=_("Variable"), initial="", choices=())
    operator = forms.ChoiceField(required=False, label=_("Operator"), initial="", choices=(), widget=forms.Select(attrs={"class": "operator"}))
    value = forms.CharField(required=False, label=_("Value"), initial="", widget=BrowseTextInput())

    def __init__(self, variables_activity=None, variables_investor=None, *args, **kwargs):
        super(BrowseConditionForm, self).__init__(*args, **kwargs)
        variables = []
        variables.append(("", "-----"))
        variables.append(("-1", "ID"))
        variables.append(("-2", "Deal scope"))
        variables.append(("fully_updated", "Fully updated"))
        variables.append(("fully_updated_by", "Fully updated by"))
        variables.append(("last_modification", "Last modification"))
        variables.append(("inv_-2", "Primary investor"))
        # TODO: fix these! This form was very tied to the old key value storage system
        if variables_activity:
        #     self.a_fields = [(str(key.id), get_field_by_key(key.id)) for key in A_Key.objects.filter(fk_language=1, key__in=variables_activity)]#FIXME language
            self.a_fields = [(str(key), get_field_by_key(str(key))) for key in a_keys().values() if key in variables_activity]
        else:
        #     self.a_fields = [(unicode(key.id), get_field_by_a_key_id(key.id)) for key in A_Key.objects.filter(fk_language=1)]#FIXME language
            self.a_fields = [(str(key), get_field_by_key(str(key))) for key in a_keys()] #FIXME language
        if variables_investor:
        #     self.sh_fields = [("inv_%s" % key.id, get_field_by_sh_key_id(key.id)) for key in SH_Key.objects.filter(fk_language=1, key__in=variables_investor).exclude(key="name")]#FIXME language
            self.sh_fields = [(str(key), get_field_by_key(str(key))) for key in a_keys().values() if key in variables_investor]
        else:
        #     self.sh_fields = [("inv_%s" % key.id, get_field_by_sh_key_id(key.id)) for key in SH_Key.objects.filter(fk_language=1).exclude(key="name")]#FIXME language
            self.sh_fields = [(str(key), get_field_by_key(str(key))) for key in a_keys().values() if not key == 'name']
        variables.extend([(f[0], str(f[1].label)) for f in self.a_fields])
        variables.extend([(f[0], "Investor %s" % str(f[1].label)) for f in self.sh_fields])
        variables = sorted(variables, key=lambda x: x[1])
        self.fields["variable"].choices = variables
        operators = [("", "-----")]
        operators.extend([(op, op_name[2]) for op, op_name in FilterToSQL.OPERATION_MAP.items()])
        self.fields["operator"].choices = operators
        if BrowseFilterConditions.DEBUG:
            from pprint import pprint
            pprint(self.fields["variable"].choices)


    #def save(self, *args, **kwargs):
        #raise IOError, self.cleaned_data["value"]
        #c = super(BrowseConditionForm, self).save(commit=False)
        #if c.variable:
        #    try:
        #        f = dict(self.a_fields)[c.variable]
        #    except:
        #        try:
        #            f = dict(self.sh_fields)[c.variable]
        #        except:
        #            f = None
        #    # single value field?
        #    if f and not isinstance(f.widget, forms.SelectMultiple) and not c.operator in ("in", "not_in"):
        #        c.value = c.value[3:-2]
        #    # multiple value field saved by admin (e.g. [u'[1,2,3]'])?
        #    elif c.value.startswith("[u'["):
        #        c.value = c.value[3:-2]
        #    c.save()
    #    return c

    class Meta:
        model = BrowseCondition
        exclude = ('rule',)
