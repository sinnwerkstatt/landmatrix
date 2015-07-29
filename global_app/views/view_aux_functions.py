__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from global_app.views.browse_condition_form import BrowseConditionForm

from django.template import loader
from django.http import HttpResponse

def parse_browse_filter_conditions(formset, order_by=None, limit=None):
    data = {
        "activity": {},
        "deal_scope": "",
        "investor": {},
        "order_by": [],
        "limit": "",
    }
    filters_act, filters_inv = {"tags":{}}, {"tags":{}}
    if formset:
        for i, form in enumerate(formset):
            fl = {}
            for j, (n, f) in enumerate(form.fields.items()):
                key = "%s-%d-%s"%(formset.prefix, i, n)
                if n == "value":
                    # is ybd field?
                    if "%s_0" % key in formset.data:
                        # just take the first row of the field
                        value = formset.data.getlist("%s_0"%key)
                        year = formset.data.get("%s_1"%key)
                        fl.update({n:value, "year":year})
                    else:
                        value = formset.data.getlist(key)
                        fl.update({n:value})
                else:
                    value = formset.data.get(key)
                    fl.update({n:value})
            variable = fl.get("variable")
            op = fl.get("operator")
            values = fl.get("value")
            year = fl.get("year")
            #skip if no variable is selected
            if not variable:
                continue
            # variable is identifier
            if variable == "-1":
                identifier_filter = filters_act.get("identifier", [])
                identifier_filter.append({
                    "value": values[0] or "0",
                    "op": op,
                })
                filters_act["identifier"] = identifier_filter
            elif variable == "-2":
                # deal scope
                if len(values) == 2:
                    data["deal_scope"] = "all"
                elif len(values) == 1:
                    data["deal_scope"] = values[0] == "10" and "domestic" or values[0] == "20" and "transnational" or ""
            elif "inv_" in variable:
                variable = variable[4:]
                f = get_field_by_sh_key_id(variable)
                values = [year and "%s##!##%s" % (get_display_value_by_field(f, value), year) or get_display_value_by_field(f, value) for value in values]
                if f and "Region" in f.label:
                    # region values not stored at activity/investor
                    variable = "region"
                elif f and "Country" in f.label:
                    # countries are referred by keys
                    values = fl.get("value")
                filters_inv["tags"].update({"%s%s" % (variable, op and "__%s" % op or op): values})
            else:
                f = get_field_by_a_key_id(variable)
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
                        variable = "pi_negotiation_status"
                filters_act["tags"].update({"%s%s" % (variable, op and "__%s" % op or op): values})
        data["activity"] = filters_act
        data["investor"] = filters_inv
    if order_by:
        for field in order_by:
            field_pre = ""
            field_GET = ""
            if len(field) > 0 and field[0] == "-":
                field_pre = "-"
                field = field[1:]
            try:
                if "Investor " in field:
                    form = get_field_by_sh_key_id(SH_Key.objects.get(key=field[9:]).id)
                else:
                    form = get_field_by_a_key_id(A_Key.objects.get(key=field).id)
                if isinstance(form, IntegerField):
                    field_GET = "+0"
            except:
                pass
            data["order_by"].append("%s%s%s" % (field_pre, field, field_GET))
    if limit:
        data["limit"] = limit
    return data


def get_field_by_a_key_id(key_id):
    return None

    field = None
    try:
        k = ActivityAttributeGroup.objects.filter(pk=int(key_id))
    except:
        k = ActivityAttributeGroup.objects.filter(key=key_id)
    if k.count() > 0:
        k = k[0].key
    else:
        k = key_id
    forms = CHANGE_FORMS
    forms.append(('primary_investor', DealPrimaryInvestorForm))
    for i, form in forms:
        form = hasattr(form, "form") and form.form or form
        if form.base_fields.has_key(k):
            field = form().fields[k]
            break
    return field

def get_display_value_by_field(field, value):
    return None
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
                dvalue.append(unicode(choices_dict.get(int(value))))
        else:
            dvalue = value and unicode(choices_dict.get(int(value)))
        return dvalue
    if isinstance(field, forms.BooleanField):
        dvalue = value == "on" and "True" or value == "off" and "False" or None
        return dvalue or value
    return value

FILTER_VAR_ACT = ["target_country", "location", "intention", "intended_size", "contract_size", "production_size", "negotiation_status", "implementation_status", "crops", "nature", "contract_farming", "url", "type", "company", "type"]
FILTER_VAR_INV = ["investor_name", "country"]
def create_condition_formset():
    from django.forms.formsets import formset_factory
    from django.utils.functional import curry

    ConditionFormset = formset_factory(BrowseConditionForm, extra=0)
    ConditionFormset.form = staticmethod(
        curry(BrowseConditionForm, variables_activity=FILTER_VAR_ACT, variables_investor=FILTER_VAR_INV)
    )
    return ConditionFormset

""" Returns a HttpResponse whose content is filled with the result of calling
    django.template.loader.render_to_string() with the passed arguments."""
def render_to_response(template_name, context, context_instance):
    # Some deprecated arguments were passed - use the legacy code path
    content = loader.render_to_string(template_name, context, context_instance)

    return HttpResponse(content)

