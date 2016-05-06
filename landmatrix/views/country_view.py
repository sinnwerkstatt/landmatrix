from django.http.response import HttpResponse
from django.views.generic.base import View

from wagtailcms.models import CountryIndex, Country

class CountryView(View):
    def get(self, *args, **kwargs):
    	try:
    		country = Country.objects.get(slug=kwargs.get('country_slug'))
    	except:
	    	country = CountryIndex.objects.get(slug='countries')
    	return country.serve(self.request)
