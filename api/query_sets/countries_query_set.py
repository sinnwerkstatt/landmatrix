from api.query_sets.simple_fake_query_set import SimpleFakeQuerySet
from landmatrix.models.country import Country

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class CountriesQuerySet(SimpleFakeQuerySet):
    def all(self):
        #if self.get_data.get('region'): #FIXME: Doesn't work, get_data returns request
        #    countries = Country.objects.filter(fk_region__slug=self.get_data['region']).order_by('name')
        #else:
        countries = Country.objects.all().order_by('name')
        return [[country.id, country.slug, country.name] for country in countries]
