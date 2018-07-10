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
    # Check for country/region in context
    country = context.get('country', '')
    if country:
        return '?country={}'.format(country.id)
    region = context.get('region', '')
    if region:
        return '?region={}'.format(region.id)

    # Check for country/region in page
    page = context.get('page', '')
    if hasattr(page, 'country'):
        return '?country={}'.format(page.country.id)
    elif hasattr(page, 'region'):
        return '?region={}'.format(page.region.id)

    # Check for country/region in request params or fallback to all params
    request = context.get('request', '')
    if request.GET:
        if 'country' in request.GET:
            return '?country={}'.format(request.GET.get('country'))
        elif 'region' in request.GET:
            return '?region={}'.format(request.GET.get('region'))
        else:
            return '?{}'.format(request.GET.urlencode())

    return ''