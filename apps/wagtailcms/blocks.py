import json
import re

from django.contrib.sites.models import Site
from django.utils.html import format_html_join
from wagtail.core import blocks
from wagtail.core.blocks import Block, RawHTMLBlock, StreamBlock, StructBlock
from wagtail.core.fields import StreamField
from wagtail.core.rich_text import expand_db_html
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock

from apps.blog.models import BlogPage
from apps.landmatrix.models import Region as DataRegion
from apps.landmatrix.models.country import Country as DataCountry
from apps.wagtailcms.twitter import TwitterTimeline


class RichTextBlock(blocks.RichTextBlock):
    def get_api_representation(self, value, context=None):
        prep_val = self.get_prep_value(value)
        return expand_db_html(prep_val)


class ExternalLinkMixin:
    def _is_external_link(self, url):
        current_site = Site.objects.get_current()
        if current_site and current_site.domain in url:
            return False
        elif re.match(r"^(?!www\.|(?:http|ftp)s?://|[A-Za-z]:\\|//).*", url):
            return False
        else:
            return True


class LinkBlock(ExternalLinkMixin, StructBlock):
    cls = blocks.ChoiceBlock(
        choices=[("btn", "Button"), ("btn btn-with-space", "Button (with space)")],
        required=False,
        label="Type",
    )
    url = blocks.URLBlock(label="URL")
    text = blocks.CharBlock()

    class Meta:
        icon = "anchor"
        template = "widgets/link.html"

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        context["href"] = get_country_or_region_link(
            value.get("url"),
            request=parent_context.get("request"),
            page=parent_context.get("page"),
        )
        context["external"] = self._is_external_link(context["href"])
        context["text"] = value.get("text")
        context["class"] = value.get("cls")
        return context


class AnchorBlock(StructBlock):
    slug = blocks.CharBlock()

    class Meta:
        icon = "anchor"
        template = "widgets/anchor.html"

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        context["slug"] = value.get("slug")
        return context


class FAQBlock(StructBlock):
    slug = blocks.CharBlock()
    question = blocks.CharBlock()
    answer = RichTextBlock()


class FAQsBlock(StructBlock):
    faqs = blocks.ListBlock(FAQBlock())

    class Meta:
        icon = "fa fa-medkit"
        template = "widgets/faq_block.html"

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        context["title"] = value.get("title")
        context["list"] = []
        for faq in value.get("faqs"):
            context["list"].append(
                {
                    "slug": faq.get("slug"),
                    "term": faq.get("question"),
                    "definition": faq.get("answer"),
                }
            )
        return context


class TwitterBlock(StructBlock):
    username = blocks.CharBlock(required=True)
    count = blocks.CharBlock(default=20)

    # help_text='You will find username and widget_id @ https://twitter.com/settings/widgets/')
    # widget_id = CharBlock(required=True)
    # tweet_limit = CharBlock(required=True, max_length=2)

    class Meta:
        icon = "fa fa-twitter"
        template = "widgets/twitter.html"

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        twitte = TwitterTimeline(count=(value.get("count")))
        context["timeline"] = twitte.get_timeline(value.get("username"))
        context["username"] = value.get(
            "username"
        )  # context['timeline'][0]['screen_name']
        return context

    def get_api_representation(self, value, context=None):
        timeline = TwitterTimeline(count=(value.get("count")))
        val = {
            "username": value.get("username"),
            "timeline": timeline.get_timeline(value.get("username")),
        }
        return val


# Overwrite Stream block to disable wrapping DIVs
class NoWrapsStreamBlock(StreamBlock):
    def render_basic(self, value, context=None):
        def get_class(block):
            if block.block_type != "full_width_container":
                return "block-%s block" % block.block_type
            else:
                return ""

        return format_html_join(
            "\n",
            '<div class="{1}">{0}</div>',
            [(child.render(context=context), get_class(child)) for child in value],
        )


class NoWrapsStreamField(StreamField):
    def __init__(self, block_types, **kwargs):
        super().__init__(block_types, **kwargs)
        if isinstance(block_types, Block):
            self.stream_block = block_types
        elif isinstance(block_types, type):
            self.stream_block = block_types()
        else:
            self.stream_block = NoWrapsStreamBlock(block_types)


