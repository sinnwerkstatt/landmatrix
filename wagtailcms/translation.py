from wagtail_modeltranslation.translation import TranslationOptions
from wagtail_modeltranslation.decorators import register

from .models import *

@register(WagtailRootPage)
class WagtailRootPageTR(TranslationOptions):
    fields = (
        'body',
    )

@register(WagtailPage)
class WagtailPageTR(TranslationOptions):
	fields = (
		'body',
	)

@register(RegionIndex)
class RegionIndexTR(TranslationOptions):
	fields = (
		'body',
	)

@register(Region)
class RegionTR(TranslationOptions):
	fields = (
		'body',
	)

@register(CountryIndex)
class CountryIndexTR(TranslationOptions):
	fields = (
		'body',
	)

@register(Country)
class CountryTR(TranslationOptions):
	fields = (
		'body',
	)


