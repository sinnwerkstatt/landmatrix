from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailcore.blocks import StructBlock
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailcore.blocks import Block, URLBlock, RawHTMLBlock, StreamBlock

from django.utils.html import format_html, format_html_join, force_text
from django.conf import settings
from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.http import Http404

from wagtail_modeltranslation.models import TranslationMixin
from wagtail.wagtailcore import hooks
from wagtail.wagtailcore.whitelist import attribute_rule, check_url, allow_without_attributes
from wagtail.wagtailadmin.edit_handlers import ObjectList
from wagtail.wagtailadmin.views.pages import PAGE_EDIT_HANDLERS
from blog.models import BlogPage

from ol3_widgets.widgets import MapWidget
from landmatrix.models.region import Region as DataRegion
from landmatrix.models.country import Country as DataCountry


class SplitMultiLangTabsMixin(object):
    """ This mixin detects multi-language fields and splits them into seperate tabs per language """
    
    def _split_i18n_wagtail_translated_panels(self, content_panels):
        """ For use with wagtail and wagtail-modeltranslation. This will encapsulate all translatable
            Page content fields in a seperate tab for each language in the wagtail admin.
         """
        object_lists = []
        for (lang, _lang_label) in getattr(settings, 'MODELTRANSLATION_LANGUAGES', getattr(settings, 'LANGUAGES', [])):
            i18n_content_panels = []
            for field_panel in content_panels:
                if field_panel.field_name.endswith(lang):
                    panel_kwargs = {'classname': field_panel.classname} if hasattr(field_panel, 'classname') else {}
                    mod = type(field_panel)(field_panel.field_name, **panel_kwargs)
                    i18n_content_panels.append( mod )
            object_lists.append(ObjectList(i18n_content_panels, heading=_('Content') + ' (%(language)s)' % {'language': lang}))
        return object_lists 
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.__class__ in PAGE_EDIT_HANDLERS and not getattr(PAGE_EDIT_HANDLERS[self.__class__], '_MULTILANG_TABS_PATCHED', False):
            handler = PAGE_EDIT_HANDLERS[self.__class__]
            tabs = [tab_handler.bind_to_model(self.__class__) for tab_handler in self._split_i18n_wagtail_translated_panels(self.content_panels)]
            handler.children = tabs + handler.children[1:]
            handler._MULTILANG_TABS_PATCHED = True

class LinkBlock(StructBlock):
    cls = blocks.ChoiceBlock(choices=[
        ('btn', 'Button'),
    ], required=False, label='Type')
    url = blocks.URLBlock(label='URL')
    text = blocks.CharBlock()

    class Meta:
        icon = 'anchor'
        template = 'widgets/link.html'

    def get_context(self, value):
        context = super().get_context(value)
        context['href'] = value.get('url')
        context['text'] = value.get('text')
        context['class'] = value.get('cls')
        return context

class AnchorBlock(StructBlock):
    slug = blocks.CharBlock()

    class Meta:
        icon = 'anchor'
        template = 'widgets/anchor.html'

    def get_context(self, value):
        context = super().get_context(value)
        context['slug'] = value.get('slug')
        return context


# Overwrite Stream block to disable wrapping DIVs
class NoWrapsStreamBlock(StreamBlock):
    def render_basic(self, value):
        def get_class(block):
            if block.block_type != 'full_width_container':
                return 'block-%s block'%block.block_type
            else:
                return ''

        return format_html_join(
            '\n', '<div class="{1}">{0}</div>',
            [
                (force_text(child), get_class(child)) for child in value
            ]
        )
        #return format_html_join(
        #    '\n', '{0}',
        #    [(force_text(child), child.block_type) for child in value]
        #)

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
    class Meta:
        icon = 'image'
        template = 'widgets/image.html'

    def get_context(self, value):
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

    class Meta:
        icon = 'image'
        template = 'widgets/image.html'

    def get_context(self, value):
        context = super().get_context(value)
        context['href'] = value.url
        context['url'] = value.get_rendition('max-1200x1200').url
        context['name'] = value.title
        return context