class ImageBlock(ImageChooserBlock):
    url = blocks.URLBlock(required=False, label="URL")

    class Meta:
        icon = "image"
        template = "widgets/image.html"

    def get_context(self, value, parent_context=None):
        context = super().get_context(value)
        context["url"] = value.get_rendition("max-1200x1200").url
        context["name"] = value.title
        return context

    def get_api_representation(self, value, context=None):
        url = value.get_rendition("max-1200x1200").url
        prep_val = self.get_prep_value(value)
        ret = {"id": prep_val, "url": url}
        return ret


class SectionDivider(StructBlock):
    class Meta:
        icon = "fa fa-minus"
        template = "widgets/divider.html"


class LinkedImageBlock(ExternalLinkMixin, StructBlock):
    image = ImageChooserBlock()
    url = blocks.URLBlock(required=False, label="URL")
    caption = RichTextBlock(required=False)

    class Meta:
        icon = "image"
        template = "widgets/image.html"

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        context["href"] = get_country_or_region_link(
            value.get("url"),
            request=parent_context and parent_context.get("request"),
            page=parent_context and parent_context.get("page"),
        )
        context["external"] = self._is_external_link(context["href"])
        image = value.get("image")
        context["url"] = image.get_rendition("max-1200x1200").url
        context["name"] = image.title
        context["caption"] = value.get("caption")
        return context

    def get_api_representation(self, value, context=None):
        url = value["image"].get_rendition("max-1200x1200").url
        prep_val = self.get_prep_value(value)
        image_id = prep_val["image"]
        prep_val["image"] = {"id": image_id, "url": url}
        prep_val["external"] = self._is_external_link(prep_val["url"])
        return prep_val


class SliderBlock(StructBlock):
    images = blocks.ListBlock(LinkedImageBlock())

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        context["title"] = value.get("title")
        images_data = value.get("images")
        images = []
        if images_data:
            for image in images_data:
                rendition = image.get("image").get_rendition("max-1200x1200")
                url = rendition.url
                name = image.get("image").title
                image_context = {
                    "url": url,
                    "name": name,
                    "href": image.get("url"),
                    "caption": image.get("caption"),
                }
                images.append(image_context)
        context["images"] = images
        return context

    class Meta:
        icon = "fa fa-picture-o"
        label = "Slider"
        template = "widgets/slider.html"


class GalleryBlock(StructBlock):
    columns = blocks.ChoiceBlock(
        choices=[
            (1, "1 column"),
            (2, "2 columns"),
            (3, "3 columns"),
            (4, "4 columns"),
            (5, "5 columns"),
            (6, "6 columns"),
        ],
        icon="fa fa-columns",
    )
    images = blocks.ListBlock(LinkedImageBlock())

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        context["title"] = value.get("title")
        columns_data = value.get("columns")
        if columns_data and columns_data.isdigit():
            context["columns"] = int(columns_data)
        images_data = value.get("images")
        images = []
        if images_data:
            for image in images_data:
                if not image.get("image"):  # pragma: no cover
                    continue
                rendition = image.get("image").get_rendition("max-1200x1200")
                url = rendition.url
                name = image.get("image").title
                image_context = {"url": url, "name": name, "href": image.get("url")}
                images.append(image_context)
        context["images"] = images
        return context

    class Meta:
        icon = "fa fa-th"
        label = "Gallery"
        template = "widgets/gallery.html"


class TitleBlock(blocks.CharBlock):
    class Meta:
        icon = "title"
        label = "Title"
        template = "widgets/title.html"


class TitleWithIconBlock(StructBlock):
    value = blocks.CharBlock(label="Title")
    fa_icon = blocks.CharBlock(required=False)
    url = blocks.URLBlock(label="URL", required=False)

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        context["value"] = value.get("value")
        context["fa_icon"] = value.get("fa_icon")
        context["url"] = get_country_or_region_link(
            value.get("url"),
            request=parent_context.get("request"),
            page=parent_context.get("page"),
        )
        return context

    class Meta:
        icon = "title"
        label = "Title with Icon"
        template = "widgets/title.html"


CONTENT_BLOCKS = [
    ("heading", TitleBlock()),
    ("title", TitleWithIconBlock()),
    ("paragraph", RichTextBlock()),
    ("image", ImageBlock()),
    ("linked_image", LinkedImageBlock()),
    ("media", EmbedBlock(icon="media")),
    ("html", RawHTMLBlock(icon="code")),
    ("link", LinkBlock(icon="link")),
    ("anchor", AnchorBlock(icon="link")),
    ("gallery", GalleryBlock()),
    ("slider", SliderBlock()),
    ("section_divider", SectionDivider()),
    ("twitter", TwitterBlock()),
    ("faqs_block", FAQsBlock()),
]

