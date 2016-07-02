from django.http.response import HttpResponse
from django.views.generic.base import View

from wagtailcms.models import CountryIndex, CountryPage

class CountryView(View):
    def get(self, *args, **kwargs):
        try:
            country = CountryPage.objects.get(slug=kwargs.get('country_slug'))
        except:
            country = CountryIndex.objects.get(slug='country')
        return country.serve(self.request)
