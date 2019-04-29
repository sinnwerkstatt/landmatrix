from django.shortcuts import render
from django.template import RequestContext


def handler500(request):
    response = render('500.html', context=RequestContext(request))
    response.status_code = 500
    return response
