from django.http import Http404
from django.views.generic.base import View

from wagtailcms.models import CountryIndex, CountryPage


class CountryView(View):

    def get(self, *args, **kwargs):
        country_slug = kwargs.get('country_slug')

        if country_slug:
            try:
                country = CountryPage.objects.get(slug=country_slug)
            except CountryPage.DoesNotExist:
                raise Http404('Country not found.')
        else:
            try:
                country = CountryIndex.objects.get(slug='country')
            except CountryIndex.DoesNotExist:
                raise Http404('Country index not found.')

        return country.serve(self.request)
