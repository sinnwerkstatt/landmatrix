from apps.blog.models import BlogIndexPage
from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions

from .models import *


@register(WagtailRootPage)
class WagtailRootPageTR(TranslationOptions):
    fields = (
        "body",
        "map_introduction",
        "data_introduction",
        # 'charts_introduction',
        "footer_column_1",
        "footer_column_2",
        "footer_column_3",
        "footer_column_4",
    )


@register(WagtailPage)
class WagtailPageTR(TranslationOptions):
    fields = ("body",)


@register(RegionIndex)
class RegionIndexTR(TranslationOptions):
    fields = ("body",)


@register(RegionPage)
class RegionPageTR(TranslationOptions):
    fields = ("body",)


@register(CountryIndex)
class CountryIndexTR(TranslationOptions):
    fields = ("body",)


@register(CountryPage)
class CountryPageTR(TranslationOptions):
    fields = ("body",)


@register(BlogIndexPage)
class BlogIndexPageTR(TranslationOptions):
    pass


@register(BlogPage)
class BlogPageTR(TranslationOptions):
    pass
