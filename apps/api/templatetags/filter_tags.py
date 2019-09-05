from django import template
from django.http import QueryDict

from ..filters import clean_filter_query_string

register = template.Library()


@register.simple_tag(takes_context=True)
def filter_query_params(context):
    """
    Returns a urlencoded sequence of get params that are allowed filters.

    Appended to URL tags for filterable views.
    """
    request = context['request']
    clean_query_string = clean_filter_query_string(request)

    if clean_query_string:
        params = '?{}'.format(clean_query_string.urlencode())
    else:
        params = ''

    return params


@register.simple_tag(takes_context=True)
def list_params(context):
    if 'list_params' not in context:
        params = QueryDict(mutable=True)

        # Check for country/region in context
        country = context.get('country', '')
        if country:
            params['country'] = country.id
        region = context.get('region', '')
        if region:
            params['region'] = region.id

        # Check for country/region in page
        page = context.get('page', '')
        if hasattr(page, 'country'):
            params['country'] = page.country.id
        elif hasattr(page, 'region'):
            params['region'] = page.region.id

        # Check for country/region in request params or fallback to all params
        request = context.get('request', '')
        if request.GET:
            if 'country' in request.GET:
                params['country'] = request.GET.get('country')
            elif 'region' in request.GET:
                params['region'] = request.GET.get('region')

        # Check for status in request
        request = context.get('request', '')
        if request.GET:
            if 'status' in request.GET:
                params.setlist('status', request.GET.getlist('status'))

        context['list_params'] = '?%s' % params.urlencode()

    return context['list_params']
