from django import template
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from apps.landmatrix.models import Country
from apps.wagtailcms.models import CountryPage, RegionPage, WagtailRootPage

register = template.Library()


@register.simple_tag
def wagtail_root_page():
    return WagtailRootPage.objects.first()


@register.simple_tag
def nav_regions():
    regions = (
        RegionPage.objects.filter(live=True, region__isnull=False)
        .order_by("title")
        .values_list("region_id", "slug", "title")
    )
    return regions


@register.simple_tag
def nav_countries():
    observatories = CountryPage.objects.filter(
        live=True, country__isnull=False
    ).order_by("title")
    other_countries = (
        Country.objects.filter(high_income=False)
        .exclude(id__in=[c.country.id for c in observatories if c.country])
        .only("id", "slug", "name")
        .order_by("name")
    )

    countries = [
        {
            "text": _("Observatories"),
            "children": [
                [
                    country.country.id if country.country else None,
                    country.slug,
                    country.title,
                ]
                for country in observatories
            ],
        },
        {
            "text": _("Other"),
            "children": [
                [country.id, country.slug, country.name] for country in other_countries
            ],
        },
    ]
    return countries
