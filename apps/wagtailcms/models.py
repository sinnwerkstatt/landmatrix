from django import forms
from django.db import models
from django.db.models import F, Count, Sum
from wagtail.admin.edit_handlers import (
    FieldPanel,
    StreamFieldPanel,
    FieldRowPanel,
)
from wagtail.admin.edit_handlers import RichTextFieldPanel
from wagtail.api import APIField
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.core.fields import RichTextField
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.core.models import Page
from wagtail.core.rich_text import expand_db_html

from apps.blog.models import BlogPage
from apps.landmatrix.models import Region, Country, Deal
from apps.landmatrix.models import Region as DataRegion
from apps.landmatrix.models.country import Country as DataCountry
from apps.wagtailcms.blocks import (
    COLUMN_BLOCKS,
    CONTENT_BLOCKS,
    DATA_BLOCKS,
    NoWrapsStreamField,
)
from apps.wagtailcms.blocks import SIMPLE_CONTENT_BLOCKS
from apps.wagtailcms.twitter import TwitterTimeline


@register_setting(icon="radio-empty")
class ChartDescriptionsSettings(BaseSetting):
    web_of_transnational_deals = RichTextField()
    dynamics_overview = RichTextField()
    produce_info_map = RichTextField()

    class Meta:
        verbose_name = "Chart descriptions"

    def to_dict(self):
        return {
            "web_of_transnational_deals": expand_db_html(
                self.web_of_transnational_deals
            ),
            "dynamics_overview": expand_db_html(self.dynamics_overview),
            "produce_info_map": expand_db_html(self.produce_info_map),
        }

    panels = [
        RichTextFieldPanel("web_of_transnational_deals"),
        RichTextFieldPanel("dynamics_overview"),
        RichTextFieldPanel("produce_info_map"),
    ]


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

    def twitter_feed(self):
        if self.twitter_username:
            tweets = TwitterTimeline().get_timeline(self.twitter_username)
            if tweets:
                return {
                    "username": self.twitter_username,
                    "timeline": tweets,
                }

    def related_blogpages(self):
        if not self.region and not self.country:
            return []
        slug = self.country.slug if self.country else self.region.slug

        return [
            article.get_dict("fill-500x500|jpegquality-60")
            for article in BlogPage.objects.live()
            .order_by("-date")
            .filter(tags__slug=slug)
            .filter(
                blog_categories__slug__in=[
                    "country-profile",
                    "news",
                    "publications",
                ]
            )
        ]

    # @staticmethod
    # def current_negotiation_status_metrics():
    #     deals = Deal.objects.visible(subset="PUBLIC").default_filtered(
    #         unset_filters=["current_negotiation_status"]
    #     )
    #     return (
    #         deals.values(value=F("current_negotiation_status"))
    #         .annotate(count=Count("pk"))
    #         .annotate(size=Sum("deal_size"))
    #     )

    api_fields = [
        APIField("short_description"),
        APIField("introduction_text"),
        APIField("body"),
        APIField("region"),
        APIField("country"),
        APIField("twitter_feed"),
        APIField("related_blogpages"),
        # APIField("current_negotiation_status_metrics"),
    ]
