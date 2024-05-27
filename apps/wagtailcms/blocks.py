import re

from django.contrib.sites.models import Site
from wagtail import blocks
from wagtail.blocks import CharBlock, RawHTMLBlock, StructBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.rich_text import expand_db_html
from wagtail.snippets.blocks import SnippetChooserBlock

from apps.landmatrix.models.country import Country as DataCountry
from apps.landmatrix.models.country import Region as DataRegion
from apps.landmatrix.models.new import DealHull

from .twitter import TwitterTimeline


class RichTextBlock(blocks.RichTextBlock):
    def get_api_representation(self, value, context=None):
        prep_val = self.get_prep_value(value)
        return expand_db_html(prep_val)


class MyDocumentChooserBlock(DocumentChooserBlock):
    def get_api_representation(self, value, context=None):
        return {
            "title": value.title,
            "file": value.file.name,
            "created_at": value.created_at,
        }


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
        icon = "suitcase-medical"

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
        icon = "twitter"

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


class NoWrapsStreamBlock(blocks.StreamBlock):
    # legacy class. keeping it for the migrations for now.
    pass


class NoWrapsStreamField(StreamField):
    # legacy class. keeping it for the migrations for now.
    pass


class ImageBlock(ImageChooserBlock):
    url = blocks.URLBlock(required=False, label="URL")

    class Meta:
        icon = "image"

    def get_context(self, value, parent_context=None):
        context = super().get_context(value)
        context["url"] = value.get_rendition("max-1200x1200").url
        context["name"] = value.title
        return context

    def get_api_representation(self, value, context=None):
        try:
            url = value.get_rendition("max-1200x1200").url
        except AttributeError:
            url = ""
        prep_val = self.get_prep_value(value)
        return {"id": prep_val, "url": url, "title": value.title}


# New Screendesign
class NewLinkBlock(blocks.StructBlock):
    page = blocks.PageChooserBlock(label="Internal link", required=False)
    external_url = blocks.URLBlock(
        label="External link",
        required=False,
        help_text=(
            "The external link will only be used if no internal link has been selected."
        ),
    )
    text = blocks.CharBlock(
        label="Button text",
        required=False,
        default="click here",
    )

    def get_api_representation(self, value, context=None):
        link = {"text": value.get("text")}
        if page := value.get("page"):
            link["href"] = page.url
        elif href := value.get("external_url"):
            link["href"] = href
            link["rel_external"] = True
        return link

    class Meta:
        label = "LinkBlock"
        label_format = "LinkBlock"
        group = "LandingPage 2023"


# New Sreendesign
class ImageTextBlock(StructBlock):
    title = blocks.CharBlock(required=False)
    subtitle = blocks.CharBlock(required=False)
    text = RichTextBlock(required=False)
    link = NewLinkBlock(required=False)
    image = ImageBlock()
    bg_color = blocks.ChoiceBlock(
        choices=[("white", "white"), ("orange", "orange")], default="white"
    )

    class Meta:
        label = "ImageTextBlock"
        label_format = "ImageTextBlock {title}"
        icon = "doc-full"
        group = "LandingPage 2023"


# New Screendesign
class PartnerBlock(StructBlock):
    def get_api_representation(self, value, context=None):
        from .models import Partner

        return [p.to_dict("max-220x220") for p in Partner.objects.all()]

    class Meta:
        label = "PartnerBlock"
        label_format = "PartnerBlock"
        group = "LandingPage 2023"


class DealCountBlock(StructBlock):
    text = CharBlock(default="It's a big deal")
    text_below = CharBlock(default="deals are currently tracked.")

    def get_api_representation(self, value, context=None):
        return {
            "deals": DealHull.objects.public().count(),
            "text": value.get("text"),
            "text_below": value.get("text_below"),
        }

    class Meta:
        label = "DealCountBlock"
        label_format = "DealCountBlock"
        group = "LandingPage 2023"


class SectionDivider(StructBlock):
    class Meta:
        icon = "minus"


