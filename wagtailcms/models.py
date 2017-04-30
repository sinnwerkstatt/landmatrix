import json

from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailcore.blocks import StructBlock
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailcore.blocks import Block, RawHTMLBlock, StreamBlock

from django.utils.html import format_html, format_html_join, force_text
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.http import Http404
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from wagtail_modeltranslation.models import TranslationMixin
from wagtail.wagtailcore import hooks
from wagtail.wagtailcore.whitelist import attribute_rule
from wagtail.wagtailadmin.edit_handlers import ObjectList
from blog.models import BlogPage

from landmatrix.models.region import Region as DataRegion
from landmatrix.models.country import Country as DataCountry
from wagtailcms.twitter import TwitterTimeline


class LinkBlock(StructBlock):
    cls = blocks.ChoiceBlock(choices=[
        ('btn', 'Button'),
        ('btn btn-with-space', 'Button (with space)'),
    ], required=False, label='Type')
    url = blocks.URLBlock(label='URL')
    text = blocks.CharBlock()

    class Meta:
        icon = 'anchor'
        template = 'widgets/link.html'

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        context['href'] = value.get('url')
        context['text'] = value.get('text')
        context['class'] = value.get('cls')
        return context


class AnchorBlock(StructBlock):
    slug = blocks.CharBlock()

    class Meta:
        icon = 'anchor'
        template = 'widgets/anchor.html'

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        context['slug'] = value.get('slug')
        return context


class FAQBlock(StructBlock):
    slug = blocks.CharBlock()
    question = blocks.CharBlock()
    answer = blocks.RichTextBlock()


class FAQsBlock(StructBlock):
    faqs = blocks.ListBlock(FAQBlock())

    class Meta:
        icon = 'fa fa-medkit'
        template = 'widgets/faq_block.html'

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        context['titel'] = value.get('title')
        context['list'] = []
        for faq in value.get('faqs'):
            context['list'].append({
                'slug': faq.get('slug'),
                'term': faq.get('question'),
                'definition': faq.get('answer')
            })
        return context


class TwitterBlock(StructBlock):
    username = blocks.CharBlock(required=True)
    count = blocks.CharBlock(default=20)

    # help_text='You will find username and widget_id @ https://twitter.com/settings/widgets/')
    # widget_id = CharBlock(required=True)
    # tweet_limit = CharBlock(required=True, max_length=2)

    class Meta:
        icon = 'fa fa-twitter'
        template = 'widgets/twitter.html'

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        twitte = TwitterTimeline(count=(value.get('count')))
        context['timeline'] = twitte.get_timeline(value.get('username'))
        context['username'] = value.get('username') #context['timeline'][0]['screen_name']
        return context


