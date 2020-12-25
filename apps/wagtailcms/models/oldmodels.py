from django import forms
from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.api import APIField
from wagtail.core.models import Page

from apps.landmatrix.models import Region as DataRegion
from apps.landmatrix.models.country import Country as DataCountry
from apps.wagtailcms.blocks import (
    COLUMN_BLOCKS,
    CONTENT_BLOCKS,
    Columns1To1Block,
    DATA_BLOCKS,
    NoWrapsStreamField,
    ThreeColumnsBlock,
    get_country_or_region,
)
from apps.wagtailcms.twitter import TwitterTimeline


class WagtailRootPage(Page):
    is_creatable = False
    body = NoWrapsStreamField(CONTENT_BLOCKS + DATA_BLOCKS + COLUMN_BLOCKS)

    content_panels = Page.content_panels + [
        StreamFieldPanel("body"),
    ]
    api_fields = [
        APIField("body"),
    ]


class WagtailPage(Page):
    body = NoWrapsStreamField(CONTENT_BLOCKS + DATA_BLOCKS + COLUMN_BLOCKS)
    content_panels = Page.content_panels + [StreamFieldPanel("body")]
    api_fields = [APIField("body")]


class RegionIndex(Page):
    max_count = 1
    template = "wagtailcms/region_page.html"

    body = NoWrapsStreamField(CONTENT_BLOCKS + DATA_BLOCKS + COLUMN_BLOCKS)
    content_panels = Page.content_panels + [StreamFieldPanel("body")]
    subpage_types = ["wagtailcms.RegionPage"]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context.update(get_country_or_region(request))
        return context

    api_fields = [APIField("body")]


class RegionPage(Page):
    region = models.OneToOneField(
        DataRegion, null=True, blank=True, on_delete=models.SET_NULL
    )
    short_description = models.CharField(
        max_length=200, blank=True, null=True, help_text="Displayed in sidebar of map"
    )
    twitter_username = models.CharField(max_length=200, blank=True, null=True)
    introduction_text = models.TextField(
        max_length=700,
        blank=True,
        null=True,
        help_text="Introduction before 'Read more'",
    )
    body = NoWrapsStreamField(CONTENT_BLOCKS + DATA_BLOCKS + COLUMN_BLOCKS)

    content_panels = Page.content_panels + [
        FieldPanel("introduction_text"),
        StreamFieldPanel("body"),
    ]
    promote_panels = [
        FieldPanel("region"),
        FieldPanel("short_description", widget=forms.Textarea),
        FieldPanel("twitter_username"),
    ] + Page.promote_panels
    parent_page_types = ["wagtailcms.RegionIndex"]

    @property
    def twitter_feed(self):
        if self.twitter_username:
            tweets = TwitterTimeline().get_timeline(self.twitter_username)
            if tweets:
                return {
                    "username": self.twitter_username,
                    "timeline": tweets,
                }

    api_fields = [
        APIField("introduction_text"),
        APIField("body"),
        APIField("region"),
        APIField("twitter_feed"),
    ]


class CountryIndex(Page):
    max_count = 1
    template = "wagtailcms/country_page.html"

    body = NoWrapsStreamField(CONTENT_BLOCKS + DATA_BLOCKS + COLUMN_BLOCKS)
    content_panels = Page.content_panels + [StreamFieldPanel("body")]
    subpage_types = ["wagtailcms.CountryPage"]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context.update(get_country_or_region(request))
        return context

    api_fields = [APIField("body")]


class CountryPage(Page):
    country = models.OneToOneField(
        DataCountry, null=True, blank=True, on_delete=models.SET_NULL
    )
    short_description = models.CharField(
        max_length=200, blank=True, null=True, help_text="Displayed in sidebar of map"
    )
    twitter_username = models.CharField(max_length=200, blank=True, null=True)
    introduction_text = models.TextField(
        max_length=700,
        blank=True,
        null=True,
        help_text="Introduction before 'Read more'",
    )
    body = NoWrapsStreamField(
        CONTENT_BLOCKS
        + [("columns_1_1", Columns1To1Block()), ("columns_3", ThreeColumnsBlock())]
    )

    content_panels = Page.content_panels + [
        FieldPanel("introduction_text"),
        StreamFieldPanel("body"),
    ]
    promote_panels = [
        FieldPanel("country"),
        FieldPanel("short_description", widget=forms.Textarea),
        FieldPanel("twitter_username"),
    ] + Page.promote_panels
    parent_page_types = ["wagtailcms.CountryIndex"]

    def twitter_feed(self):
        if self.twitter_username:
            tweets = TwitterTimeline().get_timeline(self.twitter_username)
            if tweets:
                return {
                    "username": self.twitter_username,
                    "timeline": tweets,
                }

    api_fields = [
        APIField("introduction_text"),
        APIField("body"),
        APIField("country"),
        APIField("twitter_feed"),
    ]
