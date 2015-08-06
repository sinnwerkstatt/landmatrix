from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import View
from django.forms import TextInput, CheckboxSelectMultiple

class AjaxView(View):
    def dispatch(self, request, *args, **kwargs):
        action = kwargs.get("action", "values")
        if action == "values":
            return self.render_widget_values(request)
        elif action == "operators":
            return self.render_widget_operators(request)

    def render_widget_operators(self, request):
        key_id = request.GET.get("key_id", "")
        value = request.GET.get("value", "")
        name = request.GET.get("name", "")
        widget = None
        if key_id == "inv_-2":
            form = DealPrimaryInvestorForm()
            field = form.fields["primary_investor"]
        elif "inv_" in key_id:
            field = get_field_by_sh_key_id(key_id[4:])
        else:
            field = get_field_by_a_key_id(key_id)
        if field or key_id in("-1", "fully_updated", "fully_updated_by", "last_modification"):
            operator = BrowseConditionForm().fields.get("operator")
            choices = operator.choices
            new_choices = []
            if key_id in ("-1", "-3") or type(field.widget) == NumberInput:
                for c in choices:
                    if c[0] in ("", "lt", "gt", "gte", "lte", "is", "is_empty"):
                        new_choices.append(c)
            else:
                for c in choices:
                    if c[0] in ("", "not_in", "in", "is", "contains", "is_empty"):
                        new_choices.append(c)
            operator.choices = new_choices
            widget = operator.widget.render(name, value)
        return HttpResponse(widget, mimetype="text/plain")



    def render_widget_values(self, request):
        """FIXME: Cleanup this method"""
        value = request.GET.get("value", "")
        key_id = request.GET.get("key_id", "")
        operation = request.GET.get("operation", "")
        widget = None
        field = None
        value = value and value.split(",") or []
        widget = TextInput().render(request.GET.get("name", ""), ",".join(value))
        if key_id == "-1" and operation in ("in", "not_in"):
            widget = TextInput().render(request.GET.get("name", ""), ",".join(value))
        elif key_id == "-1" and operation not in ("in", "not_in"):
            widget = NumberInput().render(request.GET.get("name", ""), ",".join(value))
        elif key_id == "-2":
            widget = CheckboxSelectMultiple()
            widget.choices = (
                (10, "Domestic"),
                (20, "Transnational")
            )
            widget = widget.render(request.GET.get("name", ""), value)
        elif key_id == "fully_updated" or key_id == "last_modification":
            value = len(value) > 0 and value[0] or ""
            if value:
                try:
                    value = datetime.strptime(value, "%Y-%m-%d")
                except:
                    value = ""
            widget = DateWidget(options={"format": "yyyy-mm-dd"}).render(request.GET.get("name", ""), value=value, attrs={"id": "id_%s"%request.GET.get("name", "")})
        elif key_id == "fully_updated_by":
            users = User.objects.filter(groups__name__in=("Research admins", "Research assistants")).order_by("username")
            if operation in ("in", "not_in"):
                widget = SelectMultiple(choices=[(u.id, u.get_full_name() or u.username) for u in users]).render(request.GET.get("name", ""),  value, attrs={"id": "id_%s"%request.GET.get("name", "")})
            else:
                widget = Select(choices=[(u.id, u.get_full_name() or u.username) for u in users]).render(request.GET.get("name", ""),  len(value) == 1 and value[0] or value, attrs={"id": "id_%s"%request.GET.get("name", "")})
        elif key_id == "inv_-2":
            form = DealPrimaryInvestorForm()
            field = form.fields["primary_investor"]
        elif key_id == "secondary_investor":
            form = DealSecondaryInvestorForm()
            field = form.fields["investor"]
        elif "inv_" in key_id:
            field = get_field_by_sh_key_id(key_id[4:])
        else:
            field = get_field_by_a_key_id(key_id)
        if field:
            widget = field.widget
            if widget.attrs.get("readonly", ""):
                del widget.attrs["readonly"]
            if type(widget) == HiddenInput:
                field.widget = Select(choices=field.choices)
                widget = Select(choices=field.choices)
            if type(widget) == LocationWidget:
                field.widget = TextInput()
                widget = field.widget.render(request.GET.get("name", ""), len(value) > 0 and value[0] or "")
            elif operation in ("in", "not_in"):
                if type(widget) == YearBasedSelect:
                    field.widget = YearBasedMultipleSelect(choices=field.widget.choices)
                    # FIXME: multiple value parameters can arrive like "value=1&value=2" or "value=1,2", not very nice
                    value = type(value) in (list, tuple) and value or request.GET.getlist("value", [])
                    value = [value, ""]
                    widget = field.widget.render(request.GET.get("name", ""), value, attrs={"id": "id_%s"%request.GET.get("name", "")})
                elif type(widget) == RadioSelect:
                    widget = CheckboxSelectMultiple()
                    widget.choices = field.widget.choices
                    widget = widget.render(request.GET.get("name", ""), value)
                elif issubclass(type(field.widget), (CheckboxSelectMultiple, SelectMultiple)):
                    widget = widget.render(request.GET.get("name", ""), value)
                elif isinstance(widget, Select):
                    widget = SelectMultiple()
                    choices = field.widget.choices
                    widget.choices = field.widget.choices
                    widget = widget.render(request.GET.get("name", ""), value)
                else:
                    widget = widget.render(request.GET.get("name", ""), ",".join(value), attrs={"id": "id_%s"%request.GET.get("name", "")})
            elif operation in ("contains",):
                widget = TextInput().render(request.GET.get("name", ""), ",".join(value))
            else:
                if issubclass(type(field.widget), (CheckboxSelectMultiple, SelectMultiple)):
                    widget = widget.render(request.GET.get("name", ""), value)
                else:
                    widget = widget.render(request.GET.get("name", ""),  ",".join(value), attrs={"id": "id_%s"%request.GET.get("name", "")})
        return HttpResponse(widget, content_type="text/plain")