class LinkedImageBlock(ExternalLinkMixin, StructBlock):
    image = ImageChooserBlock()
    url = blocks.URLBlock(required=False, label="URL")
    caption = RichTextBlock(required=False)
    lightbox = blocks.BooleanBlock(
        required=False,
        default=False,
        help_text="When selected, this image becomes clickable to show a maximized version.<br/>Beware: combining this with the URL will not work.",
    )

    class Meta:
        icon = "image"

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
        prep_val["caption"] = expand_db_html(prep_val.get("caption"))

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
        icon = "image"
        label = "Slider"


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
        icon="fa-columns",
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
        icon = "table-cells-large"
        label = "Gallery"


class TitleBlock(blocks.CharBlock):
    class Meta:
        icon = "title"
        label = "Title"


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
        icon = "list"
        label = "Latest news"

    def get_context(self, value, parent_context={}):
        context = super().get_context(value, parent_context=parent_context)
        context.update(
            get_country_or_region(
                parent_context.get("request"), parent_context.get("page")
            )
        )
        from apps.blog.models import BlogPage

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


# New Screendesign
class DataTeaserBlock(StructBlock):
    class CardBlock(StructBlock):
        title = blocks.CharBlock(max_length=200, required=False)
        teaser = blocks.CharBlock(max_length=200, required=False)
        link = NewLinkBlock(required=False)

    title = blocks.CharBlock(required=False)
    subtitle = blocks.CharBlock(required=False)
    cards = blocks.ListBlock(
        CardBlock(), min_num=3, max_num=3, help_text="Icons: 1.Maps, 2.Charts, 3.Tables"
    )

    class Meta:
        icon = "link"
        label = "DataTeaser"
        label_format = "DataTeaser"
        group = "LandingPage 2023"


# New Screendesign
class NewResourcesTeasersBlock(StructBlock):
    title = blocks.CharBlock(required=False)
    subtitle = blocks.CharBlock(required=False)
    article_highlight = blocks.PageChooserBlock(page_type="blog.BlogPage")
    other_categories = blocks.ListBlock(
        SnippetChooserBlock("blog.BlogCategory"),
        min_num=3,
        max_num=3,
        help_text="Show latest articles of 3 different categories.",
    )

    class Meta:
        icon = "list"
        label = "ResourceTeasers"
        label_format = "ResourceTeasers"
        group = "LandingPage 2023"

    def get_api_representation(self, value, context=None):
        from ..blog.models import BlogPage

        if "other_categories" in value and len(value["other_categories"]) == 3:
            other_categories = value["other_categories"]
        else:
            # fallback to latest_news, events, publications
            other_categories = [2, 5, 3]

        bp = [
            value["article_highlight"],
            *[
                BlogPage.objects.filter(blog_categories=cat).last()
                for cat in other_categories
            ],
        ]

        ret = {
            "title": value.get("title"),
            "subtitle": value.get("subtitle"),
            "image": value["article_highlight"].get_dict("fill-500x500|jpegquality-60")[
                "header_image"
            ],
            "articles": [article.get_teaser() for article in bp],
        }
        return ret


class ResourcesTeasersBlock(StructBlock):
    # limit = blocks.IntegerBlock(required=False)
    categories = blocks.ListBlock(SnippetChooserBlock("blog.BlogCategory"))

    class Meta:
        icon = "list"
        label = "Resources teasers"

    def get_api_representation(self, value, context=None):
        from apps.blog.models import BlogPage

        bp = BlogPage.objects.filter(blog_categories__in=value["categories"])
        print(bp)

        ret = {
            "articles": [
                article.get_dict("fill-500x500|jpegquality-60") for article in bp
            ]
        }
        return ret


class StatisticsBlock(StructBlock):
    class Meta:
        icon = "list"
        label = "Statistics"

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
        icon = "link"
        label = "Map / Grid / Charts"

    def get_context(self, value, parent_context={}):
        context = super().get_context(value, parent_context=parent_context)
        context.update(
            get_country_or_region(
                parent_context.get("request"), parent_context.get("page")
            )
        )
        return context