# Overwrite Stream block to disable wrapping DIVs
class NoWrapsStreamBlock(StreamBlock):
    def render_basic(self, value, context=None):
        def get_class(block):
            if block.block_type != 'full_width_container':
                return 'block-%s block'%block.block_type
            else:
                return ''

        return format_html_join(
            '\n', '<div class="{1}">{0}</div>',
            [
                (child.render(context=context), get_class(child))
                for child in value
            ]
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
    url = blocks.URLBlock(required=False, label='URL')

    class Meta:
        icon = 'image'
        template = 'widgets/image.html'

    def get_context(self, value, parent_context=None):
        context = super().get_context(value)
        context['url'] = value.get_rendition('max-1200x1200').url
        context['name'] = value.title
        return context


class SectionDivider(StructBlock):
    class Meta:
        icon = 'fa fa-minus'
        template = 'widgets/divider.html'


class LinkedImageBlock(StructBlock):
    image = ImageChooserBlock()
    url = blocks.URLBlock(required=False, label='URL')
    caption = blocks.RichTextBlock(required=False)

    class Meta:
        icon = 'image'
        template = 'widgets/image.html'

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        context['href'] = value.get('url')
        context['url'] = value.get('image').get_rendition('max-1200x1200').url
        #context['name'] = value.get('caption')
        return context


class SliderBlock(StructBlock):
    images = blocks.ListBlock(LinkedImageBlock())

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        context['title'] = value.get('title')
        images_data = value.get('images')
        images = []
        if images_data:
            for image in images_data:
                rendition = image.get('image').get_rendition('max-1200x1200')
                url = rendition.url
                name = image.get('image').title
                image_context = {
                    'url': url,
                    'name': name,
                    'href': image.get('url'),
                    'caption': image.get('caption')
                }
                images.append(image_context)
        context['images'] = images
        return context

    class Meta:
        icon = 'fa fa-picture-o'
        label = 'Slider'
        template = 'widgets/slider.html'


class GalleryBlock(StructBlock):
    columns = blocks.ChoiceBlock(choices=[
        (1, '1 column'),
        (2, '2 columns'),
        (3, '3 columns'),
        (4, '4 columns'),
        (5, '5 columns'),
        (6, '6 columns'),
    ], icon='fa fa-columns')
    images = blocks.ListBlock(LinkedImageBlock())

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        context['title'] = value.get('title')
        columns_data = value.get('columns')
        if columns_data and columns_data.isdigit():
            context['columns'] = int(columns_data)
        images_data = value.get('images')
        images = []
        if images_data:
            for image in images_data:
                if not image.get('image'):
                    continue
                rendition = image.get('image').get_rendition('max-1200x1200')
                url = rendition.url
                name = image.get('image').title
                image_context = {'url': url, 'name': name, 'href': image.get('url')}
                images.append(image_context)
        context['images'] = images
        return context

    class Meta:
        icon = 'fa fa-th'
        label = 'Gallery'
        template = 'widgets/gallery.html'


class TitleBlock(blocks.CharBlock):

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        return context

    class Meta:
        icon = 'title'
        label = 'Title'
        template = 'widgets/title.html'


class TitleWithIconBlock(StructBlock):
    value = blocks.CharBlock(label='Title')
    fa_icon = blocks.CharBlock(required=False)
    url = blocks.URLBlock(label='URL', required=False)

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        context['value'] = value.get('value')
        context['fa_icon'] = value.get('fa_icon')
        context['url'] = value.get('url')
        return context

    class Meta:
        icon = 'title'
        label = 'Title with Icon'
        template = 'widgets/title.html'


#FIXME: Move blocks to blocks.py
CONTENT_BLOCKS = [
    ('heading', TitleBlock()),
    ('title', TitleWithIconBlock()),
    ('paragraph', blocks.RichTextBlock()),
    ('image', ImageBlock()),
    ('linked_image', LinkedImageBlock()),
    ('media', EmbedBlock(icon="media")),
    ('html', RawHTMLBlock(icon="code")),
    ('link', LinkBlock(icon="link")),
    ('anchor', AnchorBlock(icon="link")),
    ('gallery', GalleryBlock()),
    ('slider', SliderBlock()),
    ('section_divider', SectionDivider()),
    ('twitter', TwitterBlock()),
    ('faqs_block', FAQsBlock()),
]


def get_country_or_region(request, page=None):
    """
    Get country or region from current page (if CountryPage/RegionPage)
    or from URL query (if CountryIndexPage/RegionIndexPage)
    """
    result = {
        'region': None,
        'country': None,
    }
    if hasattr(page, 'region'):
        result['region'] = page.region
    elif hasattr(page, 'country'):
        result['country'] = page.country
    else:
        kwargs = request.resolver_match.kwargs
        if 'region_slug' in kwargs:
            result['region'] = DataRegion.objects.get(slug=kwargs.get('region_slug'))
        elif 'country_slug' in kwargs:
            result['country'] = DataCountry.objects.get(slug=kwargs.get('country_slug'))
    return result


class LatestNewsBlock(StructBlock):
    limit = blocks.CharBlock()

    class Meta:
        icon = 'fa fa-list'
        label = 'Latest news'
        template = 'widgets/latest-news.html'

    def get_context(self, value, parent_context={}):
        context = super().get_context(value, parent_context=parent_context)
        context.update(get_country_or_region(parent_context.get('request'), parent_context.get('page')))
        queryset = BlogPage.objects.order_by('-date')
        tag = None
        if context.get('country'):
            tag = context.get('country').slug
        elif context.get('region'):
            tag = context.get('region').slug
        if tag:
            filter_queryset = queryset.filter(tags__slug=tag)
            if filter_queryset.count() > 0:
                queryset = filter_queryset
            else:
                queryset = queryset.filter(tags__isnull=True)
        limit = value.get('limit')
        context['news'] = queryset[:int(limit)]
        return context


class StatisticsBlock(StructBlock):
    class Meta:
        icon = 'fa fa-list'
        label = 'Statistics'
        template = 'widgets/statistics.html'

    def get_context(self, value, parent_context={}):
        context = super().get_context(value, parent_context=parent_context)
        context.update(get_country_or_region(parent_context.get('request'), parent_context.get('page')))
        return context

class MapDataChartsBlock(StructBlock):
    class Meta:
        icon = 'fa fa-chain'
        label = 'Map / Grid / Charts'
        template = 'widgets/map-data-charts.html'

    def get_context(self, value, parent_context={}):
        context = super().get_context(value, parent_context=parent_context)
        context.update(get_country_or_region(parent_context.get('request'), parent_context.get('page')))
        return context

class LinkMapBlock(StructBlock):
    '''
    Note that the map template used here is NOT the one from ol3_widgets.
    '''
    class Meta:
        icon = 'fa fa-map-marker'
        label = 'Map'
        template = 'widgets/link-map.html'

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context.update(get_country_or_region(parent_context.get('request'), parent_context.get('page')))
        # prevent circular import
        from map.views import MapSettingsMixin
        legend = MapSettingsMixin().get_legend()
        context.update({
            'legend': legend,
            'legend_json': json.dumps(legend),
            'map_object': context.get('region') or context.get('country'),
            'is_country': bool(context.get('country'))
        })
        return context


class LatestDatabaseModificationsBlock(StructBlock):
    limit = blocks.CharBlock()

    class Meta:
        icon = 'fa fa-list'
        label = 'Latest database modifications'
        template = 'widgets/latest-database-modifications.html'

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context.update(get_country_or_region(parent_context.get('request'), parent_context.get('page')))
        context['limit'] = value.get('limit')
        return context


class RegionBlock(StructBlock):
    class Meta:
        icon = 'fa fa-map-marker'
        label = 'Region'
        template = 'widgets/region.html'

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context.update(get_country_or_region(parent_context.get('request'), parent_context.get('page')))
        if context.get('country'):
            context['region'] = self.country.fk_region
        else:
            context['region'] = None
        return context


class CountriesBlock(StructBlock):
    class Meta:
        icon = 'fa fa-flag'
        label = 'Countries'
        template = 'widgets/countries.html'

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context.update(get_country_or_region(parent_context.get('request'), parent_context.get('page')))
        if context.get('region'):
            context['countries'] = DataCountry.objects.filter(fk_region=context.get('region'))
        else:
            context['countries'] = DataCountry.objects.all()
        return context

DATA_BLOCKS = [
    ('latest_news', LatestNewsBlock()),
    ('link_map', LinkMapBlock()),
    ('statistics', StatisticsBlock()),
    ('map_data_charts', MapDataChartsBlock()),
    ('latest_database_modifications', LatestDatabaseModificationsBlock()),
    ('countries', CountriesBlock()),
    ('region', RegionBlock()),
]


class Columns1To1Block(StructBlock):
    left_column = blocks.StreamBlock(CONTENT_BLOCKS + DATA_BLOCKS)
    right_column = blocks.StreamBlock(CONTENT_BLOCKS + DATA_BLOCKS, form_classname='pull-right')

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)

        for column in ['left_column', 'right_column']:
            context[column] = value.get(column)

        return context

    class Meta:
        label = 'Two Columns'
        template = 'widgets/two-columns.html'
        icon = 'fa fa-columns'


