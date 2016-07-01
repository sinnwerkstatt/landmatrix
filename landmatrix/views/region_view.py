from django.http.response import HttpResponse
from django.views.generic.base import View

from wagtailcms.models import RegionIndex, RegionPage

class RegionView(View):
    def get(self, *args, **kwargs):
    	try:
    		region = RegionPage.objects.get(slug=kwargs.get('region_slug'))
    	except:
	    	region = RegionIndex.objects.get(slug='region')
    	return region.serve(self.request)
