from django.http.response import HttpResponse
from django.views.generic.base import View

from wagtailcms.models import RegionIndex, Region

class RegionView(View):
    def get(self, *args, **kwargs):
    	try:
    		region = Region.objects.get(slug=kwargs.get('region_slug'))
    	except:
	    	region = RegionIndex.objects.get(slug='region')
    	return region.serve(self.request)