class ThreeColumnsBlock(StructBlock):
    left_column = blocks.StreamBlock(CONTENT_BLOCKS + DATA_BLOCKS)
    middle_column = blocks.StreamBlock(CONTENT_BLOCKS + DATA_BLOCKS)
    right_column = blocks.StreamBlock(CONTENT_BLOCKS + DATA_BLOCKS, form_classname='pull-right')

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)

        for column in ['left_column', 'middle_column', 'right_column']:
            context[column] = value.get(column)

        return context

    class Meta:
        label = 'Three Columns'
        template = 'widgets/three-columns.html'
        icon = 'fa fa-columns'

COLUMN_BLOCKS = [
    ('columns_1_1', Columns1To1Block()),
    ('columns_3', ThreeColumnsBlock()),
]


class TabBlock(StructBlock):
    title = blocks.CharBlock()
    fa_icon = blocks.CharBlock(required=False)
    content = blocks.StreamBlock(CONTENT_BLOCKS + DATA_BLOCKS + COLUMN_BLOCKS)


class TabsBlock(StructBlock):
    tabs = blocks.ListBlock(TabBlock())

    class Meta:
        icon = 'fa fa-folder'
        template = 'widgets/tabs_block.html'

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        context['list'] = []
        for tab in value.get('tabs'):
            context['list'].append({
                'title': tab.get('title'),
                'fa_icon': tab.get('fa_icon'),
                'content': tab.get('content')
            })
        return context
