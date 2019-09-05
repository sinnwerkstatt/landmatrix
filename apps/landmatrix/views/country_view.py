from django.http import Http404
from django.views.generic.base import View

from apps.wagtailcms.models import CountryIndex, CountryPage


class CountryView(View):

    def get(self, *args, **kwargs):
        try:
            country = CountryPage.objects.get(slug=kwargs.get('country_slug'))
        except CountryPage.DoesNotExist:
            try:
                country = CountryIndex.objects.get(slug='country')
            except CountryIndex.DoesNotExist:
                raise Http404('Country index not found.')

        return country.serve(self.request)
