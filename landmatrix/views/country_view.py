from django.http.response import HttpResponse
from django.views.generic.base import View

class CountryView(View):
    def get(self, *args, **kwargs):
    	return HttpResponse()
