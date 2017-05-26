from django import forms
from django.db.models.fields import IntegerField
from django.utils.translation import ugettext_lazy as _

from grid.fields import NestedMultipleChoiceField
from grid.views.change_deal_view import ChangeDealView
from grid.forms.investor_form import OperationalCompanyForm, ParentInvestorForm, ParentStakeholderForm


class BrowseFilterConditions:
    DEBUG = False

    def __init__(self, formset, order_by=None, limit=None):
        if self.DEBUG:
            from pprint import pprint
            pprint(formset.data, width=100, compact=True)
            pprint('valid' if formset.is_valid() else 'invalid')
        self.formset = formset
        self.order_by = order_by
        self.limit = limit

    def parse(self):
        self.data = {
            "activity": {},
            "deal_scope": "",
            "investor": {},
            "order_by": [],
            "limit": "",
        }

        if self.formset:
            self.read_formset()
        self.set_order_by()
        self.set_limit()

        return self.data

    def read_formset(self):
        self.filters_act, self.filters_inv = {"tags": {}}, {"tags": {}}
        if not self.formset:
            self.data["activity"] = self.filters_act
            self.data["investor"] = self.filters_inv
            return

        self.read_forms()

        self.data["activity"] = self.filters_act
        self.data["investor"] = self.filters_inv

    def read_forms(self):
        for i, form in self.get_forms():
            self.read_form(form, i)

    def get_forms(self):
        return enumerate(self.formset)

    def read_form(self, form, i):
        fl, value = self.get_fl(form, i)
        variable = fl.get("variable")
        # skip if no variable is selected
        if variable:
            self.read_form_variable(fl, fl.get("operator"), value, fl.get("value"), variable, fl.get("year"))

    def read_form_variable(self, fl, op, value, values, variable, year):
        # variable is identifier
        if variable == "-1":
            identifier_filter = self.filters_act.get("identifier", [])
            identifier_filter.append({
                "value": values[0] or "0",
                "op": op,
            })
            self.filters_act["identifier"] = identifier_filter
        elif variable == "-2":
            # deal scope
            if len(values) == 2:
                self.data["deal_scope"] = "all"
            elif len(values) == 1:
                self.data["deal_scope"] = "domestic" if values[0] == "10" else "transnational" if values[0] == "20" else ""
        elif "inv_" in variable:
            variable = variable[4:]
            f = get_field_by_sh_key_id(variable)
            values = [
                year and "%s##!##%s" % (get_display_value_by_field(f, value), year) or get_display_value_by_field(f,
                                                                                                                  value)
                for value in values]
            if f and "Region" in f.label:
                # region values not stored at activity/investor
                variable = "region"
            elif f and "Country" in f.label:
                # countries are referred by keys
                values = fl.get("value")
            self.filters_inv["tags"].update({"%s%s" % (variable, op and "__%s" % op or op): values})
        else:
            f = get_field_by_key(variable)
            if year:
                values = ["%s##!##%s" % (get_display_value_by_field(f, value), year)]
            else:
                values = [get_display_value_by_field(f, value) for value in values]
            if f:
                if "Region" in f.label:
                    # region values not stored at activity/investor
                    variable = "region"
                elif "Country" in f.label or "Crops" in f.label:
                    # countries and crops are referred by keys
                    values = fl.get("value")
                elif "Negotiation status" in f.label:
                    variable = "negotiation_status"
            self.filters_act["tags"].update({"%s%s" % (variable, op and "__%s" % op or op): values})

    def get_fl(self, form, i):
        fl = {}
        for j, (n, f) in enumerate(form.fields.items()):
            key = "%s-%d-%s" % (self.formset.prefix, i, n)
            if n == "value":
                # is ybd field?
                if "%s_0" % key in self.formset.data:
                    # just take the first row of the field
                    value = self.formset.data.getlist("%s_0" % key)
                    year = self.formset.data.get("%s_1" % key)
                    fl.update({n: value, "year": year})
                else:
                    value = self.formset.data.getlist(key)
                    fl.update({n: value})
            else:
                value = self.formset.data.get(key)
                fl.update({n: value})
        return fl, value

    def set_order_by(self):
        if not self.order_by: return
        if not isinstance(self.order_by, list): self.order_by = [self.order_by]
        for field in self.order_by:
            field_pre = ""
            field_GET = ""
            if len(field) > 0 and field[0] == "-":
                field_pre = "-"
                field = field[1:]

            form = get_field_by_key(field[9:] if "Investor " in field else field)
            if isinstance(form, IntegerField):
                field_GET = "+0"

            self.data["order_by"].append("%s%s%s" % (field_pre, field, field_GET))

    def set_limit(self):
        if self.limit:
            self.data["limit"] = self.limit


def get_field_by_key(key):
    if key.isnumeric():
        key = get_key_from_id(int(key))
    # Deal fields
    for form in ChangeDealView.FORMS:
        form = hasattr(form, "form") and form.form or form
        if key in form.base_fields:
            return form().fields[key]
    # Operational company fields
    investor_forms = {
        'operational_company_': OperationalCompanyForm,
        'parent_stakeholder_': ParentStakeholderForm,
        'parent_investor_': ParentInvestorForm,
    }
    for prefix, form in investor_forms.items():
        if prefix in key:
            k = key.replace(prefix, '')
            if k in form.base_fields:
                return form().fields[k]
    return None


def get_field_label(key):
    CUSTOM_FIELDS = {
        'activity_identifier': _('Deal ID')
    }
    if key in CUSTOM_FIELDS.keys():
        return str(CUSTOM_FIELDS[key])
    field = get_field_by_key(key)
    if field:
        investor_labels = {
            'operational_company_': _('Operational company'),
            'parent_stakeholder_': _('Parent company'),
            'parent_investor_': _('Tertiary investor/lender'),
        }
        for prefix, label in investor_labels.items():
            if prefix in key:
                return '%s %s' % (str(label), str(field.label))
        return str(field.label)
    return None


def get_display_value_by_field(field, value):
    choices_dict = {}
    if isinstance(field, forms.MultiValueField):
        field = field.fields[0]
    if isinstance(field, forms.ChoiceField):
        if isinstance(field, NestedMultipleChoiceField):
            for k, v, c in field.choices:
                if isinstance(c, (list, tuple)):
                    # This is an optgroup, so look inside the group for options
                    for k2, v2 in c:
                        choices_dict.update({k2:v2})
                choices_dict.update({k:v})
        else:
            choices_dict = dict(field.choices)
        # get displayed value/s?
        dvalue = None
        if isinstance(value, (list, tuple)):
            dvalue = []
            for v in value:
                dvalue.append(str(choices_dict.get(int(value))))
        else:
            dvalue = value and str(choices_dict.get(int(value)))
        return dvalue
    if isinstance(field, forms.BooleanField):
        dvalue = value == "on" and "True" or value == "off" and "False" or None
        return dvalue or value
    return value
