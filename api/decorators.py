import functools

from django.http import HttpResponseRedirect

from api.filters import FILTER_VARIABLE_NAMES, clean_filter_query_string


def save_filter_query_params(session_id='filter_query_params'):
    '''
    Wrap views to save query params to session. This allows other parts of the
    site (e.g. wagtail static pages) to use standard links, but when the user
    returns to a filtered view, their filters are still present.

    Only actually used for status filtering right now, but we should move
    everything over in future.
    TODO: also, this shouldn't be in api.
    '''

    def valid_params(request):
        return [
            key for key in request.GET.keys() if key in FILTER_VARIABLE_NAMES
        ]

    def decorator(view_func):
        @functools.wraps(view_func)
        def wrapper(request, *args, **kwargs):
            current_params = valid_params(request)
            if current_params:
                # If we have params, use and save them
                clean = clean_filter_query_string(request)
                request.session[session_id] = clean.urlencode()
            else:
                # if not, load whatever we have saved, and redirect to there.
                saved_params = request.session[session_id]
                if saved_params:
                    url = '{}?{}'.format(request.path_info, saved_params)
                    return HttpResponseRedirect(url)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
