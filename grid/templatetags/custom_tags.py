import re
import time, datetime
from uuid import uuid4

from django import template
from django.forms.fields import MultiValueField, ChoiceField, BooleanField
from django.template import Node, resolve_variable, Variable
from django.template.defaultfilters import slugify, title, stringfilter
from django.contrib.humanize.templatetags.humanize import naturaltime, intcomma
from django.utils.safestring import mark_safe
from django import forms
from django.utils.translation import ugettext_lazy as _
from collections import OrderedDict


# from editor.views import get_display_value_by_field
from grid.fields import NestedMultipleChoiceField

register = template.Library()


@register.filter
def lookup(d, key):
    if key < len(d):
        return d[key]


@register.filter
@stringfilter
def slug_and_slash_to_plus(value):
    """
    Converts any slashes in the given value into spaces, then slugify's the result.
    Leading and Trailing slashes (e.g. /some/url/) are ignored.
    """
    return slugify('+'.join(value.split('/')))


@register.filter
def replaceUnderscores(value):
    return value.replace("_", " ")


@register.filter
def split(str,splitter):
    return str.split(splitter)


@register.filter(name='ensure_list')
def ensure_list(value):
    if isinstance(value, (list, tuple)):
        return value
    else:
        return [value,]


@register.filter(name='display_values')
def get_display_values(values, field):
    result = []
    for v in values:
        if "|" in v:
            for ybd in v.split("|"):
                result.append("%s%s" % (ybd.split(":")[1] and "[%s]" % ybd.split(":")[1] or "" , get_display_value_by_field(field, ybd.split(":")[0])))
        elif ":" in v:
            result.append("%s%s" % (v.split(":")[1] and "[%s] " % v.split(":")[1] or "" , get_display_value_by_field(field, v.split(":")[0])))
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
                        choices_dict.update({k2:v2})
                choices_dict.update({k:v})
        else:
            choices_dict = dict(field.choices)

        # get displayed value/s?
        dvalue = None
        if isinstance(value, (list, tuple)):
            dvalue = []
            for v in value:
                dvalue.append(get_value_from_i18nized_choices_dict(choices_dict, value))
        else:
            dvalue = value and get_value_from_i18nized_choices_dict(choices_dict, value)
        return dvalue
    if isinstance(field, BooleanField):
        dvalue = value == "on" and "True" or value == "off" and "False" or None
        return dvalue or value
    return value


def get_value_from_i18nized_choices_dict(choices_dict, value):
    try:
        if choices_dict.get(int(value)):
            return str(choices_dict.get(int(value)))
    except ValueError:
        pass

    if value in choices_dict.values():
        return value
    raise RuntimeError('Damn: %s not in %s' %(value, str(choices_dict)))


@register.filter
def get_range(value):
  """
    Filter - returns a list containing range made from given value
    Usage (in template):

    <ul>{% for i in 3|get_range %}
      <li>{{ i }}. Do something</li>
    {% endfor %}</ul>

    Results with the HTML:
    <ul>
      <li>0. Do something</li>
      <li>1. Do something</li>
      <li>2. Do something</li>
    </ul>

    Instead of 3 one may use the variable set in the views
  """
  return range(int(value))


@register.filter
def naturaltime_from_string(value):
    if not value:
        return ''
    time_format = "%Y-%m-%d %H:%M:%S"
    date = datetime.datetime.fromtimestamp(time.mktime(time.strptime(value, time_format)))
    natural_time = naturaltime(date)
    natural_time = natural_time.split(",")
    if len(natural_time) == 1:
        return natural_time[0]
    else:
        return "%s ago" % natural_time[0]


@register.filter
def timestamp_from_epoch(timestamp):
    try:
        #assume, that timestamp is given in seconds with decimal point
        ts = float(timestamp)
    except ValueError:
        return None
    return datetime.datetime.fromtimestamp(ts)



"""
This is custom tag I wrote for myself for solving situations when you have filter form and page
numbers in the same page. You want to change ?page=.. or add it if it doesn't exist to save
filter form data while moving through pages.

Usage: place this code in your application_dir/templatetags/add_get_parameter.py
In template:
{% load add_get_parameter %}
<a href="{% add_get_paramater param1='const_value',param2=variable_in_context %}">
    Link with modified params
</a>

It's required that you have 'django.core.context_processors.request' in TEMPLATE_CONTEXT_PROCESSORS

URL: http://django.mar.lt/2010/07/add-get-parameter-tag.html
"""


class AddGetParameter(Node):
    def __init__(self, values):
        self.values = values

    def render(self, context):
        req = resolve_variable('request',context)
        params = req.GET.copy()
        for key, value in self.values.items():
            params[key] = Variable(value).resolve(context)
        return '?%s' %  params.urlencode()


@register.tag
def add_get_parameter(parser, token):
    from re import split
    contents = split(r'\s+', token.contents, 2)[1]
    pairs = split(r',', contents)

    values = {}

    for pair in pairs:
        s = split(r'=', pair, 2)
        values[s[0]] = s[1]

    return AddGetParameter(values)


@register.simple_tag
def get_GET_params(GET):
    return GET.urlencode()


@register.simple_tag
def add_or_update_param(GET, new_param, new_value):
    params = GET.copy()
    params[new_param] = new_value
    return params.urlencode()


@register.filter
def create_order_by_link(value):
    return value

@register.filter
def add_class(field, new_cls):
    #return mark_safe(re.sub(r'(<(select|input|textarea).*?class=\")', '\1%s ' % new_cls, str(field)))
    #cls = field.field.widget.attrs.get('class', '')
    #cls += ' ' + new_cls
    if isinstance(field.field.widget, (forms.CheckboxInput, forms.RadioSelect, forms.CheckboxSelectMultiple)):
        return field
    #elif isinstance(field.field.widget, forms.MultiValueWidget):
    #    attrs = field.field.widget.get_widgets()
    else:
        # MultiValueWidget?
        attrs = field.field.widget.attrs
        if 'class' in attrs:
            attrs['class'] += ' %s' % new_cls
        else:
            attrs['class'] = new_cls
        return mark_safe(field.as_widget())
        #return mark_safe(field.as_widget(attrs={"class":new_cls}))


@register.filter
def classname(obj):
    return obj.__class__.__name__

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
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)


@register.filter
def random_id(obj):
    """Overwrite bound form field with random ID (workaround for location/map)"""
    return obj.as_widget(attrs={'id': obj.auto_id + ('_%i' % uuid4())})


@register.simple_tag
def get_user_role(user):
    output = []
    roles = OrderedDict()
    roles['Administrators'] = _('Administrator')
    roles['Editors'] = _('Editor')
    roles['Reporters'] = _('Reporter')
    groups = [g.name for g in user.groups.all()]
    for role, name in roles.items():
        if role in groups:
            output.append(str(name))
    if not output:
        output.append(str(_('No role')))
    userregionalinfo = None
    try:
        userregionalinfo = user.userregionalinfo
    except:
        pass
    if userregionalinfo:
        area = [c.name for c in user.userregionalinfo.country.all()]
        area.extend([r.name for r in user.userregionalinfo.region.all()])
        if area:
            output.append(str(_('for')))
            output.append(', '.join(area))
    return ' '.join(output)


@register.filter
def history(item, user):
    return item.get_history(user)


@register.filter
def history_count(item, user):
    return len(item.get_history(user))


@register.filter
def is_editable(activity, user):
    return activity.is_editable(user)


@register.filter
def get_latest(activity, user):
    return activity.get_latest(user)


@register.filter
def deslugify(slug):
    return title(slug.replace('_', ' ').replace('-', ' '))