class SliderBlock(StructBlock):
    images = blocks.ListBlock(LinkedImageBlock())

    def get_context(self, value):
        context = super().get_context(value)
        context['title'] = value.get('title')
        images_data = value.get('images')
        images = []
        if images_data:
            for image in images_data:
                rendition = image.get('image').get_rendition('max-1200x1200')
                url = rendition.url
                name = image.get('image').title
                image_context = {'url': url, 'name': name, 'href': image.get('url')}
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

    def get_context(self, value):
        context = super().get_context(value)
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

    class Meta:
        icon = 'title'
        label = 'Title'
        template = 'widgets/title.html'

#FIXME: Move blocks to blocks.py
CONTENT_BLOCKS = [
    ('heading', TitleBlock()),
    ('paragraph', blocks.RichTextBlock()),
    ('image', ImageChooserBlock(icon="image")),
    ('media', EmbedBlock(icon="media")),
    ('html', RawHTMLBlock(icon="code")),
    ('link', LinkBlock(icon="link")),
    ('anchor', AnchorBlock(icon="link")),
    ('gallery', GalleryBlock()),
    ('slider', SliderBlock()),
    ('section_divider', SectionDivider()),
]

class CountryRegionStructBlock(StructBlock):
    country = None
    region = None

    def __init__(self, *args, **kwargs):
        self.country = kwargs.pop('country', None)
        self.region = kwargs.pop('region', None)
        super().__init__(*args, **kwargs)

    def get_context(self, value):
        context = super().get_context(value)
        if self.country:
            context['country'] = self.country
        if self.region:
            context['region'] = self.region
        return context

class LatestNewsBlock(CountryRegionStructBlock):
    limit = blocks.CharBlock()

    class Meta:
        icon = 'fa fa-list'
        label = 'Latest news'
        template = 'widgets/latest-news.html'

    def get_context(self, value):
        context = super().get_context(value)
        queryset = BlogPage.objects.order_by('-date')
        if self.country or self.region:
            tag = self.country.slug or self.region.slug
            filter_queryset = queryset.filter(tags__slug=tag)
            if filter_queryset.count() > 0:
                queryset = filter_queryset
            else:
                queryset = queryset.filter(tags__isnull=True)
        limit = value.get('limit')
        context['news'] = queryset[:int(limit)]
        return context

class StatisticsBlock(CountryRegionStructBlock):
    class Meta:
        icon = 'fa fa-list'
        label = 'Statistics'
        template = 'widgets/statistics.html'

class MapDataChartsBlock(CountryRegionStructBlock):
    class Meta:
        icon = 'fa fa-chain'
        label = 'Map / Grid / Charts'
        template = 'widgets/map-data-charts.html'

class LinkMapBlock(CountryRegionStructBlock):
    '''
    Note that the map template used here is the one from ol3_widgets.
    '''
    class Meta:
        icon = 'fa fa-map-marker'
        label = 'Map'
        template = 'widgets/link-map.html'

    def get_mapwidget_context(self, context):
        '''
        Modify map attrs here.
        '''
        widget_context = context.copy()

        bound_attrs = (
            'point_lat_min', 'point_lat_max', 'point_lon_min', 'point_lon_max',
        )
        has_country_bounds = self.country and all(
            [hasattr(self.country, attr) for attr in bound_attrs])
        has_region_bounds = self.region and all(
            [hasattr(self.region, attr) for attr in bound_attrs])

        if has_country_bounds:
            initial_bounds = [
                getattr(self.country, attr) for attr in bound_attrs
            ]
        elif has_region_bounds:
            initial_bounds = [
                getattr(self.region, attr) for attr in bound_attrs
            ]
        else:
            initial_bounds = None

        widget_context.update({
            'width': 800,
            'height': 600,
            'initial_bounds': initial_bounds,
            'disable_drawing': True,
        })

        return widget_context

    def render_mapwidget(self, value, context):
        widget_context = self.get_mapwidget_context(context)
        widget = MapWidget()
        rendered = widget.render('map', value, attrs=widget_context)

        return rendered

    def get_context(self, value):
        context = super().get_context(value)
        context['id'] = 'map'
        context['mapwidget'] = self.render_mapwidget(value, context)

        return context