# def get_legend():
#     return {
#         "implementation": {
#             "label": _("Implementation status"),
#             "attributes": [
#                 {
#                     "label": _("Project not started"),
#                     "id": "Project not started",
#                     "color": "#1D6914",
#                 },
#                 {
#                     "label": _("Startup phase (no production)"),
#                     "id": "Startup phase (no production)",
#                     "color": "#2A4BD7",
#                 },
#                 {
#                     "label": _("In operation (production)"),
#                     "id": "In operation (production)",
#                     "color": "#575757",
#                 },
#                 {
#                     "label": _("Project abandoned"),
#                     "id": "Project abandoned",
#                     "color": "#AD2323",
#                 },
#                 {"label": _("Unknown"), "id": "Unknown", "color": "#bab8b8"},
#             ],
#         },
#         "intention": {
#             "label": _("Intention of investment"),
#             "attributes": [
#                 {
#                     "label": _("Agriculture"),
#                     "id": "Agriculture",
#                     "color": "#1D6914",
#                 },
#                 {"label": _("Forestry"), "id": "Forestry", "color": "#2A4BD7"},
#                 {"label": _("Mining"), "id": "Mining", "color": "#814A19"},
#                 {"label": _("Tourism"), "id": "Tourism", "color": "#9DAFFF"},
#                 {"label": _("Industry"), "id": "Industry", "color": "#AD2323"},
#                 {
#                     "label": _("Conservation"),
#                     "id": "Conservation",
#                     "color": "#575757",
#                 },
#                 {
#                     "label": _("Renewable Energy"),
#                     "id": "Renewable Energy",
#                     "color": "#81C57A",
#                 },
#                 {"label": _("Other"), "id": "Other", "color": "#8126C0"},
#                 {"label": _("Unknown"), "id": "Unknown", "color": "#bab8b8"},
#             ],
#         },
#         "level_of_accuracy": {
#             "label": _("Spatial accuracy"),
#             "attributes": [
#                 {"label": _("Country"), "id": "Country", "color": "#1D6914"},
#                 {
#                     "label": _("Administrative region"),
#                     "id": "Administrative region",
#                     "color": "#8126C0",
#                 },
#                 {
#                     "label": _("Approximate location"),
#                     "id": "Approximate location",
#                     "color": "#575757",
#                 },
#                 {
#                     "label": _("Exact location"),
#                     "id": "Exact location",
#                     "color": "#AD2323",
#                 },
#                 {
#                     "label": _("Coordinates"),
#                     "id": "Coordinates",
#                     "color": "#814A19",
#                 },
#                 {"label": _("Unknown"), "id": "Unknown", "color": "#bab8b8"},
#             ],
#         },
#     }


class LatestDatabaseModificationsBlock(StructBlock):
    limit = blocks.CharBlock()

    class Meta:
        icon = "list"
        label = "Latest database modifications"

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
        icon = "location-dot"
        label = "Region"

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context.update(
            get_country_or_region(
                parent_context.get("request"), parent_context.get("page")
            )
        )
        if context.get("country"):
            context["region"] = context["country"].region
        return context


class CountriesBlock(StructBlock):
    class Meta:
        icon = "flag"
        label = "Countries"

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context.update(
            get_country_or_region(
                parent_context.get("request"), parent_context.get("page")
            )
        )
        if context.get("region"):
            context["countries"] = DataCountry.objects.filter(
                region=context.get("region")
            )
        return context


DATA_BLOCKS = [
    ("latest_news", LatestNewsBlock()),
    ("resources_teasers", ResourcesTeasersBlock()),
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
        icon = "table-columns"
        group = "Layout"


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
        icon = "table-columns"
        group = "Layout"


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
        icon = "folder"

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
    content = blocks.StreamBlock(
        COLUMN_BLOCKS + DATA_BLOCKS + CONTENT_BLOCKS, form_classname="pull-right"
    )

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        context["content"] = value.get("content")
        context["color"] = value.get("color")
        return context

    class Meta:
        icon = "left-right"
        label = "Full width container"
        group = "Layout"


NEW_BLOCKS = [
    ("image_text_block", ImageTextBlock()),
    ("latest_resources", NewResourcesTeasersBlock()),
    ("data_teaser", DataTeaserBlock()),
    ("partners", PartnerBlock()),
    ("dealcount", DealCountBlock()),
]

CONTENT_BLOCKS += [("full_width_container", FullWidthContainerBlock(form_classname=""))]
