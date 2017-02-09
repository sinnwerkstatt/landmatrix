from django import template

from api.filters import clean_filter_query_string


register = template.Library()


@register.simple_tag(takes_context=True)
def filter_query_params(context):
    '''
    Returns a urlencoded sequence of get params that are allowed filters.

    Appended to URL tags for filterable views.
    '''
    request = context['request']
    clean_query_string = clean_filter_query_string(request)

    if clean_query_string:
        params = '?{}'.format(clean_query_string.urlencode())
    else:
        params = ''

    return params
