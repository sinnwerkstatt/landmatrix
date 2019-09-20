from blog.models import BlogPage
from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page

from apps.landmatrix.models.country import Country as DataCountry
from apps.landmatrix.models.region import Region as DataRegion
from apps.wagtailcms.blocks import COLUMN_BLOCKS, CONTENT_BLOCKS, Columns1To1Block, DATA_BLOCKS, NoWrapsStreamField, ThreeColumnsBlock, \
    get_country_or_region


class WagtailRootPage(Page):
    body = NoWrapsStreamField(CONTENT_BLOCKS + DATA_BLOCKS + COLUMN_BLOCKS)
    map_introduction = RichTextField(blank=True)
    data_introduction = RichTextField(blank=True)
    # charts_introduction = RichTextField(blank=True)
    footer_column_1 = RichTextField(blank=True)
    footer_column_2 = RichTextField(blank=True)
    footer_column_3 = RichTextField(blank=True)
    footer_column_4 = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
        FieldPanel('map_introduction'),
        FieldPanel('data_introduction'),
        # FieldPanel('charts_introduction'),
        FieldPanel('footer_column_1'),
        FieldPanel('footer_column_2'),
        FieldPanel('footer_column_3'),
        FieldPanel('footer_column_4')
    ]


class WagtailPage(Page):
    body = NoWrapsStreamField(CONTENT_BLOCKS + DATA_BLOCKS + COLUMN_BLOCKS)
    content_panels = Page.content_panels + [StreamFieldPanel('body')]


class RegionIndex(Page):
    template = 'wagtailcms/region_page.html'

    body = NoWrapsStreamField(CONTENT_BLOCKS + DATA_BLOCKS + COLUMN_BLOCKS)
    content_panels = Page.content_panels + [
        StreamFieldPanel('body')
    ]
    subpage_types = ['wagtailcms.RegionPage']

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context.update(get_country_or_region(request))
        return context


class RegionPage(Page):
    region = models.ForeignKey(DataRegion, null=True, blank=True, on_delete=models.SET_NULL)

    body = NoWrapsStreamField(CONTENT_BLOCKS + DATA_BLOCKS + COLUMN_BLOCKS)
    content_panels = Page.content_panels + [
        StreamFieldPanel('body')
    ]
    promote_panels = [
                         FieldPanel('region'),
                     ] + Page.promote_panels
    parent_page_types = ['wagtailcms.RegionIndex']


class CountryIndex(Page):
    template = 'wagtailcms/country_page.html'

    body = NoWrapsStreamField(CONTENT_BLOCKS + DATA_BLOCKS + COLUMN_BLOCKS)
    content_panels = Page.content_panels + [
        StreamFieldPanel('body')
    ]
    subpage_types = ['wagtailcms.CountryPage']

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context.update(get_country_or_region(request))
        return context


class CountryPage(Page):
    country = models.ForeignKey(DataCountry, null=True, blank=True, on_delete=models.SET_NULL)
    body = NoWrapsStreamField(CONTENT_BLOCKS + [
        ('columns_1_1', Columns1To1Block()),
        ('columns_3', ThreeColumnsBlock()),
    ]
                              )
    content_panels = Page.content_panels + [
        StreamFieldPanel('body')
    ]
    promote_panels = [
                         FieldPanel('country')
                     ] + Page.promote_panels
    parent_page_types = ['wagtailcms.CountryIndex']
