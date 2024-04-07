from django import forms
from django.db import models
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel, FieldRowPanel
from wagtail.api import APIField
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting
from wagtail.fields import RichTextField, StreamField
from wagtail.images import get_image_model_string
from wagtail.models import Page, Orderable
from wagtail.snippets.models import register_snippet
from wagtail_headless_preview.models import HeadlessPreviewMixin

from apps.blog.models import BlogPage
from apps.landmatrix.models.country import Country, Region
from apps.landmatrix.models.new import DealHull
from .blocks import (
    COLUMN_BLOCKS,
    CONTENT_BLOCKS,
    DATA_BLOCKS,
    NEW_BLOCKS,
    SIMPLE_CONTENT_BLOCKS,
)
from .twitter import TwitterTimeline


@register_snippet
class Partner(Orderable):
    name = models.CharField(max_length=500, unique=True)

    class RoleChoices(models.TextChoices):
        PARTNER = "PARTNER", _("Partner")
        DONOR = "DONOR", _("Donor")

    role = models.CharField(
        choices=RoleChoices,
        default=RoleChoices.PARTNER,
    )

    homepage = models.URLField(max_length=500)

    logo = models.ForeignKey(
        get_image_model_string(),
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    def __str__(self):
        return f"{self.name} ({self.get_role_display()})"

    def to_dict(self, rendition_str):
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "homepage": self.homepage,
            "logo": self.logo.get_rendition(rendition_str).url if self.logo else None,
        }


@register_setting(icon="radio-empty")
class ChartDescriptionsSettings(BaseGenericSetting):
    web_of_transnational_deals = RichTextField()
    global_web_of_investments = RichTextField()
    dynamics_overview = RichTextField()
    produce_info_map = RichTextField()

    class Meta:
        verbose_name = "Chart descriptions"

    panels = [
        FieldPanel("global_web_of_investments"),
        FieldPanel("web_of_transnational_deals"),
        FieldPanel("dynamics_overview"),
        FieldPanel("produce_info_map"),
    ]


class WagtailRootPage(HeadlessPreviewMixin, Page):
    is_creatable = False

    body = StreamField(
        NEW_BLOCKS + CONTENT_BLOCKS + DATA_BLOCKS + COLUMN_BLOCKS,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [FieldPanel("body")]
    api_fields = [APIField("body")]


class WagtailPage(HeadlessPreviewMixin, Page):
    body = StreamField(
        CONTENT_BLOCKS + DATA_BLOCKS + COLUMN_BLOCKS, use_json_field=True
    )
    content_panels = Page.content_panels + [FieldPanel("body")]
    api_fields = [APIField("body")]


class AboutIndexPage(HeadlessPreviewMixin, Page):
    max_count = 1
    subpage_types = ["wagtailcms.WagtailPage"]


class ObservatoryIndexPage(HeadlessPreviewMixin, Page):
    max_count = 1
    subpage_types = ["wagtailcms.ObservatoryPage"]


class ObservatoryPage(HeadlessPreviewMixin, Page):
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
    body = StreamField(SIMPLE_CONTENT_BLOCKS, use_json_field=True)

    twitter_username = models.CharField(blank=True)

    content_panels = Page.content_panels + [
        FieldRowPanel(
            [FieldPanel("region"), FieldPanel("country")], classname="region-or-country"
        ),
        FieldPanel("introduction_text", widget=forms.Textarea),
        FieldPanel("body"),
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
        qs: QuerySet[BlogPage] = (
            BlogPage.objects.live()
            .order_by("-date")
            .filter(
                blog_categories__slug__in=[
                    "country-profile",
                    "news",
                    "publications",
                ]
            )
        )
        if self.country or self.region:
            slug = self.country.slug if self.country else self.region.slug
            qs = qs.filter(tags__slug=slug)
        return [article.get_dict("fill-500x500|jpegquality-60") for article in qs]

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

    def markers(self):
        return DealHull.get_geo_markers(self.region_id, self.country_id)

    api_fields = [
        APIField("short_description"),
        APIField("introduction_text"),
        APIField("body"),
        APIField("region"),
        APIField("country"),
        APIField("twitter_feed"),
        APIField("related_blogpages"),
        APIField("markers"),
        # APIField("current_negotiation_status_metrics"),
    ]
