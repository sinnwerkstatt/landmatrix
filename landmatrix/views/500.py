from django.shortcuts import render_to_response
from django.template import RequestContext


def handler500(request):
    response = render_to_response('500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response