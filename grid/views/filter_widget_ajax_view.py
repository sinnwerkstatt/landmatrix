__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from grid.views.browse_filter_conditions import get_field_by_key
from grid.widgets import LocationWidget, YearBasedSelect, YearBasedMultipleSelect, YearBasedTextInput, NumberInput
from grid.forms.choices import intention_choices, int_choice_to_string

from django.http import HttpResponse
from django.views.generic.edit import View
from django.forms import TextInput, CheckboxSelectMultiple, HiddenInput, SelectMultiple, RadioSelect, Select

from bootstrap3_datetime.widgets import DateTimePicker
import datetime

from django.contrib.auth.models import User


class FilterWidgetAjaxView(View):
    def dispatch(self, request, *args, **kwargs):
        """ render form to enter values for the requested field in the filter widget for the grid view
            form to select operations is updated by the javascript function update_widget() in /media/js/main.js
        """
        action = kwargs.get("action", "values")
        if action == "values":
            return self.render_widget_values(request)

    def render_widget_values(self, request):

        # TODO: Cleanup this hog of a method

        fc_attrs = {'class': 'valuefield form-control'}
        vf_attrs = {'class': 'valuefield'}

        value = request.GET.get("value", "")
        key_id = request.GET.get("key_id", "")
        operation = request.GET.get("operation", "")
        field = None
        value = value and value.split(",") or []
        widget = TextInput().render(request.GET.get("name", ""), ",".join(value), attrs=fc_attrs)

        #if operation == 'is_empty':
        #    return HttpResponse('', content_type="text/plain")
        # Deal ID
        if key_id == 'activity_identifier':
            if operation in ("in", "not_in"):
                widget = TextInput().render(request.GET.get("name", ""), ",".join(value), attrs=fc_attrs)
            else:
                widget = NumberInput().render(request.GET.get("name", ""), ",".join(value), attrs=fc_attrs)
        # deal scope
        #elif key_id == "-2":
        #    widget = CheckboxSelectMultiple()
        #    widget.choices = (
        #        (10, "Domestic"),
        #        (20, "Transnational")
        #    )
        #    widget = widget.render(request.GET.get("name", ""), value, attrs=vf_attrs)

        elif key_id == "fully_updated" or key_id == "last_modification":
            value = len(value) > 0 and value[0] or ""
            if value:
                try:
                    value = datetime.strptime(value, "%Y-%m-%d")
                except:
                    value = ""
            widgetObject = DateTimePicker(options={
                "format": "YYYY-MM-DD",
                "inline": True,
            })

            # See here: https://github.com/jorgenpt/django-bootstrap3-datetimepicker/commit/042dd1da3a7ff21010c1273c092cba108d95baeb#commitcomment-16877308
            widgetObject.js_template = """<script>
                    $(function(){$("#%(picker_id)s:has(input:not([readonly],[disabled]))").datetimepicker(%(options)s);});
            </script>"""
            widget = widgetObject.render(
                    request.GET.get("name", ""), value=value, attrs={"id": "id_%s" % request.GET.get("name", "")}
            )

        elif key_id == "fully_updated_by":
            users = User.objects.filter(groups__name__in=("Research admins", "Research assistants")).order_by(
                "username")
            if operation in ("in", "not_in"):
                widget = SelectMultiple(choices=[(u.id, u.get_full_name() or u.username) for u in users]).render(
                    request.GET.get("name", ""), value, attrs={"id": "id_%s" % request.GET.get("name", ""), "class": "form-control"})
            else:
                widget = Select(choices=[(u.id, u.get_full_name() or u.username) for u in users]).render(
                    request.GET.get("name", ""), len(value) == 1 and value[0] or value,
                    attrs={"id": "id_%s" % request.GET.get("name", "")})
        elif "inv_" in key_id:
            field = get_field_by_key(key_id[4:])
        else:
            field = get_field_by_key(key_id)

        if field:
            widget = field.widget
            if widget.attrs.get("readonly", ""):
                del widget.attrs["readonly"]
            if type(widget) == HiddenInput:
                field.widget = Select(choices=field.choices)
                widget = Select(choices=field.choices)
            if type(widget) == LocationWidget:
                field.widget = TextInput()
                widget = field.widget.render(request.GET.get("name", ""), len(value) > 0 and value[0] or "", attrs=fc_attrs)
            elif operation in ("in", "not_in"):
                if type(widget) == YearBasedSelect:
                    field.widget = YearBasedMultipleSelect(choices=field.widget.choices)
                    # FIXME: multiple value parameters can arrive like "value=1&value=2" or "value=1,2", not very nice
                    value = type(value) in (list, tuple) and value or request.GET.getlist("value", [])
                    value = [value, ""]
                    widget = field.widget.render(request.GET.get("name", ""), value,
                                                 attrs={"id": "id_%s" % request.GET.get("name", ""), "class": "form-control"})

                elif type(widget) == YearBasedTextInput:
                    widget = widget.render(request.GET.get("name", ""), ",".join(value),
                                           attrs={"id": "id_%s" % request.GET.get("name", ""), "class": "form-control"})
                elif type(widget) == RadioSelect:
                    widget = CheckboxSelectMultiple()
                    widget.choices = field.widget.choices
                    widget = widget.render(request.GET.get("name", ""), value)
                elif issubclass(type(field.widget), (CheckboxSelectMultiple, SelectMultiple)):
                    widget = widget.render(request.GET.get("name", ""), value)
                elif isinstance(widget, Select):
                    widget = SelectMultiple()
                    widget.choices = field.widget.choices
                    widget = widget.render(request.GET.get("name", ""), value)
                else:
                    widget = widget.render(request.GET.get("name", ""), ",".join(value),
                                           attrs={"id": "id_%s" % request.GET.get("name", ""), "class": "valuefield form-control"})
            elif operation in ("contains",):
                widget = TextInput().render(request.GET.get("name", ""), ",".join(value), attrs=fc_attrs)
            else:

                if issubclass(type(field.widget), (CheckboxSelectMultiple, SelectMultiple, RadioSelect)):
                    widget = widget.render(request.GET.get("name", ""), value)
                elif issubclass(type(field.widget), (YearBasedMultipleSelect, YearBasedSelect, YearBasedTextInput)):
                    widget = widget.render(request.GET.get("name", ""), ",".join(value),
                                           attrs={"id": "id_%s" % request.GET.get("name", ""), "class": "form-control"})
                else:
                    widget = widget.render(request.GET.get("name", ""), ",".join(value),
                                           attrs={"id": "id_%s" % request.GET.get("name", ""), "class": "valuefield form-control"})

            #print(type(field.widget))
        return HttpResponse(widget, content_type="text/plain")
