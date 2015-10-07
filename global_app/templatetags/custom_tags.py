import time, datetime

from django import template
from django.template import Library, Node, resolve_variable, TemplateSyntaxError
from django.template import Context, Template, Node, resolve_variable, TemplateSyntaxError, Variable
from django.template.defaultfilters import slugify
from django.template.defaultfilters import stringfilter
from django.contrib.humanize.templatetags.humanize import naturaltime
# from django.utils.encoding import force_unicode


# from editor.views import get_display_value_by_field

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


@register.filter
def get_range( value ):
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
    time_format = "%Y-%m-%d %H:%M:%S"
    date = datetime.datetime.fromtimestamp(time.mktime(time.strptime(value, time_format)))
    natural_time = naturaltime(date)
    natural_time = natural_time.split(",")
    if len(natural_time) == 1:
        return natural_time[0]
    else:
        return "%s ago" % natural_time[0]

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