class LatestDatabaseModificationsBlock(CountryRegionStructBlock):
    limit = blocks.CharBlock()

    class Meta:
        icon = 'fa fa-list'
        label = 'Latest database modifications'
        template = 'widgets/latest-database-modifications.html'

    def get_context(self, value):
        context = super().get_context(value)
        context['limit'] = value.get('limit')
        return context


DATA_BLOCKS = [
    ('latest_news', LatestNewsBlock()),
    ('link_map', LinkMapBlock()),
    ('statistics', StatisticsBlock()),
    ('map_data_charts', MapDataChartsBlock()),
    ('latest_database_modifications', LatestDatabaseModificationsBlock()),
]

class ColumnsBlock(CountryRegionStructBlock):
    left_column = blocks.StreamBlock(CONTENT_BLOCKS + DATA_BLOCKS)
    right_column = blocks.StreamBlock(CONTENT_BLOCKS + DATA_BLOCKS, form_classname='pull-right')

    def get_context(self, value):
        context = super().get_context(value)
        
        for column in ['left_column', 'right_column']:
            context[column] = value.get(column)
        country_or_region = {}
        if hasattr(self, 'country') and self.country:
            country_or_region['country'] = self.country
        if hasattr(self, 'region') and self.region:
            country_or_region['region'] = self.region
        if country_or_region:
            for column in ['left_column', 'right_column']:
                for data in DATA_BLOCKS:
                    context[column].stream_block.child_blocks[data[0]] = type(data[1])(**country_or_region)
        return context

    class Meta:
        icon = 'fa fa-columns'
        label = 'Columns 1-1'
        template = None


class Columns1To1Block(ColumnsBlock):
    class Meta:
        label = 'Columns 1:1'
        template = 'widgets/columns-1-1.html'


class Columns2To1Block(ColumnsBlock):
    class Meta:
        label = 'Columns 2:1'
        template = 'widgets/columns-2-1.html'


class Columns1To2Block(ColumnsBlock):
    class Meta:
        label = 'Columns 1:2'
        template = 'widgets/columns-1-2.html'

COLUMN_BLOCKS = [
    ('columns_1_1', Columns1To1Block()),
    ('columns_2_1', Columns2To1Block()),
    ('columns_1_2', Columns1To2Block())
]
class FullWidthContainerBlock(StructBlock):
    color = blocks.ChoiceBlock(choices=[
        ('white', 'White'),
        ('lightgrey', 'Light grey'),
        ('darkgrey', 'Dark grey')
    ], default='white')
    content = NoWrapsStreamBlock(COLUMN_BLOCKS + DATA_BLOCKS + CONTENT_BLOCKS, form_classname='pull-right')

    def get_context(self, value):
        context = super().get_context(value)
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

class WagtailRootPage(TranslationMixin, SplitMultiLangTabsMixin, Page):
    body = NoWrapsStreamField(CONTENT_BLOCKS + DATA_BLOCKS + COLUMN_BLOCKS)
    footer_column_1 = RichTextField(blank=True)
    footer_column_2 = RichTextField(blank=True)
    footer_column_3 = RichTextField(blank=True)
    footer_column_4 = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
        FieldPanel('footer_column_1'),
        FieldPanel('footer_column_2'),
        FieldPanel('footer_column_3'),
        FieldPanel('footer_column_4')
    ]

