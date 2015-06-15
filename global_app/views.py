
from django.views.generic import View
from django.http import HttpResponse

def test_view(request):
    return HttpResponse("<html><body>Howdy.</body></html>")