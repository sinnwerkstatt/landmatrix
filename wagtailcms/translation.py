from wagtail_modeltranslation.translation import TranslationOptions
from wagtail_modeltranslation.decorators import register

from .models import *

@register(WagtailRootPage)
class WagtailRootPageTR(TranslationOptions):
    fields = (
        'body',
        'footer_column_1',
    	'footer_column_2',
    	'footer_column_3',
    	'footer_column_4',
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

@register(RegionPage)
class RegionPageTR(TranslationOptions):
	fields = (
		'body',
	)

@register(CountryIndex)
class CountryIndexTR(TranslationOptions):
	fields = (
		'body',
	)

@register(CountryPage)
class CountryPageTR(TranslationOptions):
	fields = (
		'body',
	)