class WagtailPage(TranslationMixin, SplitMultiLangTabsMixin, Page):
    body = NoWrapsStreamField(CONTENT_BLOCKS + DATA_BLOCKS + COLUMN_BLOCKS)
    content_panels = Page.content_panels + [StreamFieldPanel('body')]

class RegionIndex(TranslationMixin, SplitMultiLangTabsMixin, Page):
    template = 'wagtailcms/region_page.html'

    body = NoWrapsStreamField(CONTENT_BLOCKS + DATA_BLOCKS + COLUMN_BLOCKS)
    content_panels = Page.content_panels + [
        StreamFieldPanel('body')
    ]
    subpage_types = ['wagtailcms.RegionPage']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.region = None

    def get_context(self, request):
        context = super().get_context(request)
        if self.region:
            context['region'] = self.region
        return context

    def serve(self, request):
        kwargs = request.resolver_match.kwargs
        region_slug = kwargs.get('region_slug', None)
        if region_slug:
            try:
                self.region = DataRegion.objects.get(slug=region_slug)
            except DataRegion.DoesNotExist:
                raise Http404('Region data not found.')
            for data in (DATA_BLOCKS + COLUMN_BLOCKS):
                self.body.stream_block.child_blocks[data[0]] = type(data[1])(region=self.region)
        return super().serve(request)

class RegionPage(TranslationMixin, SplitMultiLangTabsMixin, Page):
    region = models.ForeignKey(DataRegion, null=True, blank=True, on_delete=models.SET_NULL)

    body = NoWrapsStreamField(CONTENT_BLOCKS + DATA_BLOCKS + COLUMN_BLOCKS)
    content_panels = Page.content_panels + [
        StreamFieldPanel('body')
    ]
    promote_panels = [
        FieldPanel('region'),
    ] + Page.promote_panels
    parent_page_types = ['wagtailcms.RegionIndex']

    def serve(self, request):
        if self.region:
            for data in (DATA_BLOCKS + COLUMN_BLOCKS):
                self.body.stream_block.child_blocks[data[0]] = type(data[1])(region=self.region)
        return super().serve(request)

class CountryIndex(TranslationMixin, SplitMultiLangTabsMixin, Page):
    template = 'wagtailcms/country_page.html'

    body = NoWrapsStreamField(CONTENT_BLOCKS + DATA_BLOCKS + COLUMN_BLOCKS)
    content_panels = Page.content_panels + [
        StreamFieldPanel('body')
    ]
    subpage_types = ['wagtailcms.CountryPage']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.country = None

    def get_context(self, request):
        context = super().get_context(request)
        if self.country:
            context['country'] = self.country
        return context

    def serve(self, request):
        kwargs = request.resolver_match.kwargs
        country_slug = kwargs.get('country_slug', None)
        if country_slug:
            try:
                self.country = DataCountry.objects.get(slug=country_slug)
            except DataCountry.DoesNotExist:
                raise Http404('Country data not found.')
            for data in (DATA_BLOCKS + COLUMN_BLOCKS):
                self.body.stream_block.child_blocks[data[0]] = type(data[1])(country=self.country)
        return super().serve(request)

class CountryPage(TranslationMixin, SplitMultiLangTabsMixin, Page):
    country = models.ForeignKey(DataCountry, null=True, blank=True, on_delete=models.SET_NULL)
    body = NoWrapsStreamField(CONTENT_BLOCKS + [
            ('columns_1_1', Columns1To1Block()),
            ('columns_2_1', Columns2To1Block()),
            ('columns_1_2', Columns1To2Block())
        ]
    )
    content_panels = Page.content_panels + [
        StreamFieldPanel('body')
    ]
    promote_panels = [
        FieldPanel('country')
    ] + Page.promote_panels
    parent_page_types = ['wagtailcms.CountryIndex']

    def serve(self, request):
        if self.country:
            for data in (DATA_BLOCKS + COLUMN_BLOCKS):
                self.body.stream_block.child_blocks[data[0]] = type(data[1])(region=self.country)
        return super().serve(request)


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