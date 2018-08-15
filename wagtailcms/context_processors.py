from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from wagtailcms.models import WagtailRootPage
from wagtailcms.models import CountryPage, RegionPage

from landmatrix.models import Country


def add_root_page(request):
    return {
        'wagtail_root_page': WagtailRootPage.objects.first()
    }

def add_data_source_dir(request):
    return {
        'DATA_SOURCE_DIR': settings.DATA_SOURCE_DIR
    }

def add_countries_and_regions(request):
    # Countries: Land Observatories
    countries = []
    observatories = CountryPage.objects.filter(live=True).order_by('title')
    countries.append({
        'text': _('Observatories'),
        'children': [[country.country.id if country.country else None, country.slug, country.title]
                     for country in observatories]
    })
    other_countries = Country.objects.filter(is_target_country=True, high_income=False)
    other_countries = other_countries.exclude(id__in=[c.country.id
                                                      for c in observatories if c.country])
    other_countries = other_countries.only('id', 'slug', 'name').order_by('name')
    countries.append({
        'text': _('Other'),
        'children': [[country.id, country.slug, country.name] for country in other_countries]
    })

    # Filter out pages without an assigned region, those just error
    regions = RegionPage.objects.filter(region__isnull=False).order_by('title')
    regions = [[region.region.id, region.slug, region.title] for region in regions]

    return {
        'nav_countries': countries,
        'nav_regions': regions,
    }