SIMPLE_CONTENT_BLOCKS = [
    (
        "paragraph",
        RichTextBlock(
            features=[
                "bold",
                "italic",
                "h2",
                "h3",
                "ol",
                "ul",
                "hr",
                "link",
                "image",
                "document-link",
            ]
        ),
    ),
    ("link", LinkBlock(icon="link")),
    ("anchor", AnchorBlock(icon="link")),
    ("image", ImageBlock()),
    ("linked_image", LinkedImageBlock()),
    ("media", EmbedBlock(icon="media")),
    ("gallery", GalleryBlock()),
    ("slider", SliderBlock()),
    ("section_divider", SectionDivider()),
    ("faqs_block", FAQsBlock()),
]


def get_country_or_region(request, page=None):
    """
    Get country or region from current page (if CountryPage/RegionPage)
    or from URL query (if CountryIndexPage/RegionIndexPage)
    """
    result = {"region": None, "country": None}
    if hasattr(page, "region"):
        result["region"] = page.region
    elif hasattr(page, "country"):
        result["country"] = page.country
    elif request and hasattr(request, "resolver_match") and request.resolver_match:
        kwargs = request.resolver_match.kwargs
        if "region_slug" in kwargs:
            result["region"] = DataRegion.objects.get(slug=kwargs.get("region_slug"))
        elif "country_slug" in kwargs:
            result["country"] = DataCountry.objects.get(slug=kwargs.get("country_slug"))
    return result


def get_country_or_region_link(link, request=None, page=None):
    data = get_country_or_region(request, page=page)
    if data.get("region", None):
        link = "%s?region=%s" % (link, data["region"].id)
    elif data.get("country", None):
        link = "%s?country=%s" % (link, data["country"].id)
    return link


class LatestNewsBlock(StructBlock):
    limit = blocks.CharBlock()

    class Meta:
        icon = "fa fa-list"
        label = "Latest news"
        template = "widgets/latest-news.html"

    def get_context(self, value, parent_context={}):
        context = super().get_context(value, parent_context=parent_context)
        context.update(
            get_country_or_region(
                parent_context.get("request"), parent_context.get("page")
            )
        )
        queryset = BlogPage.objects.live().public().order_by("-date")
        tag = None
        if context.get("country"):
            tag = context.get("country").slug
            context["name"] = context.get("country").name
        elif context.get("region"):
            tag = context.get("region").slug
            context["name"] = context.get("region").name
        if tag:
            queryset = queryset.filter(tags__slug=tag)
        limit = value.get("limit")
        context["tag"] = tag
        context["news"] = queryset[: int(limit)]
        return context


class StatisticsBlock(StructBlock):
    class Meta:
        icon = "fa fa-list"
        label = "Statistics"
        template = "widgets/statistics.html"

    def get_context(self, value, parent_context={}):
        context = super().get_context(value, parent_context=parent_context)
        context.update(
            get_country_or_region(
                parent_context.get("request"), parent_context.get("page")
            )
        )
        return context


class MapDataChartsBlock(StructBlock):
    class Meta:
        icon = "fa fa-chain"
        label = "Map / Grid / Charts"
        template = "widgets/map-data-charts.html"

    def get_context(self, value, parent_context={}):
        context = super().get_context(value, parent_context=parent_context)
        context.update(
            get_country_or_region(
                parent_context.get("request"), parent_context.get("page")
            )
        )
        return context


class LinkMapBlock(StructBlock):
    """
    Note that the map template used here is NOT the one from ol3_widgets.
    """

    class Meta:
        icon = "fa fa-map-marker"
        label = "Map"
        template = "widgets/link-map.html"

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context.update(
            get_country_or_region(
                parent_context.get("request"), parent_context.get("page")
            )
        )
        # prevent circular import
        from apps.map.views import MapSettingsMixin

        legend = MapSettingsMixin().get_legend()
        context.update(
            {
                "legend": legend,
                "legend_json": json.dumps(legend),
                "map_object": context.get("region") or context.get("country"),
                "is_country": bool(context.get("country")),
            }
        )
        return context


