from django import forms
from django.db import models
from wagtail.admin.edit_handlers import (
    FieldPanel,
    StreamFieldPanel,
    FieldRowPanel,
)
from wagtail.api import APIField
from wagtail.core.fields import StreamField
from wagtail.core.models import Page

from apps.landmatrix.models import Region, Country
from apps.wagtailcms.blocks import SIMPLE_CONTENT_BLOCKS
from apps.wagtailcms.twitter import TwitterTimeline


class AboutIndexPage(Page):
    max_count = 1
    subpage_types = ["wagtailcms.WagtailPage"]


class ObservatoryIndexPage(Page):
    max_count = 1
    subpage_types = ["wagtailcms.ObservatoryPage"]


class ObservatoryPage(Page):
    region = models.OneToOneField(
        Region,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="observatory_page_id",
    )
    country = models.OneToOneField(
        Country,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="observatory_page_id",
    )

    short_description = models.CharField(
        max_length=200, blank=True, help_text="Displayed in sidebar of map"
    )
    introduction_text = models.CharField(
        max_length=700,
        blank=True,
        help_text="Introduction before 'Read more'",
    )
    body = StreamField(SIMPLE_CONTENT_BLOCKS)

    twitter_username = models.CharField(max_length=200, blank=True)

    content_panels = Page.content_panels + [
        FieldRowPanel(
            [FieldPanel("region"), FieldPanel("country")], classname="region-or-country"
        ),
        FieldPanel("introduction_text", widget=forms.Textarea),
        StreamFieldPanel("body"),
    ]
    promote_panels = [
        FieldPanel("short_description", widget=forms.Textarea),
        FieldPanel("twitter_username"),
    ] + Page.promote_panels
    parent_page_types = ["wagtailcms.ObservatoryIndexPage"]
    subpage_types = ["wagtailcms.WagtailPage"]

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
        APIField("short_description"),
        APIField("introduction_text"),
        APIField("body"),
        APIField("region"),
        APIField("country"),
        APIField("twitter_feed"),
    ]
