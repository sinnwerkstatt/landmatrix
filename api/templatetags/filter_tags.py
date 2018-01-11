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


@register.simple_tag(takes_context=True)
def regional_params(context):
    country = context.get('country', '')
    region = context.get('region', '')
    page = context.get('page', '')
    request = context.get('request', '')
    if country:
        return '?country={}'.format(country.id)
    elif region:
        return '?region={}'.format(region.id)
    elif hasattr(page, 'country'):
        return '?country={}'.format(page.country.id)
    elif hasattr(page, 'region'):
        return '?region={}'.format(page.region.id)
    elif request.GET:
        return '?{}'.format(request.GET.urlencode())
    return ''