class LatestDatabaseModificationsBlock(StructBlock):
    limit = blocks.CharBlock()

    class Meta:
        icon = "fa fa-list"
        label = "Latest database modifications"
        template = "widgets/latest-database-modifications.html"

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context.update(
            get_country_or_region(
                parent_context.get("request"), parent_context.get("page")
            )
        )
        context["limit"] = value.get("limit")
        return context


class RegionBlock(StructBlock):
    class Meta:
        icon = "fa fa-map-marker"
        label = "Region"
        template = "widgets/region.html"

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context.update(
            get_country_or_region(
                parent_context.get("request"), parent_context.get("page")
            )
        )
        if context.get("country"):
            context["region"] = context["country"].fk_region
        return context


class CountriesBlock(StructBlock):
    class Meta:
        icon = "fa fa-flag"
        label = "Countries"
        template = "widgets/countries.html"

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context.update(
            get_country_or_region(
                parent_context.get("request"), parent_context.get("page")
            )
        )
        if context.get("region"):
            context["countries"] = DataCountry.objects.filter(
                fk_region=context.get("region")
            )
        return context


DATA_BLOCKS = [
    ("latest_news", LatestNewsBlock()),
    ("link_map", LinkMapBlock()),
    ("statistics", StatisticsBlock()),
    ("map_data_charts", MapDataChartsBlock()),
    ("latest_database_modifications", LatestDatabaseModificationsBlock()),
    ("countries", CountriesBlock()),
    ("region", RegionBlock()),
]


class Columns1To1Block(StructBlock):
    left_column = blocks.StreamBlock(CONTENT_BLOCKS + DATA_BLOCKS)
    right_column = blocks.StreamBlock(
        CONTENT_BLOCKS + DATA_BLOCKS, form_classname="pull-right"
    )

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)

        for column in ["left_column", "right_column"]:
            context[column] = value.get(column)

        return context

    class Meta:
        label = "Two Columns"
        template = "widgets/two-columns.html"
        icon = "fa fa-columns"


class ThreeColumnsBlock(StructBlock):
    left_column = blocks.StreamBlock(CONTENT_BLOCKS + DATA_BLOCKS)
    middle_column = blocks.StreamBlock(CONTENT_BLOCKS + DATA_BLOCKS)
    right_column = blocks.StreamBlock(
        CONTENT_BLOCKS + DATA_BLOCKS, form_classname="pull-right"
    )

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)

        for column in ["left_column", "middle_column", "right_column"]:
            context[column] = value.get(column)

        return context

    class Meta:
        label = "Three Columns"
        template = "widgets/three-columns.html"
        icon = "fa fa-columns"


COLUMN_BLOCKS = [
    ("columns_1_1", Columns1To1Block()),
    ("columns_3", ThreeColumnsBlock()),
]


class TabBlock(StructBlock):
    title = blocks.CharBlock()
    fa_icon = blocks.CharBlock(required=False)
    content = blocks.StreamBlock(CONTENT_BLOCKS + DATA_BLOCKS + COLUMN_BLOCKS)


class TabsBlock(StructBlock):
    tabs = blocks.ListBlock(TabBlock())

    class Meta:
        icon = "fa fa-folder"
        template = "widgets/tabs_block.html"

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        context["list"] = []
        for tab in value.get("tabs"):
            context["list"].append(
                {
                    "title": tab.get("title"),
                    "fa_icon": tab.get("fa_icon"),
                    "content": tab.get("content"),
                }
            )
        return context


CONTENT_BLOCKS += [("tabs_block", TabsBlock())]


class FullWidthContainerBlock(StructBlock):
    color = blocks.ChoiceBlock(
        choices=[
            ("white", "White"),
            ("lightgrey", "Light grey"),
            ("darkgrey", "Dark grey"),
        ],
        default="white",
    )
    content = NoWrapsStreamBlock(
        COLUMN_BLOCKS + DATA_BLOCKS + CONTENT_BLOCKS, form_classname="pull-right"
    )

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        context["content"] = value.get("content")
        context["color"] = value.get("color")
        return context

    class Meta:
        icon = "fa fa-arrows-h"
        label = "Full width container"
        template = "widgets/full-width-container.html"


CONTENT_BLOCKS += [("full_width_container", FullWidthContainerBlock(form_classname=""))]
