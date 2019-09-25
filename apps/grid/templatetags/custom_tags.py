import datetime
import time
from collections import OrderedDict
from uuid import uuid4

from django import forms, template
from django.contrib.humanize.templatetags.humanize import intcomma, naturaltime
from django.forms.fields import BooleanField, ChoiceField, MultiValueField
from django.template.defaultfilters import title
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

# from apps.editor.views import get_display_value_by_field
from apps.grid.fields import NestedMultipleChoiceField
from apps.grid.utils import has_perm_approve_reject

register = template.Library()


@register.filter(name="ensure_list")
def ensure_list(value):
    if isinstance(value, (list, tuple)):
        return value
    else:
        return [value]


@register.filter(name="fields_display")
def get_fields_display(form, user):
    if hasattr(form, "get_fields_display"):
        return form.get_fields_display(user=user)
    else:
        return ""


@register.filter(name="display_values")
def get_display_values(values, field):
    result = []
    for v in values:
        if "|" in v:
            for ybd in v.split("|"):
                result.append(
                    "%s%s"
                    % (
                        ybd.split(":")[1] and "[%s]" % ybd.split(":")[1] or "",
                        get_display_value_by_field(field, ybd.split(":")[0]),
                    )
                )
        elif ":" in v:
            result.append(
                "%s%s"
                % (
                    v.split(":")[1] and "[%s] " % v.split(":")[1] or "",
                    get_display_value_by_field(field, v.split(":")[0]),
                )
            )
        else:
            result.append(get_display_value_by_field(field, v))
    return result


def get_display_value_by_field(field, value):
    choices_dict = {}
    if isinstance(field, MultiValueField):
        field = field.fields[0]
    if isinstance(field, ChoiceField):
        if isinstance(field, NestedMultipleChoiceField):
            for k, v, c in field.choices:
                if isinstance(c, (list, tuple)):
                    # This is an optgroup, so look inside the group for options
                    for k2, v2 in c:
                        choices_dict.update({k2: v2})
                choices_dict.update({k: v})
        else:
            choices_dict = dict(field.choices)

        # get displayed value/s?
        dvalue = None
        if isinstance(value, (list, tuple)):
            dvalue = []
            for v in value:
                dvalue.append(get_value_from_choices_dict(choices_dict, v))
        else:
            dvalue = value and get_value_from_choices_dict(choices_dict, value)
        return dvalue
    if isinstance(field, BooleanField):
        dvalue = value == "on" and "True" or value == "off" and "False" or None
        return dvalue or value
    return value


def get_value_from_choices_dict(choices_dict, value):

    if str(value).isdigit():
        int_value = int(value)
        if int_value in choices_dict:
            return str(choices_dict.get(int_value))

    if value in choices_dict:
        return value

    return


@register.filter
def naturaltime_from_string(value):
    if not value:
        return ""
    time_format = "%Y-%m-%d %H:%M:%S"
    date = datetime.datetime.fromtimestamp(
        time.mktime(time.strptime(value, time_format))
    )
    natural_time = naturaltime(date)
    natural_time = natural_time.split(",")
    if len(natural_time) == 1:
        return natural_time[0]
    else:
        return "%s ago" % natural_time[0]


@register.simple_tag
def add_or_update_param(GET, new_param, new_value):
    params = GET.copy()
    params[new_param] = new_value
    return params.urlencode()


@register.filter
def add_class(field, new_cls):
    # return mark_safe(re.sub(r'(<(select|input|textarea).*?class=\")', '\1%s ' % new_cls, str(field)))
    # cls = field.field.widget.attrs.get('class', '')
    # cls += ' ' + new_cls
    if isinstance(
        field.field.widget,
        (forms.CheckboxInput, forms.RadioSelect, forms.CheckboxSelectMultiple),
    ):
        return field
    # elif isinstance(field.field.widget, forms.MultiValueWidget):
    #    attrs = field.field.widget.get_widgets()
    else:
        # MultiValueWidget?
        attrs = field.field.widget.attrs
        if "class" in attrs:
            attrs["class"] += " %s" % new_cls
        else:
            attrs["class"] = new_cls
        return mark_safe(field.as_widget())


@register.filter
def decimalgroupstring(obj):
    try:
        origs = obj.split(" ")
        val = int(origs.pop(0))
        new = intcomma(val)

        return str(new + " " + " ".join(origs))
    except ValueError:
        return obj


@register.filter
def random_id(obj):
    """Overwrite bound form field with random ID (workaround for location/map)"""
    return obj.as_widget(attrs={"id": obj.auto_id + ("_%i" % uuid4())})


@register.simple_tag
def get_user_role(user):
    output = []
    roles = OrderedDict()
    roles["Administrators"] = _("Administrator")
    roles["Editors"] = _("Editor")
    roles["Reporters"] = _("Reporter")
    groups = [g.name for g in user.groups.all()]
    for role, name in roles.items():
        if role in groups:
            output.append(str(name))
    if not output:
        output.append(str(_("No role")))
    userregionalinfo = None
    try:
        userregionalinfo = user.userregionalinfo
    except:
        pass
    if userregionalinfo:
        area = [c.name for c in user.userregionalinfo.country.all()]
        area.extend([r.name for r in user.userregionalinfo.region.all()])
        if area:
            output.append(str(_("for")))
            output.append(", ".join(area))
    return " ".join(output)


@register.filter
def history(item, user):
    return hasattr(item, "get_history") and item.get_history(user) or []


@register.filter
def history_count(item, user):
    return hasattr(item, "get_history") and len(item.get_history(user)) or 0


@register.filter
def is_editable(object, user):
    return object.is_editable(user)


@register.filter
def get_latest(object, user):
    return object.get_latest(user)


@register.filter
def deslugify(slug):
    return title(slug.replace("_", " ").replace("-", " "))


@register.filter
def can_approve_reject(user, object=None):
    return has_perm_approve_reject(user, object)


@register.filter()
def field_label(model, field_name):
    return model._meta.get_field(field_name).verbose_name
