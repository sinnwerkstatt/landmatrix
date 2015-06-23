__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django.http import HttpResponse

def test_view(request):
    return HttpResponse("<html><body>Howdy.</body></html>")

