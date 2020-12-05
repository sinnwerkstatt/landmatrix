from apps.blog.models import BlogPage, BlogIndexPage
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
    fields = ("introduction_text", "body", "short_description")


@register(CountryIndex)
class CountryIndexTR(TranslationOptions):
    fields = ("body",)


@register(CountryPage)
class CountryPageTR(TranslationOptions):
    fields = ("introduction_text", "body", "short_description")


@register(BlogIndexPage)
class BlogIndexPageTR(TranslationOptions):
    pass


@register(BlogPage)
class BlogPageTR(TranslationOptions):
    pass


@register(ObservatoryIndexPage)
class ObservatoryIndexPageTR(TranslationOptions):
    pass


@register(ObservatoryPage)
class ObservatoryPageTR(TranslationOptions):
    fields = ("short_description", "introduction_text", "body")


@register(ChartDescriptionsSettings)
class ChartDescriptionsSettingsTR(TranslationOptions):
    fields = ("web_of_transnational_deals", "dynamics_overview", "produce_info_map")