CONTENT_BLOCKS += [
    ('tabs_block', TabsBlock()),
]


class FullWidthContainerBlock(StructBlock):
    color = blocks.ChoiceBlock(choices=[
        ('white', 'White'),
        ('lightgrey', 'Light grey'),
        ('darkgrey', 'Dark grey')
    ], default='white')
    content = NoWrapsStreamBlock(COLUMN_BLOCKS + DATA_BLOCKS + CONTENT_BLOCKS, form_classname='pull-right')

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        context['content'] = value.get('content')
        context['color'] = value.get('color')
        return context

    class Meta:
        icon = 'fa fa-arrows-h'
        label = 'Full width container'
        template = 'widgets/full-width-container.html'
CONTENT_BLOCKS += [
    ('full_width_container', FullWidthContainerBlock(form_classname='')),
]


class WagtailRootPage(TranslationMixin, Page):
    body = NoWrapsStreamField(CONTENT_BLOCKS + DATA_BLOCKS + COLUMN_BLOCKS)
    map_introduction = RichTextField(blank=True)
    data_introduction = RichTextField(blank=True)
    #charts_introduction = RichTextField(blank=True)
    footer_column_1 = RichTextField(blank=True)
    footer_column_2 = RichTextField(blank=True)
    footer_column_3 = RichTextField(blank=True)
    footer_column_4 = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
        FieldPanel('map_introduction'),
        FieldPanel('data_introduction'),
        #FieldPanel('charts_introduction'),
        FieldPanel('footer_column_1'),
        FieldPanel('footer_column_2'),
        FieldPanel('footer_column_3'),
        FieldPanel('footer_column_4')
    ]


class WagtailPage(TranslationMixin, Page):
    body = NoWrapsStreamField(CONTENT_BLOCKS + DATA_BLOCKS + COLUMN_BLOCKS)
    content_panels = Page.content_panels + [StreamFieldPanel('body')]

    def serve(self, request):
        # Reset country/region blocks, since they might have been set
        # by a region/country page that has been called just before
        _update_country_region_structs(self.body.stream_block)
        return super().serve(request)

class RegionIndex(TranslationMixin, Page):
    template = 'wagtailcms/region_page.html'

    body = NoWrapsStreamField(CONTENT_BLOCKS + DATA_BLOCKS + COLUMN_BLOCKS)
    content_panels = Page.content_panels + [
        StreamFieldPanel('body')
    ]
    subpage_types = ['wagtailcms.RegionPage']

    def get_context(self, request, *args, **kwarg):
        context = super().get_context(request, *args, **kwargs)
        context.update(get_country_or_region(request))
        return context


class RegionPage(TranslationMixin, Page):
    region = models.ForeignKey(DataRegion, null=True, blank=True, on_delete=models.SET_NULL)

    body = NoWrapsStreamField(CONTENT_BLOCKS + DATA_BLOCKS + COLUMN_BLOCKS)
    content_panels = Page.content_panels + [
        StreamFieldPanel('body')
    ]
    promote_panels = [
        FieldPanel('region'),
    ] + Page.promote_panels
    parent_page_types = ['wagtailcms.RegionIndex']


class CountryIndex(TranslationMixin, Page):
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


class CountryPage(TranslationMixin, Page):
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


#FIXME: Move hooks to wagtail_hooks.py
@hooks.register('insert_editor_js')
def editor_js():
  return format_html(
    """
    <script>
      registerHalloPlugin('hallojustify');
    </script>
    """
  )


@hooks.register('insert_editor_css')
def editor_css():
    # Add extra CSS files to the admin like font-awesome
    css_files = [
        'vendor/font-awesome/css/font-awesome.min.css',
        'css/wagtail-font-awesome.css'
    ]

    css_includes = format_html_join(
        '\n',
        '<link rel="stylesheet" href="{0}{1}">',
        ((settings.STATIC_URL, filename) for filename in css_files))

    return css_includes


@hooks.register('construct_whitelister_element_rules')
def whitelister_element_rules():
    return {
        'h2': attribute_rule({'style': True}),
        'h3': attribute_rule({'style': True}),
        'h4': attribute_rule({'style': True}),
        'h5': attribute_rule({'style': True}),
        'p': attribute_rule({'style': True}),
    }
