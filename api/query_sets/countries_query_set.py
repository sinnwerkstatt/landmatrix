from django.utils.translation import ugettext_lazy as _

from api.query_sets.simple_fake_query_set import SimpleFakeQuerySet
from landmatrix.models.country import Country
from wagtailcms.models import CountryPage



class CountriesQuerySet(SimpleFakeQuerySet):
    def all(self):
        #if self.get_data.get('region'): #FIXME: Doesn't work, get_data returns request
        #    countries = Country.objects.filter(fk_region__slug=self.get_data['region']).order_by('name')
        #else:
        # Return country pages then all other countries in two option groups
        response = []
        countries = CountryPage.objects.filter(live=True).order_by('title')
        response.append({
            'text': str(_('Observatories')),
            'children': [[country.id, country.slug, country.title] for country in countries]
        })
        countries = Country.objects.filter(is_target_country=True).exclude(
            id__in=[c.country.id for c in countries]
        ).only('id', 'slug', 'name').order_by('name')
        response.append({
            'text': str(_('Other')),
            'children': [[country.id, country.slug, country.name] for country in countries]
        })
        return response
